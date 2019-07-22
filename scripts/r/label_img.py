from _image import *
from _shutil import *
from _gui import *
from PIL import Image

f = get_files(cd=True)[0]
fn, ext = os.path.splitext(f)
text_file = fn + '.txt'

call(['notepad.exe', text_file])
with open(text_file, 'r') as fp:
    text = fp.read()

im = Image.open(f)
draw_text(im, text, (0, 0, im.width, im.height), align='top')

im.save(fn + '_labelled' + ext)