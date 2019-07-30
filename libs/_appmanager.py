import yaml
import shutil
from os.path import dirname, join
from _shutil import run_elevated
import subprocess


def get_executable(app_name):
    with open(join(dirname(__file__), 'app_list.yaml'), 'r') as f:
        app_list = yaml.load(f.read())

    matched_apps = [k for k, v in app_list.items() if app_name.lower() == k.lower()]
    app_name = matched_apps[0]
    app = app_list[app_name]

    def find_executable():
        for exe in app['executable']:
            if shutil.which(exe):
                return exe
        return None

    # Install app if not exists
    executable = find_executable()

    if executable is None:
        run_elevated('choco source add --name=chocolatey --priority=-1 -s="https://chocolatey.org/api/v2/"')

        pkg_name = app_name
        if 'choco' in app:
            pkg_name = app['choco']
        print('Installing %s...' % pkg_name)
        run_elevated(['choco', 'install', pkg_name, '-y'])
        executable = find_executable()

    return executable


if __name__ == '__main__':
    # For testing
    get_executable('7z')
