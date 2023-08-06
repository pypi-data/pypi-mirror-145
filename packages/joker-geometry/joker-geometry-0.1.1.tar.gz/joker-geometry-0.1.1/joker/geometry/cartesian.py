#!/usr/bin/env python3
# coding: utf-8

import functools
from math import sqrt
from typing import NamedTuple, List


class Point2D(NamedTuple):
    x: float = 0.
    y: float = 0.


class Vector2D(NamedTuple):
    x: float = 0.
    y: float = 0.


class Point3D(NamedTuple):
    x: float = 0.
    y: float = 0.
    z: float = 0.


class Vector3D(NamedTuple):
    x: float = 0.
    y: float = 0.
    z: float = 0.


def _auto_cast(cls_2d, cls_3d, /):
    """Cast 2-tuple or 3-tuple into specified types"""

    def decorating_function(func):
        @functools.wraps(func)
        def _func(*args, **kwargs):
            rv: tuple = func(*args, **kwargs)
            ndim = len(rv)
            if ndim == 2:
                return cls_2d(*rv)
            if ndim == 3:
                return cls_3d(*rv)
            return rv

        return _func

    return decorating_function


@_auto_cast(Vector2D, Vector3D)
def vsum(*vectors: tuple) -> tuple:
    rv = (sum(w) for w in zip(*vectors))
    return tuple(rv)


@_auto_cast(Vector2D, Vector3D)
def vdiff(vector1: tuple, vector2: tuple) -> tuple:
    ndim = len(vector1)
    assert len(vector2) == ndim
    rv = (u - v for u, v in zip(vector1, vector2))
    if ndim == 2:
        return Vector2D(*rv)
    if ndim == 3:
        return Vector3D(*rv)
    return tuple(rv)


def dot_product(vector1: tuple, vector2: tuple) -> float:
    return sum(u * v for u, v in zip(vector1, vector2))


def manhattan_norm(vector: tuple) -> float:
    return sum((abs(x) for x in vector))


def euclidean_norm(vector: tuple) -> float:
    return sqrt(dot_product(vector, vector))


def euclidean_distance(point1: tuple, point2: tuple) -> float:
    return euclidean_norm(vdiff(point1, point2))


@_auto_cast(Vector2D, Vector3D)
def get_a_perpendicular_vector(vector: tuple) -> tuple:
    lcoordinates = list(vector)
    n = len(lcoordinates)
    rcoordinates = [0.] * n
    for i in range(n):
        if lcoordinates[i]:
            j = (i + 1) % n
            rcoordinates[j] = -lcoordinates[i]
            rcoordinates[i] = lcoordinates[j]
            break
    return tuple(rcoordinates)


class Line2D(NamedTuple):
    a: float = 1.
    b: float = 1.
    c: float = 1.

    def __contains__(self, point: tuple):
        """inaccurate"""
        x, y = point
        return dot_product(self, (x, y, 1.)) < .00001

    @property
    def direction_vector(self):
        return Vector2D(self.a, self.b)

    @property
    def normal_vector(self):
        return Vector2D(-self.b, self.a)


def find_nearest_point(
        ref_point: tuple, points: List[tuple],
        distfunc=euclidean_distance) -> (int, tuple, float):
    nearest_ix = -1
    nearest_pt = None
    min_dist = float('inf')
    for ix, pt in enumerate(points):
        dist = distfunc(ref_point, pt)
        if dist < min_dist:
            nearest_ix = ix
            nearest_pt = pt
            min_dist = dist
    return nearest_ix, nearest_pt, min_dist


def test():
    pt1 = Point3D()
    pt2 = Point3D(1, 1, 1)
    euclidean_distance(pt1, pt2)
