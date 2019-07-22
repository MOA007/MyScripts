from _video import *
import cv2
from _script import *

if '{{CROP_RECT}}':
    CROP_RECT = [int(x) for x in '{{CROP_RECT}}'.split()]
else:
    CROP_RECT = None


def crop_image(im, rect):
    return im[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2], :]


cur_folder = os.environ['CURRENT_FOLDER']
chdir(cur_folder)

files = list(glob.glob('*.png'))
files = sorted(files)

imgs = []
for i, f in enumerate(files):
    print('Processing (%d / %d)...' % (i, len(files)))
    im = cv2.imread(f)
    if CROP_RECT:
        im = crop_image(im, CROP_RECT)
    imgs.append(im)

make_video(imgs, out_file='out.mp4')