from typing import Any, NamedTuple
import webbrowser
import urllib
import re
import capture_animation
from slide.generate import generate_slide
from r.open_with.open_with_ import open_with
from _shutil import *
from collections import defaultdict
from collections import OrderedDict
import numpy as np

if 1:
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))


if 1:  # Import moviepy
    f = glob.glob(r"C:\Program Files\ImageMagick-*\magick.exe")[0]
    os.environ["IMAGEMAGICK_BINARY"] = f
    from moviepy.config import change_settings
    from moviepy.editor import *
    import moviepy.video.fx.all as vfx
    import moviepy.audio.fx.all as afx
    from moviepy.video.tools.subtitles import SubtitlesClip


change_settings({"FFMPEG_BINARY": "ffmpeg"})

PROJ_DIR = r"{{VIDEO_PROJECT_DIR}}"

FPS = int("{{_FPS}}")
FADEOUT_DURATION = 0.25
PARSE_LINE_START = int("{{_PARSE_LINE_START}}") if "{{_PARSE_LINE_START}}" else None
PARSE_LINE_END = int("{{_PARSE_LINE_END}}") if "{{_PARSE_LINE_END}}" else None

ADD_SUBTITLE = False

VOLUME_DIM = 0.15


class _VideoClipInfo:
    def __init__(self):
        self.file: str = None
        self.start: float = 0
        self.duration: float = None
        self.mpy_clip: Any = None
        self.speed: float = 1
        self.pos = None
        self.fadein: bool = False
        self.fadeout: bool = False


class _AudioClipInfo:
    def __init__(self):
        self.file: str = None
        self.mpy_clip: Any = None
        self.speed: float = 1


class _AnimationInfo:
    def __init__(self):
        self.clip_info_list = []
        self.url = None
        self.calc_length = True
        self.url_params = {}


_audio_clips = []
cur_markers = None

_audio_track_cur_pos = 0
_pos_list = [0]
_pos_dict = {"a": 0}


_add_fadeout_to_last_clip = False

_video_tracks = OrderedDict(
    [("vid", []), ("hl", []), ("hl2", []), ("md", []), ("sub", [])]
)
_cur_vid_track_name = "vid"  # default video track

_animations = defaultdict(_AnimationInfo)

_subtitle = []
_srt_lines = []
_srt_index = 1

_bgm_file = None
_bgm = {}
_bgm_vol = []


def _get_vid_track(name=None):
    if name is None:
        name = _cur_vid_track_name

    if name not in _video_tracks:
        track = []
        _video_tracks[name] = track
    else:
        track = _video_tracks[name]

    return track


def _get_markers(file):
    marker_file = file + ".marker.txt"
    if os.path.exists(marker_file):
        with open(marker_file, "r") as f:
            s = f.read()
            return [float(x) for x in s.split()]
    else:
        return None


def _get_pos(p):
    PATT_FLOAT = r"([-+]?\d*\.?\d*)"

    if p is None:
        return _pos_list[-1]

    if type(p) == int or type(p) == float:
        return float(p)

    if type(p) == str:
        if p in _pos_dict:
            return _pos_dict[p]

        # TODO: remove
        match = re.match(r"^\+=" + PATT_FLOAT + "$", p)
        if match:
            delta = float(match.group(1))
            return _pos_list[-1] + delta

        # TODO: remove
        match = re.match(r"^\<" + PATT_FLOAT + "$", p)
        if match:
            delta = float(match.group(1))
            clip_info = _get_vid_track()[-1]
            return clip_info.start + delta

        # TODO: remove
        match = re.match(r"^(\^+)" + PATT_FLOAT + "$", p)
        if match:
            index_back_in_history = len(match.group(1))
            delta = float(match.group(2))
            return _pos_list[-index_back_in_history - 1] + delta

        match = re.match(r"^([a-z_]+)" + PATT_FLOAT + "$", p)
        if match:
            tag = match.group(1)
            delta = float(match.group(2))
            return _pos_dict[tag] + delta

    raise Exception("Invalid param.")


def _set_pos(p):
    new_pos = _get_pos(p)
    _pos_list.append(new_pos)


def _format_time(sec):
    td = datetime.timedelta(seconds=sec)
    return "%02d:%02d:%02d,%03d" % (
        td.seconds // 3600,
        td.seconds // 60,
        td.seconds % 60,
        td.microseconds // 1000,
    )


def _generate_text_image(
    text,
    font="Source-Han-Sans-CN",
    font_size=44,
    color="#ffffff",
    stroke_color="#555555",
):
    # Generate subtitle png image using magick
    tempfile_fd, tempfilename = tempfile.mkstemp(suffix=".png")
    os.close(tempfile_fd)
    cmd = [
        glob.glob(r"C:\Program Files\ImageMagick-*\magick.exe")[0],
        "-background",
        "transparent",
        "-font",
        font,
        "-pointsize",
        "%d" % font_size,
        "-stroke",
        stroke_color,
        "-strokewidth",
        "6",
        "-gravity",
        "center",
        "label:%s" % text,
        "-stroke",
        "None",
        "-fill",
        color,
        "label:%s" % text,
        "-layers",
        "merge",
        "PNG32:%s" % tempfilename,
    ]
    subprocess.check_call(cmd)
    return tempfilename


def _add_subtitle_clip(start, end, text):
    tempfilename = _generate_text_image(text)

    ci = _VideoClipInfo()
    ci.mpy_clip = (
        ImageClip(tempfilename).set_duration(end - start).set_pos(("center", 910))
    )
    ci.start = start
    ci.duration = end - start
    _video_tracks["sub"].append(ci)


def record(f, start="a", **kwargs):
    print(f)
    audio("tmp/record/" + f + ".final.wav", start=start, **kwargs)

    END_CHAR = ["。", "，", "！"]

    global _srt_index
    assert len(_subtitle) > 0

    if ADD_SUBTITLE:
        start = end = _get_pos("as")
        subtitle = _subtitle[-1].strip()

        if subtitle[-1] not in END_CHAR:
            subtitle += END_CHAR[0]

        length = len(subtitle)
        word_dura = (_get_pos("ae") - start) / length

        i = 0
        MAX = 5
        word = ""

        while i < length:
            if subtitle[i] in ["，", "。", "！"] and len(word) > MAX:
                _srt_lines.extend(
                    [
                        "%d" % _srt_index,
                        "%s --> %s" % (_format_time(start), _format_time(end)),
                        word,
                        "",
                    ]
                )

                _add_subtitle_clip(start=start, end=end, text=word)

                end += word_dura
                start = end
                word = ""
                _srt_index += 1
            else:
                word += subtitle[i]
                end += word_dura

            i += 1


def audio_gap(duration):
    _bgm_vol.append((_pos_dict["a"], "in"))

    _pos_dict["a"] += duration
    _pos_list.append(_pos_dict["a"])

    _bgm_vol.append((_pos_dict["a"], "out"))


def bgm(vol, duration=0.25):
    print("bgm:", (_pos_list[-1], vol, duration))
    _bgm_vol.append((_pos_list[-1], vol, duration))


def bgm_file(file):
    global _bgm_file
    _bgm_file = file


def audio(f, start=None, duration=None):
    global cur_markers

    _pos_dict["as"] = _get_pos(start)
    _pos_list.append(_pos_dict["as"])

    # HACK: still don't know why changing buffersize would help reduce the noise at the end
    audio_clip = AudioFileClip(f, buffersize=400000)

    # if start is not None:
    #     audio_clip = audio_clip.subclip(start)

    audio_clip = audio_clip.set_start(_pos_dict["as"])

    if duration is not None:
        audio_clip = audio_clip.set_duration(duration)

    _audio_clips.append(audio_clip)

    # Forward audio track pos
    _pos_dict["a"] = _pos_dict["ae"] = _pos_dict["as"] + audio_clip.duration

    # Get markers
    cur_markers = _get_markers(f)
    if cur_markers:
        print(cur_markers)


def pos(p):
    _set_pos(p)


def image(f, **kwargs):
    _add_clip(f, **kwargs)


def text(text, track="sub", **kwargs):
    temp_file = _generate_text_image(
        text, font="zcool-gdh", font_size=100, color="#ffd700", stroke_color="#6900ff",
    )
    _add_clip(temp_file, track=track, pos=("center", 750), **kwargs)


def _add_fadeout(track):
    global _add_fadeout_to_last_clip

    if _add_fadeout_to_last_clip:
        clip_info = track[-1]

        if clip_info.mpy_clip is not None:
            clip_info.mpy_clip = clip_info.mpy_clip.fx(vfx.fadeout, FADEOUT_DURATION)

            _add_fadeout_to_last_clip = False


def create_image_seq_clip(tar_file):
    tmp_folder = os.path.join(
        tempfile.gettempdir(),
        "animation",
        os.path.splitext(os.path.basename(tar_file))[0],
    )

    # Unzip
    print2("Unzip to %s" % tmp_folder)
    shutil.unpack_archive(tar_file, tmp_folder)

    # Get all image files
    image_files = sorted(glob.glob((os.path.join(tmp_folder, "*.png"))))

    clip = ImageSequenceClip(image_files, fps=FPS)
    return clip


def _update_prev_clip(track):
    _clip_extend_prev_clip(track)

    # _add_fadeout(track)


def _create_mpy_clip(
    file=None,
    clip_operations=None,
    speed=None,
    pos=None,
    text_overlay=None,
    no_audio=False,
    duration=None,
    vol=None,
):
    if file is None:
        clip = ColorClip((200, 200), color=(0, 1, 0)).set_duration(0)

    elif file.endswith(".tar"):
        clip = create_image_seq_clip(file)

    elif file.endswith(".png"):
        clip = ImageClip(file).set_duration(4)

    else:
        clip = VideoFileClip(file)

        if duration is not None:
            clip = clip.set_duration(duration)

        if text_overlay is not None:
            mkdir("tmp/text_overlay")
            overlay_file = "tmp/text_overlay/%s.png" % slugify(text_overlay)
            if not os.path.exists(overlay_file):
                generate_slide(
                    text_overlay, template_file="source.html", out_file=overlay_file
                )
            im_clip = ImageClip(overlay_file).set_duration(clip.duration)
            clip = CompositeVideoClip([clip, im_clip])

    if speed is not None:
        clip = clip.fx(vfx.speedx, speed)

    if clip_operations is not None:
        clip = clip_operations(clip)

    if no_audio:
        clip = clip.set_audio(None)
    
    if clip.audio is not None and vol:
        clip.audio = _adjust_mpy_audio_clip_volume(clip.audio, vol)

    if pos is not None:
        # half_size = [x // 2 for x in clip.size]
        # clip = clip.set_position((pos[0] - half_size[0], pos[1] - half_size[1]))
        clip = clip.set_position(pos)

    return clip


def _add_clip(
    file=None,
    clip_operations=None,
    speed=None,
    pos=None,
    tag=None,
    track=None,
    fadein=False,
    fadeout=False,
    start=None,
    **kwargs
):
    track = _get_vid_track(track)

    # _update_prev_clip(track)

    cur_pos = _get_pos(start)
    _pos_dict["vs"] = cur_pos

    # TODO: remove??
    if tag:
        _pos_dict[tag] = cur_pos

    clip_info = _VideoClipInfo()
    clip_info.file = file
    clip_info.start = cur_pos
    clip_info.pos = pos
    clip_info.speed = speed
    clip_info.fadein = fadein
    clip_info.fadeout = fadeout

    if file is not None:
        clip_info.mpy_clip = _create_mpy_clip(
            file=file, clip_operations=clip_operations, speed=speed, pos=pos, **kwargs
        )

        # Advance the pos
        end = cur_pos + clip_info.mpy_clip.duration
        _pos_list.append(end)
        _pos_dict["ve"] = end

    track.append(clip_info)

    return clip_info


def _animation(url, name, track=None, params={}, calc_length=True, **kwargs):
    anim = _animations[name]
    anim.url = url
    anim.url_params = params
    anim.calc_length = calc_length
    anim.clip_info_list.append(_add_clip(track=track, **kwargs))


def anim(s, **kwargs):
    _animation(url="http://localhost:8080/%s.html" % s, name=slugify(s), **kwargs)


def image_anim(file, t=5):
    _animation(
        url="http://localhost:8080/image.html",
        name=os.path.splitext(file)[0],
        params={"t": "%d" % t, "src": file},
    )


def title_anim(h1, h2, **kwargs):
    _animation(
        url="http://localhost:8080/title-animation.html",
        name=slugify("title-%s-%s" % (h1, h2)),
        params={"h1": h1, "h2": h2},
        **kwargs
    )


def _clip_extend_prev_clip(track=None):
    if len(track) == 0:
        return

    clip_info = track[-1]

    if clip_info.duration is None:
        clip_info.duration = _pos_list[-1] - clip_info.start
        print(
            "previous clip (start, duration) updated: (%.2f, %.2f)"
            % (clip_info.start, clip_info.duration)
        )


def empty(track=None):
    track = _get_vid_track(track)
    _clip_extend_prev_clip(track)


def video(f, **kwargs):
    print("Video: %s" % f)
    _add_clip(f, tag="video", **kwargs)


def screencap(f, speed=None, track=None, **kwargs):
    _add_clip(
        f,
        clip_operations=lambda x: x.crop(x1=0, y1=0, x2=2560, y2=1380)
        .resize(0.75)
        .set_position((0, 22)),
        speed=speed,
        tag="video",
        track=track,
        **kwargs
    )


def md(s, track="md", **kwargs):
    mkdir("tmp/slides")
    out_file = "tmp/slides/%s.png" % slugify(s)

    if not os.path.exists(out_file):
        generate_slide(
            s, template_file="markdown.html", out_file=out_file, gen_html=True
        )

    _add_clip(out_file, track=track, fadein=True, fadeout=True, **kwargs)


def hl(pos, track="hl"):
    image("images/highlight.png", pos=pos, track=track, fadein=True, fadeout=True)


def track(name="vid"):
    global _cur_vid_track_name
    _cur_vid_track_name = name


def _framehold_track_gap(track):
    prev_clip_info = None
    for clip_info in track:
        if (prev_clip_info is not None) and (clip_info.duration is None):
            prev_clip_info.duration = clip_info.start - prev_clip_info.start

        prev_clip_info = clip_info


def _export_video(resolution=(1920, 1080), fps=FPS):
    # Update clip duration for each track
    for track in _video_tracks.values():
        _framehold_track_gap(track)

    # Animation
    if 1:
        for name, animation_info in _animations.items():
            out_file = "tmp/animation/%s.mov" % name
            os.makedirs("tmp/animation", exist_ok=True)

            if 1:  # generate animation video file

                if not os.path.exists(out_file):
                    params = {**animation_info.url_params}

                    if animation_info.calc_length:
                        subclip_dura_list = "|".join(
                            ["%g" % x.duration for x in animation_info.clip_info_list]
                        )
                        print(subclip_dura_list)

                        params.update({"t": subclip_dura_list})

                    final_url = (
                        animation_info.url
                        + "?"
                        + "&".join(
                            [
                                "%s=%s" % (k, urllib.parse.quote(v))
                                for k, v in params.items()
                            ]
                        )
                    )

                    capture_animation.capture_js_animation(
                        url=final_url, out_file=out_file,
                    )

            for i, clip_info in enumerate(animation_info.clip_info_list):
                clip_info.mpy_clip = _create_mpy_clip(
                    file=(out_file if i == 0 else "tmp/animation/%s.%d.mov" % (name, i))
                )

    # Update fx for each track.
    for track in _video_tracks.values():
        for i, clip_info in enumerate(track):
            assert clip_info.mpy_clip is not None
            assert clip_info.duration is not None if i < len(track) - 1 else True

            if clip_info.duration is not None:
                # Use duration to extend / hold the last frame instead of creating new clips.
                clip_info.mpy_clip = clip_info.mpy_clip.set_duration(clip_info.duration)

            if clip_info.fadein:
                if clip_info.file and clip_info.file.endswith(".png"):
                    clip_info.mpy_clip = clip_info.mpy_clip.crossfadein(
                        FADEOUT_DURATION
                    )
                else:
                    clip_info.mpy_clip = clip_info.mpy_clip.fx(
                        vfx.fadein, FADEOUT_DURATION
                    )

            if clip_info.fadeout:
                if clip_info.file and clip_info.file.endswith(".png"):
                    clip_info.mpy_clip = clip_info.mpy_clip.crossfadeout(
                        FADEOUT_DURATION
                    )
                else:
                    clip_info.mpy_clip = clip_info.mpy_clip.fx(
                        vfx.fadeout, FADEOUT_DURATION
                    )

    _create_bgm()

    video_clips = []
    for _, track in _video_tracks.items():
        for clip_info in track:
            video_clips.append(clip_info.mpy_clip.set_start(clip_info.start))

    final_clip = CompositeVideoClip(video_clips, size=resolution)

    if final_clip.audio:
        _audio_clips.append(final_clip.audio)

    final_clip = final_clip.set_audio(CompositeAudioClip(_audio_clips))

    # final_clip.show(10.5, interactive=True)
    # final_clip.preview(fps=10, audio=False)

    final_clip.write_videofile(
        "out.mp4", codec="libx264", threads=8, fps=fps, ffmpeg_params=["-crf", "19"]
    )

    open_with("out.mp4", program_id=1)


def _adjust_mpy_audio_clip_volume(clip, vol):
    xp = []
    fp = []
    cur_vol = 0

    for i, (start, vol, duration) in enumerate(vol):
        if isinstance(vol, (int, float)):
            xp += [start, start + duration]
            fp += [cur_vol, vol]
            cur_vol = vol

        else:
            raise Exception("unsupported bgm parameter type:" % type(vol))

    def volume_adjust(gf, t):
        factor = np.interp(t, xp, fp)
        factor = np.vstack([factor, factor]).T
        return factor * gf(t)

    return clip.fl(volume_adjust)


def _create_bgm():
    if _bgm_file is None:
        return

    if not os.path.exists(_bgm_file):
        raise Exception("Please make sure `%s` exists.")

    # .subclip(13.8, 60)
    clip = AudioFileClip(_bgm_file).set_duration(60)

    clip = _adjust_mpy_audio_clip_volume(clip, [0, VOLUME_DIM, 0.5] + _bgm_vol)

    _audio_clips.append(clip)


def _export_srt():
    with open("out.srt", "w", encoding="utf-8") as f:
        f.write("\n".join(_srt_lines))


if __name__ == "__main__":
    cd(PROJ_DIR)

    with open("index.md", "r", encoding="utf-8") as f:
        lines = f.readlines()

        if PARSE_LINE_START is not None:
            lines = lines[(PARSE_LINE_START - 1) : (PARSE_LINE_END)]

        # Remove all comments
        s = "\n".join(lines)
        s = re.sub("<!--[\d\D]*?-->", "", s)
        lines = s.splitlines()

        for line in lines:
            line = line.strip()
            if line.startswith("! "):
                python_code = line.lstrip("! ")
                exec(python_code, globals())

            elif line.startswith("#"):
                pass

            elif line != "":
                print2(line, color="green")
                _subtitle.append(line)

    # _export_srt()

    # sys.exit(0)

    _export_video()
