# -*- coding: utf-8 -*-
"""Testes de geometria PDF sem dependência do Windows / GUI."""
import math
import sys
from pathlib import Path
import pytest
from PIL import Image, ImageDraw
from pypdf import PdfReader

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from a3_two_a4 import plan_a3_two, export_a3_two_a4

@pytest.mark.parametrize("orientation,mode,expected", [
  ("horizontal","safe",(210.,297.)),
  ("horizontal","borderless",(210.,297.)),
  ("vertical","safe",(297.,210.)),
  ("vertical","borderless",(297.,210.)),
])
def test_a3_two_a4_geometry(tmp_path,orientation,mode,expected):
    im=Image.new("RGB",(720,1200),(220,228,232))
    d=ImageDraw.Draw(im)
    d.line((0,600,720,600),fill=(120,43,36),width=40)
    image=tmp_path/"input.png"
    im.save(image)
    out=tmp_path/"out.pdf"
    p=export_a3_two_a4(image,out,orientation,mode,8)
    reader=PdfReader(str(out))
    assert len(reader.pages)==2
    for page in reader.pages:
        assert abs(float(page.mediabox.width)*25.4/72-expected[0])<0.02
        assert abs(float(page.mediabox.height)*25.4/72-expected[1])<0.02
    assert p["pages"]==2 and p["nx"]*p["ny"]==2
    assert p["image_width"]<=p["work_w"]+1.e-7
    assert p["image_height"]<=p["work_h"]+1.e-7
    assert abs(p["image_width"]/p["image_height"]-720/1200)<1.e-5

def test_standard_printer_not_claimed_to_be_exact_a3():
    for o in ["horizontal","vertical"]:
        p=plan_a3_two(o,"safe",8)
        if o=="horizontal":
            assert (p["assembled_width"],p["assembled_height"])==(404,297)
            assert (p["work_w"],p["work_h"])==(388,281)
        else:
            assert (p["assembled_width"],p["assembled_height"])==(297,404)
            assert (p["work_w"],p["work_h"])==(281,388)

def test_exact_a3_requires_borderless():
    for o in ["horizontal","vertical"]:
        p=plan_a3_two(o,"borderless",8)
        assert p["m"]==0
        assert (p["assembled_width"],p["assembled_height"])==(
            (420,297) if o=="horizontal" else (297,420))
    with pytest.raises(ValueError, match="pelo menos"):
        plan_a3_two("horizontal","safe",0)

def test_invalid_parameters():
    for o,m,margin in [("diagonal","safe",8),("horizontal","unknown",8),
                         ("horizontal","safe",-1),("horizontal","safe",float("nan"))]:
        with pytest.raises(ValueError):
            plan_a3_two(o,m,margin)
