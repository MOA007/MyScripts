from _term import *
from _shutil import *
from _editor import *


def grep(src_dir, exclude=[]):
    repo_root = None
    rel_path = None
    ps = None
    lines = []
    files = set()
    cur_text = None

    if False:
        tmp_path = ""
        for comp in src_dir.split("\\"):
            tmp_path += comp + "\\"
            if exists(tmp_path + ".gitignore"):
                print("REPO ROOT: " + tmp_path)
                repo_root = tmp_path
                rel_path = src_dir.replace(repo_root, "")
                print(rel_path)
                break

        input()

    def on_text_changed(s):
        nonlocal ps, cur_text
        cur_text = s
        if ps is not None:
            ps.kill()
            ps = None

    def on_item_selected(i):
        arr = lines[i].split(":")
        file = os.path.join(src_dir, arr[0])
        line_no = arr[1]
        open_in_vscode(file, line_no)

    if repo_root:
        chdir(repo_root)
    else:
        chdir(src_dir)
    
    lw = ListWindowAsync(
        lines=lines, on_text_changed=on_text_changed, on_item_selected=on_item_selected
    )

    text = None
    while True:
        while cur_text == text:
            time.sleep(0.1)
            lw.update()
        text = cur_text

        if text == "":
            lines.clear()
            continue

        args = f'rg --line-number -F "{text}"'
        if rel_path:
            args += " " + rel_path

        if not exists(".gitignore"):
            args += ' -g "!intermediates/" -g "!build/" -g "!Build/"'
        for x in exclude:
            args += ' -g "!%s"' % x

        ps = check_output2(args)

        lines.clear()
        files.clear()
        for l in ps.readlines(block=False, timeout=0.1):
            if l is not None:
                s = l.decode(errors="replace")
                s = s.strip()
                lines.append(s)

            lw.update()


grep(src_dir=r"{{SOURCE_FOLDER}}", exclude="{{_EXCLUDE}}".split())
