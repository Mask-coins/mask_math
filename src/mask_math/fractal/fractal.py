from __future__ import annotations

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def complex_field_symmetry(
        draw_height: int=2,
        draw_width: int=2,
        display_range=complex(2, 2),
        center=complex(2,1) ) -> np.ndarray:
    x_axis = np.arange(-draw_width,draw_width+1,1, dtype=complex).reshape((1,2*draw_width+1))
    x_axis = x_axis*(display_range.real/draw_width)
    y_axis = -1.j * np.arange(-draw_height,draw_height+1,1, dtype=complex).reshape((2*draw_height+1,1))
    y_axis = y_axis*(display_range.imag/draw_height)
    return x_axis+y_axis + center


def complex_field_square(draw_range:int = 2, display_range:float = 1, center=complex(0,0)):
    return complex_field_symmetry(
        draw_height=draw_range,
        draw_width=draw_range,
        display_range=complex(display_range,display_range),
        center=center)


class Mandelbrot(object):
    def __init__(self,draw_range=100, draw_height=None, draw_width=None, display_range=2, center=complex(0,0), power:int|float=2):
        if draw_height is not None and draw_width is not None and isinstance(display_range, complex) and display_range.imag > 0:
            self.c = complex_field_symmetry(
                draw_height=draw_height,
                draw_width=draw_width,
                display_range=display_range,
                center=center
            )
        else:
            self.c = complex_field_square(
                draw_range=draw_range,
                display_range=display_range,
                center=center
            )
        self._z = 0 * self.c
        self._count = np.abs(0 * self.c)
        self._power = power
        self.itr = 0

    def calc_z(self):
        if self._power == 2 or self._power == 2.0:
            self._z = self._z * self._z + self.c
        else:
            self._z = np.power(self._z, self._power) + self.c

    def calc_count(self):
        self._count = self._count + np.where(np.abs(self._z) < 2, 1, 0)

    def calc(self, itr=1000):
        for _ in range(itr):
            self.itr += 1
            self.calc_z()
            self.calc_count()

    @property
    def z(self):
        return self.z

    @property
    def abs_z_cleaned(self):
        return np.abs(np.where(np.abs(self._z) < 2, np.abs(self._z), 2))

    @property
    def count(self):
        return self._count

    def plot_count(self, file_path, cmap:str= "copper"):
        """
        The numbers of calculation times arranged in two dimensions are output as an image .
        :param file_path:
        :param cmap: A color map name in matplotlib .
        :return:
        """
        plot_real_number_field(self.count, file_path, cmap)

    def plot_abs_z(self, file_path, cmap:str= "copper"):
        """
        The numbers of abs(z) arranged in two dimensions are output as an image .
        Note: Numbers above 2 are replaced by 2.
        :param file_path:
        :param cmap: A color map name in matplotlib .
        :return:
        """
        plot_real_number_field(self.abs_z_cleaned, file_path, cmap)

    def plot_count_and_abs_z(self, file_path, cmap:str= "copper"):
        """
        :param file_path:
        :param cmap:
        :return:
        """
        f = self.count * self.abs_z_cleaned
        plot_real_number_field(f, file_path, cmap)


def plot_real_number_field(surf, file_path, cmap:str= "copper"):
    surf1 = (1/np.max(surf))*surf
    cm = plt.get_cmap(cmap)
    colored_image = cm(surf1)
    Image.fromarray((colored_image[:, :, :3] * 255).astype(np.uint8)).save(file_path)









