#!/usr/bin/env python
import os
import subprocess
import glob
import time
import sys


def file_filter(name):
    return name.endswith(".py")


def get_mtime():
    for filename in glob.iglob('*.py'):
        yield os.stat(filename).st_mtime
    for filename in glob.iglob('scripts/*.*', recursive=True):
        yield os.stat(filename).st_mtime


command = [sys.executable, 'main.py']

# How often we check the filesystem for changes (in seconds)
WAIT = 1

# The process to autoreload
process = subprocess.Popen(command)

# The current maximum file modified time under the watched directory
last_mtime = max(get_mtime())


while True:
    try:
        max_mtime = max(get_mtime())
        # print_stdout(process)
        if max_mtime > last_mtime:
            last_mtime = max_mtime
            process.kill()
            process = subprocess.Popen(command)
        time.sleep(WAIT)
    except KeyboardInterrupt:
        process.kill()
        process = subprocess.Popen(command)
