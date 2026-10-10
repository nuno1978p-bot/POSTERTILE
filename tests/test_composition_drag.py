# -*- coding: utf-8 -*-
"""No GUI required: image/viewport maths for draggable text."""
import unittest
from composition_drag import fitted_image_rect, image_rect_to_view, point_hits_rect, drag_anchor


class TestCompositionDrag(unittest.TestCase):
    def test_aspect_fit_letterbox_wide(self):
        rect=fitted_image_rect(640,480,1200,600)
        self.assertEqual(rect,(0.,80.,640.,320.))
        middle=image_rect_to_view((300,150,600,300),rect,1200,600)
        self.assertEqual(middle,(160.,160.,320.,160.))
        self.assertTrue(point_hits_rect(319,239,middle))
        self.assertFalse(point_hits_rect(70,239,middle))

    def test_aspect_fit_letterbox_portrait(self):
        rect=fitted_image_rect(640,480,600,1200)
        self.assertEqual(rect,(200.,0.,240.,480.))
        # Text on an image with empty sidebars: pointer in sidebar is not a hit.
        mapped=image_rect_to_view((150,240,300,720),rect,600,1200)
        self.assertEqual(mapped,(260.,96.,120.,288.))
        self.assertFalse(point_hits_rect(100,190,mapped))
        self.assertTrue(point_hits_rect(320,190,mapped))

    def test_drag_percent_from_screen_pixels(self):
        x,y,sx,sy=drag_anchor(30,36,64,60,640,320)
        self.assertAlmostEqual(x,40)
        self.assertAlmostEqual(y,54.75)
        self.assertFalse(sx)
        self.assertFalse(sy)

    def test_snap_both_axes(self):
        x,y,sx,sy=drag_anchor(45,46,28,18,640,480)
        self.assertEqual((x,y),(50,50))
        self.assertTrue(sx)
        self.assertTrue(sy)

    def test_nosnap_outside_tolerance(self):
        x,y,sx,sy=drag_anchor(45,46,18,0,640,480)
        self.assertFalse(sx)
        self.assertFalse(sy)
        self.assertAlmostEqual(x,47.8125)

    def test_clamps_to_canvas(self):
        x,y,sx,sy=drag_anchor(80,20,10000,-10000,800,400)
        self.assertEqual((x,y),(100,0))
        self.assertFalse(sx)
        self.assertFalse(sy)

    def test_resize_changes_mapping_not_anchor(self):
        # Same normalized drag on different viewports -> identical result.
        a=drag_anchor(10,20,64,32,640,320)
        b=drag_anchor(10,20,128,64,1280,640)
        self.assertEqual(a,b)

    def test_invalid_sizes(self):
        with self.assertRaises(ValueError):
            fitted_image_rect(0,200,400,400)
        with self.assertRaises(ValueError):
            drag_anchor(20,20,12,12,0,400)


if __name__=="__main__":
    unittest.main()
