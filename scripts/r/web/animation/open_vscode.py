from _shutil import *
from _editor import *

proj_dir = r"{{VIDEO_PROJECT_DIR}}"

subprocess.call(
    'MKLINK /J "%USERPROFILE%\\.vscode\\extensions\\my-animation-extension" "{}"'.format(
        os.path.join(os.getcwd(), "_extension")
    ),
    shell=True,
)

os.makedirs(os.path.join(proj_dir, "animation"), exist_ok=True)
os.makedirs(os.path.join(proj_dir, "record"), exist_ok=True)
os.makedirs(os.path.join(proj_dir, "tmp"), exist_ok=True)
os.makedirs(os.path.join(proj_dir, "video"), exist_ok=True)
os.makedirs(os.path.join(proj_dir, "image"), exist_ok=True)

