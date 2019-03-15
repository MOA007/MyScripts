import subprocess
import os

try:
    import moviepy
except:
    subprocess.call('pip install moviepy')
    import requests

from moviepy.editor import VideoFileClip, TextClip, ColorClip, clips_array, vfx
import numpy as np
import moviepy.editor as mpy


def generate_video_matrix(vid_files, titles=None, out_file=None, columns=None, fps=None):
    if out_file is None:
        out_file = 'combined.mp4'

    os.environ['IMAGEMAGICK_BINARY'] = r"C:\Program Files\ImageMagick-7.0.8-Q16\magick.exe"

    if vid_files[0] is str:
        vid_clips = [VideoFileClip(x, resize_algorithm='fast_bilinear') for x in vid_files]
    else:
        vid_clips = vid_files
    max_h = np.max([x.h for x in vid_clips])

    vid_clips = [x.fx(vfx.resize, max_h / x.h) for x in vid_clips]
    vid_clips = [x.margin(2) for x in vid_clips]

    dura = np.max([x.duration for x in vid_clips])
    print('Duration: %i' % dura)

    def create_text_clip(text, dura):
        global src
        return TextClip(text,
                        font='Verdana',
                        fontsize=max_h / 20,
                        color='white') \
            .set_duration(dura)

    if titles is None:
        titles = [os.path.splitext(os.path.basename(x))[0] for x in vid_files]
    text_clips = [create_text_clip(x, dura) for x in titles]

    arr = []
    if columns is not None:
        for i in range(0, len(vid_clips), columns):
            arr.append(vid_clips[i:i + columns])
            arr.append(text_clips[i:i + columns])

        remainder = len(vid_clips) % columns
        if remainder != 0:
            remainder = columns - remainder
            blank_clip = ColorClip((1, 1), color=(0, 0, 0), duration=0)
            arr[-1].extend([blank_clip] * remainder)
            arr[-2].extend([blank_clip] * remainder)

    else:
        arr.append(vid_clips)
        arr.append(text_clips)

    final = clips_array(arr)

    final.write_videofile(out_file, fps=fps)
