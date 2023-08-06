#!/usr/bin/env python3
# coding: utf-8

"""
https://en.wikipedia.org/wiki/Paper_size
"""

import re
import math


def conv_mm_to_inch(val: float):
    return val / 25.4


class StandardPaperSize:
    __slots__ = ['width']
    sqrt2 = math.sqrt(2)
    base_widths = {
        ('A', 'mm'): 840.8964152537146,
        ('A', 'cm'): 84.08964152537146,
        ('A', 'inch'): 33.10615808085491,
        ('B', 'mm'): 1000.,
        ('B', 'cm'): 100.,
        ('B', 'inch'): 39.37007874015748,
        ('C', 'mm'): 917.0040432046713,
        ('C', 'cm'): 91.70040432046713,
        ('C', 'inch'): 36.102521386010686,
    }

    def __init__(self, width: float = None):
        width = width or 840.8964152537146
        self.width = width

    @property
    def length(self) -> float:
        return self.width * self.sqrt2

    def pair(self, ndigits=64) -> tuple:
        width = self.width
        length = self.width * self.sqrt2
        if ndigits == 64:
            return width, length
        return round(width, ndigits), round(length, ndigits)

    def bisect(self, repeat: int = 1):
        r = self.sqrt2 ** repeat
        return self.__class__(self.width / r)

    def __getitem__(self, n: int):
        return self.bisect(n)

    def __repr__(self):
        cn = self.__class__.__name__
        return f'{cn}({self.width})'

    def __str__(self):
        width, length = self.pair(3)
        return f'{width}x{length}'

    @classmethod
    def abc_series(cls, base_name: str = 'A', unit: str = 'mm'):
        try:
            w = cls.base_widths[base_name, unit]
        except KeyError:
            raise ValueError('unit must be "mm", "cm" or "inch"')
        return cls(w)

    @classmethod
    def a_series(cls, unit: str = 'mm'):
        return cls.abc_series('A', unit)

    @classmethod
    def b_series(cls, unit: str = 'mm'):
        return cls.abc_series('B', unit)

    @classmethod
    def c_series(cls, unit: str = 'mm'):
        return cls.abc_series('C', unit)

    @classmethod
    def from_name(cls, name: str = 'A4', unit: str = 'mm'):
        mat = re.match(r'([ABC])(0|[1-9][0-9]?)', name.upper())
        if not mat:
            msg = 'unknown name for standard paper size: "{}"'.format(name)
            raise ValueError(msg)
        a, n = mat.groups()
        return cls.abc_series(a + '0', unit)[int(n)]

    @classmethod
    def iter_abc_sizes(cls, unit: str = 'mm', ndigits=64):
        for base_name in 'ABC':
            series = cls.abc_series(base_name, unit)
            for n in range(11):
                name = base_name + str(n)
                yield name, series[n].pair(ndigits)
