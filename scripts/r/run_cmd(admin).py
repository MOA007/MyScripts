import os
import subprocess

if 'CURRENT_FOLDER' in os.environ:
    os.chdir(os.environ['CURRENT_FOLDER'])
subprocess.Popen('cmd', close_fds=True)
