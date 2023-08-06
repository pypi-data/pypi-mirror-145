#!/usr/bin/env python3
# coding: utf-8

import colorsys
from math import pi, sqrt, cos, sin
from typing import NamedTuple


def hsl_to_bicone_xyz(hue: float, sat: float, lit: float):
    """
    Args:
        hue: 0. ~ 1.
        sat: 0. ~ 1., saturation
        lit: 0. ~ 1., lightness
    Returns: 3-tuple, (x, y, z)
    """
    theta = 2. * pi * hue
    z = 2. * sqrt(2) * (lit - .5)
    r = (sqrt(2) - abs(z)) / sqrt(2)
    x = r * sat * cos(theta)
    y = r * sat * sin(theta)
    return x, y, z


def pct360_hsl_to_bicone_xyz(h_hue: float, h_sat: float, h_lit: float):
    return hsl_to_bicone_xyz(h_hue / 360., h_sat / 100., h_lit / 100.)


def hsl_to_rgb(hue: float, sat: float, lit: float):
    return colorsys.hls_to_rgb(hue, lit, sat)


def pct360_hsl_to_rgb(h_hue: float, h_sat: float, h_lit: float):
    return hsl_to_rgb(h_hue / 360., h_sat / 100., h_lit / 100.)


class Color(NamedTuple):
    r: float
    g: float
    b: float

    @classmethod
    def from_uint8_rgb(cls, ir: int, ig: int, ib: int):
        return cls(ir / 255., ig / 255., ib / 255.)

    @property
    def uint8_rgb(self) -> tuple:
        return (
            int(self.r * 255),
            int(self.g * 255),
            int(self.b * 255),
        )

    @property
    def hsl(self) -> tuple:
        """
        Returns: 3-tuple, (hue, sat, lit)
            hue: (float) 0. ~ 1.
            sat: (float) 0. ~ 1., saturation
            lit: (float) 0. ~ 1., lightness
        """
        hue, lit, sat = colorsys.rgb_to_hls(*self)
        return hue, sat, lit

    @property
    def pct360_hsl(self) -> tuple:
        """
        Returns: 3-tuple, (h_hue, h_sat, h_lit)
            h_hue: (int) 0 ~ 360
            h_sat: (int) 0 ~ 100, saturation
            h_lit: (int) 0 ~ 100, lightness
        """
        hue, lit, sat = colorsys.rgb_to_hls(*self)
        return (
            int(hue * 360),
            int(sat * 100),
            int(lit * 100),
        )

    @property
    def bicone_xyz(self) -> tuple:
        """
        Returns: 3-tuple, (x, y, z)
        """
        return hsl_to_bicone_xyz(*self.hsl)


named_colors = {
    'k': Color(0, 0, 0),
    'r': Color(1, 0, 0),
    'g': Color(0, 1, 0),
    'b': Color(0, 0, 1),
    'w': Color(1, 1, 1),
    'y': Color(1, 1, 0),
    'c': Color(0, 1, 1),
    'm': Color(1, 0, 1),
    'red': Color(1, 0, 0),
    'blue': Color(0, 0, 1),
    'cyan': Color(0, 1, 1),
    'black': Color(0, 0, 0),
    'white': Color(1, 1, 1),
    'green': Color(0, 1, 0),
    'yellow': Color(1, 1, 0),
    'magenta': Color(1, 0, 1),
}