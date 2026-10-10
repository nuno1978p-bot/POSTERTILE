# -*- coding: utf-8 -*-
"""Geometry for the NONIVERUS Composition Studio pointer editor.

All positions of the text anchor are percentages of the *image*, not of the
QLabel/widget, so letterboxing and window resizes cannot displace the text.
This module has no Qt dependencies and can be tested without a GUI.
"""
from __future__ import annotations
from math import isfinite


def fitted_image_rect(view_w: float, view_h: float, image_w: float, image_h: float) -> tuple[float, float, float, float]:
    """Return (left, top, width, height) of an aspect-fitted, centered image."""
    values = (view_w, view_h, image_w, image_h)
    if not all(isfinite(float(v)) and v > 0 for v in values):
        raise ValueError("Dimensões da imagem ou do ecrã inválidas")
    scale = min(view_w / image_w, view_h / image_h)
    width = image_w * scale
    height = image_h * scale
    return ((view_w - width) / 2, (view_h - height) / 2, width, height)


def image_rect_to_view(
    bounds: tuple[float, float, float, float],
    fitted: tuple[float, float, float, float],
    image_w: float,
    image_h: float,
) -> tuple[float, float, float, float]:
    """Map a glyph bounding rectangle in source image pixels to label pixels."""
    left, top, w, h = fitted
    bx, by, bw, bh = bounds
    return (
        left + bx * w / image_w,
        top + by * h / image_h,
        bw * w / image_w,
        bh * h / image_h,
    )


def point_hits_rect(x: float, y: float, rect: tuple[float, float, float, float], pad: float = 8) -> bool:
    left, top, width, height = rect
    return (left - pad <= x <= left + width + pad and
            top - pad <= y <= top + height + pad)


def drag_anchor(
    original_x: float, original_y: float,
    pointer_dx: float, pointer_dy: float,
    displayed_image_width: float, displayed_image_height: float,
    snap_pixels: float = 9.0,
) -> tuple[float, float, bool, bool]:
    """Translate a mouse delta, snapping anchors to the image's central axes.

    Snapping occurs in screen pixels to remain predictable at all zoom levels.
    Returns (x_percent, y_percent, snapped_x, snapped_y).
    """
    if displayed_image_width <= 0 or displayed_image_height <= 0:
        raise ValueError("Imagem sem dimensão visível")
    x = min(100.0, max(0.0, original_x + 100.0 * pointer_dx / displayed_image_width))
    y = min(100.0, max(0.0, original_y + 100.0 * pointer_dy / displayed_image_height))
    snap_x = abs(x - 50.0) * displayed_image_width / 100.0 <= snap_pixels
    snap_y = abs(y - 50.0) * displayed_image_height / 100.0 <= snap_pixels
    return (50.0 if snap_x else x, 50.0 if snap_y else y, snap_x, snap_y)
