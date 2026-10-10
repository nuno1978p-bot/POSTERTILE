# -*- coding: utf-8 -*-
"""PosterTile framing geometry shared by preview and PDF output.

Coordinates are expressed in target mm (or any other consistent target units).
Ajustar: entire source visible, possible white letterboxing.
Preencher: fills poster, centrally crops overflow.
Personalizado: fills poster, crops overflow around chosen focus (0-100%).
No mode stretches an image.
"""
from math import isfinite

MODES = ("Ajustar", "Preencher", "Personalizado")


def image_placement(iw, ih, w, h, mode="Ajustar", focal_x=50.0, focal_y=50.0):
    values = (iw, ih, w, h, focal_x, focal_y)
    if not all(isfinite(float(v)) for v in values):
        raise ValueError("Invalid framing dimensions or focus.")
    if min(iw, ih, w, h) <= 0:
        raise ValueError("Image and poster dimensions must be positive.")
    if mode not in MODES:
        raise ValueError("Unknown framing mode.")
    if not (0 <= focal_x <= 100 and 0 <= focal_y <= 100):
        raise ValueError("Framing focus must be between 0 and 100.")
    factor = min(w / iw, h / ih) if mode == "Ajustar" else max(w / iw, h / ih)
    dw, dh = iw * factor, ih * factor
    fx, fy = (focal_x / 100, focal_y / 100) if mode == "Personalizado" else (.5, .5)
    ox = (w - dw) * fx
    oy = (h - dh) * fy
    return dw, dh, ox, oy


def flatten_source(source):
    """Mimics the engine's EXIF correction, alpha bounds, and white background."""
    from PIL import Image, ImageOps
    raw = ImageOps.exif_transpose(source).convert("RGBA")
    if source.mode in ("RGBA", "LA", "P"):
        alpha = raw.getchannel("A")
        bbox = alpha.point(lambda a: 255 if a > 8 else 0).getbbox()
        if bbox:
            raw = raw.crop(bbox)
    bg = Image.new("RGBA", raw.size, "white")
    return Image.alpha_composite(bg, raw).convert("RGB")


def framed_thumbnail(image_path, target_w, target_h, mode="Ajustar",
                     focal_x=50.0, focal_y=50.0, max_side=1200):
    """Render a geometry-matched thumbnail without allocating a huge scaled original.

    PIL's inverse affine transform maps each preview pixel to a corresponding
    source pixel; out-of-bounds areas are white, exactly as in the PDF.
    """
    from PIL import Image
    if not 128 <= max_side <= 4096:
        raise ValueError("Preview size outside allowed range.")
    with Image.open(image_path) as source:
        im = flatten_source(source)
    iw, ih = im.size
    dw, dh, ox, oy = image_placement(
        iw, ih, target_w, target_h, mode, focal_x, focal_y
    )
    scale = min(max_side / target_w, max_side / target_h)
    pw, ph = max(1, round(target_w * scale)), max(1, round(target_h * scale))
    # target pixel -> original image pixel
    a = iw / (dw * scale)
    e = ih / (dh * scale)
    c = -ox * iw / dw
    f = -oy * ih / dh
    return im.transform(
        (pw, ph), Image.Transform.AFFINE, (a, 0.0, c, 0.0, e, f),
        resample=Image.Resampling.BICUBIC, fillcolor=(255, 255, 255)
    )
