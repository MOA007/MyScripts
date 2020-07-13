import sys
import os
import curses
import curses.ascii
import re
import time

SCRIPT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.append(os.path.join(SCRIPT_ROOT, "libs"))
sys.path.append(os.path.join(SCRIPT_ROOT, "bin"))

import run_python
from _script import *


GLOBAL_HOTKEY = os.path.join(tempfile.gettempdir(), "GlobalHotkey.ahk")


def execute_script(script):
    args = update_env_var_explorer()
    script.execute(args=args)


def setup_console_font():
    import ctypes

    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.c_ulong),
            ("nFont", ctypes.c_ulong),
            ("dwFontSize", COORD),
            ("FontFamily", ctypes.c_uint),
            ("FontWeight", ctypes.c_uint),
            ("FaceName", ctypes.c_wchar * LF_FACESIZE),
        ]

    font = CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font.nFont = 12
    font.dwFontSize.X = 11
    font.dwFontSize.Y = 18
    font.FontFamily = 54
    font.FontWeight = 400
    font.FaceName = "Lucida Console"

    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(
        handle, ctypes.c_long(False), ctypes.pointer(font)
    )


class InputWidget:
    def __init__(self, label="", text=""):
        self.text = text
        self.label = label
        self.caret_pos = len(text)

    def on_update_screen(self, stdscr, row, cursor=False):
        stdscr.addstr(row, 0, self.label)

        text_start = len(self.label) + 1 if self.label else 0
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(row, text_start, self.text)
        stdscr.attroff(curses.color_pair(1))

        if cursor:
            stdscr.move(row, self.caret_pos + text_start)

    def clear(self):
        self.text = ""
        self.caret_pos = 0

    def on_getch(self, ch):
        if ch == curses.ERR:
            pass
        elif ch == curses.KEY_LEFT:
            self.caret_pos = max(self.caret_pos - 1, 0)
        elif ch == curses.KEY_RIGHT:
            self.caret_pos = min(self.caret_pos + 1, len(self.text))
        elif ch == ord("\b"):
            self.text = self.text[: self.caret_pos - 1] + self.text[self.caret_pos :]
            self.caret_pos = max(self.caret_pos - 1, 0)
        elif ch == curses.ascii.ctrl(ord("a")):
            self.clear()
        elif ch == ord("\n"):
            pass
        elif re.match("[\x00-\x7F]", chr(ch)):
            self.text = (
                self.text[: self.caret_pos] + chr(ch) + self.text[self.caret_pos :]
            )
            self.caret_pos += 1


def sort_scripts(scripts):
    script_access_time, _ = get_all_script_access_time()

    def key(script):
        if script.script_path in script_access_time:
            return max(
                script_access_time[script.script_path],
                os.path.getmtime(script.script_path),
            )
        else:
            return os.path.getmtime(script.script_path)

    return sorted(scripts, key=key, reverse=True)


def search_items(items, kw):
    if not kw:
        for i, s in enumerate(items):
            yield i, s
    else:
        tokens = kw.split(" ")
        for i, item in enumerate(items):
            if all([(x in str(item).lower()) for x in tokens]):
                yield i, item


def on_hotkey():
    pass


def register_hotkeys(scripts):
    hotkeys = {}
    for script in scripts:
        hotkey = script.meta["hotkey"]
        if hotkey is not None:
            print("Hotkey: %s: %s" % (hotkey, script.name))

            hotkey = hotkey.lower()
            key = hotkey[-1].lower()

            if "ctrl+" in hotkey:
                ch = curses.ascii.ctrl(ord(key))
                hotkeys[ch] = script
            elif "shift+" in hotkey or "alt+" in hotkey:
                # HACK: use `shift+` in place of `alt+`
                ch = ord(key.upper())
                hotkeys[ch] = script

    return hotkeys


class SearchWindow:
    def __init__(self, stdscr, items, label=">", text=""):
        self.input_ = InputWidget(label=label, text=text)
        self.items = items
        self.closed = False
        self.stdscr = stdscr

        while True:
            height, width = stdscr.getmaxyx()

            # Search scripts
            matched_items = list(search_items(items, self.input_.text))

            # Sreen update
            stdscr.clear()

            # Get matched scripts
            row = 2
            max_row = height
            for i, (idx, item) in enumerate(matched_items):
                stdscr.addstr(row, 0, "%d. %s" % (idx + 1, str(item)))
                row += 1
                if row >= max_row:
                    break

            self.input_.on_update_screen(stdscr, 0, cursor=True)
            stdscr.refresh()

            # Keyboard event
            ch = stdscr.getch()

            if ch == ord("\n") or ch == ord("\t"):
                if len(matched_items) > 0:
                    item_index, item = matched_items[0]
                else:
                    item = None
                    item_index = -1

                if ch == ord("\n"):
                    self.on_enter_pressed(self.input_.text, item_index)
                else:
                    self.on_tab_pressed(self.input_.text, item_index)

            elif ch == 27:
                return

            elif self.on_getch(ch):
                pass

            else:
                self.input_.on_getch(ch)

            if self.closed:
                return

    def on_getch(self, ch):
        return False

    def on_enter_pressed(self, text, item_index):
        pass

    def on_tab_pressed(self, text, item_index):
        pass

    def close(self):
        self.closed = True


class VariableEditWindow(SearchWindow):
    def __init__(self, stdscr, vars, var_name):
        self.vars = vars
        self.var_name = var_name

        super().__init__(
            stdscr,
            [],
            label=var_name + " :",
            text=(self.vars[var_name][-1] if len(self.vars[var_name]) > 0 else ""),
        )

    def on_enter_pressed(self, text, item_index):
        self.vars[self.var_name] = text
        self.close()


def get_variable_str_list(variables):
    result = []
    max_width = max([len(val_name) for val_name in variables]) + 1
    for _, (var_name, var_val) in enumerate(variables.items()):
        result.append(
            var_name.ljust(max_width) + ": " + (var_val[-1] if len(var_val) > 0 else "")
        )
    return result


class VariableSearchWindow(SearchWindow):
    def __init__(self, stdscr, script):
        self.vars = get_script_variables(script)
        self.items = []

        if len(self.vars):
            self.update_items()
            super().__init__(stdscr, self.items, label="%s >" % (script.name))

    def update_items(self):
        self.items.clear()
        self.items.extend(get_variable_str_list(self.vars))

    def on_getch(self, ch):
        if ch == ord("\t"):
            self.close()
        else:
            super().on_getch(ch)

    def on_enter_pressed(self, text, item_index):
        var_name = list(self.vars)[item_index]
        VariableEditWindow(self.stdscr, self.vars, var_name)
        self.update_items()
        self.input_.clear()


class State:
    def __init__(self):
        self.scripts = []
        self.modified_time = {}
        self.last_ts = 0
        self.hotkeys = {}
        self.execute_script = None


def add_keyboard_hooks(keyboard_hooks):
    if sys.platform != "linux":
        import keyboard

        keyboard.unhook_all()
        for hotkey, func in keyboard_hooks.items():
            keyboard.add_hotkey(hotkey, func)


def register_global_hotkeys(scripts):
    if platform.system() == "Windows":
        htk_definitions = ""
        with open(GLOBAL_HOTKEY, "w") as f:
            for item in scripts:
                hotkey = item.meta["globalHotkey"]
                if hotkey is not None:
                    print("Global Hotkey: %s: %s" % (hotkey, item.name))
                    hotkey = hotkey.replace("Ctrl+", "^")
                    hotkey = hotkey.replace("Alt+", "!")
                    hotkey = hotkey.replace("Shift+", "+")
                    hotkey = hotkey.replace("Win+", "#")

                    htk_definitions += (
                        f'{hotkey}::RunScript("{item.name}", "{item.script_path}")\n'
                    )

            # TODO: use templates
            f.write(
                """#SingleInstance, Force
#include libs/ahk/ExplorerHelper.ahk
; SetTitleMatchMode, 2
RunScript(name, path)
{
if WinExist(name)
{
    WinActivate % name
}
else if WinExist("Administrator:  " name)
{
    WinActivate % "Administrator:  " name
}
else
{
    WriteDefaultExplorerInfo()
    Run cmd /c """
                + sys.executable
                + ' "'
                + os.path.realpath("bin/run_script.py")
                + """" --new_window=None --console_title "%name%" --restart_instance 0 "%path%" || pause
}
}

#If not WinActive("ahk_exe vncviewer.exe")
"""
                + htk_definitions
                + """
#If
"""
            )

        subprocess.Popen([get_ahk_exe(), GLOBAL_HOTKEY], close_fds=True, shell=True)

    else:
        keyboard_hooks = {}
        for script in scripts:
            hotkey = script.meta["globalHotkey"]
            if hotkey is not None:
                print("Global Hotkey: %s: %s" % (hotkey, script.name))
                keyboard_hooks[hotkey] = lambda script=script: execute_script(script)
        add_keyboard_hooks(keyboard_hooks)


def main(stdscr):
    # # Clear screen
    # stdscr.clear()

    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    stdscr = curses.initscr()
    stdscr.keypad(1)
    stdscr.nodelay(False)

    input_ = InputWidget(">")

    while True:
        # Reload scripts
        now = time.time()
        if now - state.last_ts > 2.0:
            load_scripts(state.scripts, state.modified_time, autorun=True)
            state.scripts = sort_scripts(state.scripts)
            state.hotkeys = register_hotkeys(state.scripts)
            register_global_hotkeys(state.scripts)

        state.last_ts = now

        height, width = stdscr.getmaxyx()

        # Search scripts
        matched_scripts = list(search_items(state.scripts, input_.text))

        # Sreen update
        stdscr.clear()

        # Get matched scripts
        row = 2
        max_row = height
        for i, (idx, script) in enumerate(matched_scripts):
            stdscr.addstr(row, 0, "%d. %s" % (idx + 1, str(script)))
            row += 1

            if i == 0:
                vars = get_script_variables(script)
                if len(vars):
                    str_list = get_variable_str_list(vars)
                    max_row = max(5, height - len(vars))
                    for i, s in enumerate(str_list):
                        if max_row + i >= height:
                            break
                        stdscr.addstr(max_row + i, 0, s)

            if row >= max_row:
                break

        input_.on_update_screen(stdscr, 0, cursor=True)
        stdscr.refresh()

        # Keyboard event
        ch = stdscr.getch()

        if ch == ord("\n"):
            if matched_scripts:
                _, script = matched_scripts[0]

                update_script_acesss_time(script)

                state.execute_script = lambda: execute_script(script)
                return

        elif ch == 27:
            pass

        elif ch == curses.ascii.ctrl(ord("c")):
            return

        elif ch == ord("\t"):
            if matched_scripts:
                _, script = matched_scripts[0]

                VariableSearchWindow(stdscr, script)

        elif ch in state.hotkeys:
            if matched_scripts:
                _, script = matched_scripts[0]
                script_abs_path = os.path.abspath(script.script_path)
                os.environ["_SCRIPT_PATH"] = script_abs_path

                state.execute_script = lambda: execute_script(script)
                return

        elif ch != 0:
            input_.on_getch(ch)


def init():
    os.environ["PATH"] = os.pathsep.join(
        [os.path.join(SCRIPT_ROOT, "bin"), os.environ["PATH"]]
    )
    os.environ["PYTHONPATH"] = os.path.join(SCRIPT_ROOT, "libs")

    refresh_env()

    setup_nodejs(install=False)

    if is_instance_running():
        print("An instance is running. Exited.")
        sys.exit(0)


if __name__ == "__main__":
    # setup_console_font()

    init()

    state = State()

    while True:
        curses.wrapper(main)
        if state.execute_script is not None:
            state.execute_script()
            state.execute_script = None

            # HACK: workaround: key bindings will not work on windows.
            time.sleep(1)
        else:
            break
