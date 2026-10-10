# -*- coding: utf-8 -*-
"""Geometry/preview/PDF regression tests; pure Python, no GUI required."""
import math
from pathlib import Path
import pytest
from PIL import Image, ImageDraw

from poster_framing import image_placement, framed_thumbnail
from postertile_engine import export_pdf
from a3_two_a4 import export_a3_two_a4


def test_fit_has_unprinted_bands():
    dw,dh,ox,oy=image_placement(800,200,420,594,"Ajustar")
    assert math.isclose(dw,420)
    assert math.isclose(dh,105)
    assert ox==0
    assert oy>0


def test_fill_crops_without_stretch():
    dw,dh,ox,oy=image_placement(800,200,420,594,"Preencher")
    assert math.isclose(dw/dh,4.0)
    assert math.isclose(dh,594)
    assert ox<0
    assert oy==0


def test_custom_focus_uses_exact_left_and_right_extremes():
    centred=image_placement(800,200,420,594,"Personalizado",50,50)
    left=image_placement(800,200,420,594,"Personalizado",0,50)
    right=image_placement(800,200,420,594,"Personalizado",100,50)
    assert left[:2]==right[:2]==centred[:2]
    assert left[2] == 0
    assert right[2] == 420-right[0]
    assert math.isclose(centred[2],(left[2]+right[2])/2)


@pytest.mark.parametrize("mode",["Ajustar","Preencher","Personalizado"])
def test_thumbnail_respects_composition_geometry(tmp_path,mode):
    source=Image.new("RGB",(600,200),"blue")
    dr=ImageDraw.Draw(source)
    dr.rectangle((0,0,99,199),fill="red")
    dr.rectangle((500,0,599,199),fill="green")
    fn=tmp_path/"bands.png"
    source.save(fn)
    thumb=framed_thumbnail(fn,300,300,mode,0,50,max_side=600)
    assert thumb.size==(600,600)
    if mode=="Ajustar":
        assert thumb.getpixel((300,20))==(255,255,255)
    else:
        assert thumb.getpixel((300,20))!=(255,255,255)
    # Left focus on filled crop shows the red strip, while right focus shows green.
    if mode=="Personalizado":
        assert thumb.getpixel((5,300))[0] > 200
        right=framed_thumbnail(fn,300,300,mode,100,50,max_side=600)
        assert right.getpixel((595,300))[1] > 70


def test_invalid_mode_or_focus_is_not_silent():
    with pytest.raises(ValueError):
        image_placement(100,100,200,200,"unknown")
    with pytest.raises(ValueError):
        image_placement(100,100,200,200,"Personalizado",101,50)


def test_both_exporters_accept_fit_and_focus(tmp_path):
    from PIL import Image
    try:
        import fitz
    except ImportError:
        fitz = None
    fn=tmp_path/"poster.png"
    im=Image.new("RGB",(600,220),"white")
    draw=ImageDraw.Draw(im)
    draw.rectangle((0,0,200,219),fill="red")
    draw.rectangle((400,0,599,219),fill="blue")
    im.save(fn)
    for mode in ("Ajustar","Preencher","Personalizado"):
        pdf=tmp_path/f"main_{mode}.pdf"
        result=export_pdf(str(fn),str(pdf),297,420,margin=8,overlap=10,
                          paper="A4 vertical",assembly="Cortar e unir",
                          fit=mode,focal_x=100,focal_y=50)
        assert pdf.stat().st_size > 800
        if fitz:
            with fitz.open(pdf) as doc:
                assert len(doc)==result["pages"]
                assert doc[0].rect.width>0
        small=tmp_path/f"a3_{mode}.pdf"
        result=export_a3_two_a4(str(fn),str(small),"horizontal","safe",
                                 fit=mode,focal_x=100,focal_y=50)
        assert small.stat().st_size > 800
        if fitz:
            with fitz.open(small) as doc:
                assert len(doc)==2
