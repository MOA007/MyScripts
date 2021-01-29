from _gui import *
from _script import *
from _shutil import *
import markdown2
import webbrowser
from r.web.webscreenshot import webscreenshot

SCALE = 1
GEN_HTML = bool("{{GEN_HTML}}")
REGENERATE = True

# TODO: hack
if os.path.exists("palette.json"):
    _root = os.getcwd()
else:
    _root = os.path.abspath(os.path.dirname(__file__))


_template_loader = jinja2.FileSystemLoader(searchpath=_root)
_template_env = jinja2.Environment(loader=_template_loader)
_palette = json.load(open(os.path.join(_root, "palette.json")))


def generate_slide(
    text, template_file, out_file=None, gen_html=False, im_size=(1920, 1080)
):
    if out_file is None:
        out_file = get_hash(text) + ".png"

    text = markdown2.markdown(text, extras=["break-on-newline", "fenced-code-blocks"])
    print(text)

    template = _template_env.get_template(template_file)
    # this is where to put args to the template renderer
    html = template.render({"text": text, "palette": _palette})

    if gen_html:
        html_file = out_file + ".html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html)
    else:
        html_file = write_temp_file(html, ".html")

    webscreenshot(html_file=html_file, out_file=out_file)

    return out_file


if __name__ == "__main__":
    im_size = (
        int("{{_W}}") if "{{_W}}" else 1920,
        int("{{_H}}") if "{{_H}}" else 1080,
    )

    in_file = get_files()[0]
    in_file_name = os.path.splitext(os.path.basename(in_file))[0]
    template_file = in_file_name + ".html"
    if not os.path.exists(template_file):
        # Specify template file from parameter
        template_file = "{{GS_TEMPLATE}}"
        if not template_file:
            templates = list(sorted(glob.glob("*.html")))
            i = search(templates)
            template_file = templates[i]
            set_variable("GS_TEMPLATE", template_file)

    out_folder = os.path.dirname(in_file)

    with open(in_file, encoding="utf-8") as f:
        s = f.read()
    slides = s.split("---")
    slides = [x.strip() for x in slides]

    for text in slides:
        out_file = os.path.join(out_folder, get_hash(text) + ".png")
        if REGENERATE or (not os.path.exists(out_file)):
            print2("Generate %s ..." % out_file)

            generate_slide(
                text,
                template_file,
                out_file=out_file,
                gen_html=GEN_HTML,
                im_size=im_size,
            )
