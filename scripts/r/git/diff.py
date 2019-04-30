from _shutil import *

prepend_to_path([
    r'C:\Program Files (x86)\Meld',
    r'C:\Program Files (x86)\Meld\lib'
])

call('git config --global diff.tool meld')
call('git config --global difftool.prompt false')
call(['git', 'config', '--global', 'difftool.meld.cmd', 'meld "$LOCAL" "$REMOTE"'])

chdir(r'{{GIT_REPO}}')
call('git difftool')