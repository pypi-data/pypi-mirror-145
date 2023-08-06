import logging
import os
from PIL import Image, ImageFont, ImageDraw
from pydantic import BaseModel, Field, validate_arguments

font_cache = {}  # NOTE: This will not work concurrently


@validate_arguments
def get_font(font_name: str, size: int):
    if (font_name, size) not in font_cache:
        font = ImageFont.truetype(font_name, size)
        font_cache[(font_name, size)] = font
    return font_cache[(font_name, size)]


@validate_arguments
def text_dims(font_name: str, size: int, text: str):
    font = get_font(font_name, size)

    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text).getbbox()[2]
    text_height = font.getmask(text).getbbox()[3] + descent

    return (text_width, text_height)


@validate_arguments
def require_env(name, default=None):
    assert (
        default is not None or name in os.environ
    ), "Environment variable '%s' must be set" % (name)
    return os.environ.get(name, default)


def EnvField(name, default=None):
    return Field(default_factory=lambda: require_env(name, default))


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]


@validate_arguments
def prefixed_logger(prefix: str, log_level: int):
    log = logging.getLogger(prefix)
    log.setLevel(log_level)
    log.propagate = False
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: [" + prefix + "] %(message)s"
    )
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log
