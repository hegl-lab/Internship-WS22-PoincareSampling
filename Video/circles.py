from manim import *
from hyperbolic_polygon import HyperbolicArcBetweenPoints
from geometry_util import moving_circle, \
    moving_line, polar_to_point, tf_poincare_to_klein, \
    get_both_intersections_line_with_unit_circle
import numpy as np

class CreateCircle(Scene):
    def construct(self):
        self.play(Create(Circle()))
        self.wait(2)

class Createf(Scene):
    def construct(self):
        circle = Circle(color=WHITE, radius = 1, stroke_width=2)

        vg = VGroup()
        vg.add(circle)

        angle_start = np.pi/12
        angle_end = np.pi*11/12
        for angle in np.arange(angle_start, angle_end+angle_start, angle_start):
            vg.add(HyperbolicArcBetweenPoints(polar_to_point(angle), polar_to_point(-angle), stroke_width=2, color=LIGHT_PINK))

        angle_start = -5/12*np.pi
        angle_end = np.pi/2
        for angle in np.arange(angle_start, angle_end, np.pi/12):
            vg.add(HyperbolicArcBetweenPoints(polar_to_point(angle), polar_to_point(np.pi-angle), stroke_width=2, color=RED_A))
        
        # vg = vg.shift(2)
        self.play(Create(vg))
        
        self.wait(5)
