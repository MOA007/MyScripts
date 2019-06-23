from _gui import search
import sys
import subprocess

PKGS = {
    'other': [
        'miktex',
        'unity --version 2018.2.0',
        'unity --version 2018.2.14',
        'sketchup',
        'blender',
        'graphviz',
        'inkscape',
        'mousewithoutborders',
        'tightvnc',
        'gifcam',
        'autohotkey',
        'nsis',
    ],
    'common': [
        'everything',
        'irfanview',
    ],
    'dev': [
        'conemu',
        'atom',
        'graphviz',
        'anaconda3',
        'miniconda3',
        'pycharm-community',
        'cmake',
        'visualstudio2017community',
        'androidstudio',
        'android-sdk',
        'llvm',
        'ripgrep',
        'vscode',
        'sumatrapdf',
    ],
    'media': [
        'ffmpeg',
        'vlc',
        'imagemagick',
    ],
    'for_work': [
        'p4v',
        'selenium-chrome-driver',
    ],
    'ue4': [
        'directx',
    ]
}

pkg_list = ['@for work'] + sorted([app for cate in PKGS.values() for app in cate])
idx = search(pkg_list)
if idx < 0:
    sys.exit(1)

subprocess.call('choco source add --name=chocolatey --priority=-1 -s="https://chocolatey.org/api/v2/"')

if pkg_list[idx] == '@for work':
    for pkg in [PKGS['for_work'] + PKGS['media'] + PKGS['dev'] + PKGS['common']]:
        subprocess.call('choco install %s -y' % pkg)
else:
    subprocess.call('choco install %s -y' % pkg_list[idx])
