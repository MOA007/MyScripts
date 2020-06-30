import sys
import os
import curses
import curses.ascii
import re

sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), "libs"))
sys.path.append(os.path.join(os.path.realpath(os.path.dirname(__file__)), "bin"))

import run_python
from _script import *


class Input:
    def __init__(self):
        self.text = ""
        self.caret_pos = 0

    def on_update_screen(self, stdscr, row, cursor=False):

        stdscr.addstr(row, 0, self.text)

        if cursor:
            stdscr.move(row, self.caret_pos)

    def on_getch(self, ch):
        text_changed = False

        if ch == curses.ERR:
            pass
        elif ch == curses.KEY_LEFT:
            self.caret_pos = max(self.caret_pos - 1, 0)
        elif ch == curses.KEY_RIGHT:
            self.caret_pos = min(self.caret_pos + 1, len(self.text))
        elif ch == ord("\b"):
            self.text = self.text[: self.caret_pos - 1] + self.text[self.caret_pos :]
            self.caret_pos = max(self.caret_pos - 1, 0)
            text_changed = True
        elif ch == curses.ascii.ctrl(ord("a")):
            self.text = ""
            self.caret_pos = 0
            text_changed = True
        elif ch == ord("\n"):
            pass
        elif re.match("[\x00-\x7F]", chr(ch)):
            self.text = (
                self.text[: self.caret_pos] + chr(ch) + self.text[self.caret_pos :]
            )
            self.caret_pos += 1
            text_changed = True

        if text_changed:
            pass


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


def search_scripts(scripts, kw):
    if not kw:
        for s in scripts:
            yield s

    tokens = kw.split(" ")
    for i, script in enumerate(scripts):
        if all([(x in script.name.lower()) for x in tokens]):
            yield script


def main(stdscr):
    scripts = []
    modified_time = {}

    # # Clear screen
    # stdscr.clear()

    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    stdscr = curses.initscr()
    stdscr.keypad(1)
    stdscr.nodelay(False)

    input_ = Input()

    last_ts = 0

    while True:
        # Reload scripts
        now = time.time()
        if now - last_ts > 2.0:
            load_scripts(scripts, modified_time, autorun=False)
            scripts = sort_scripts(scripts)

        height, width = stdscr.getmaxyx()

        # Keyboard event
        ch = stdscr.getch()
        if ch == ord("\n"):
            if matched_scripts:
                matched_scripts[0].execute()
                update_script_acesss_time(script)
        else:
            input_.on_getch(ch)

        # Search scripts
        matched_scripts = list(search_scripts(scripts, input_.text))

        # Sreen update
        stdscr.clear()

        # Get matched scripts
        row = 2
        for script in matched_scripts:
            stdscr.addstr(row, 0, script.name)
            row += 1
            if row >= height:
                break

        input_.on_update_screen(stdscr, 0, cursor=True)
        stdscr.refresh()

        last_ts = now


curses.wrapper(main)
