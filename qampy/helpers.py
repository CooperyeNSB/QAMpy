# -*- coding: utf-8 -*-
#  This file is part of QAMpy.
#
#  QAMpy is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Foobar is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with QAMpy.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2018 Jochen Schröder, Mikael Mazur

from __future__ import division, print_function
import numpy as np


def cabssquared(x):
    """Calculate the absolute squared of a complex number"""
    return x.real**2 + x.imag**2


def dB2lin(x):
    """
    Convert input from dB(m) units to linear units
    """
    return 10**(x/10)


def lin2dB(x):
    """
    Convert input from linear units to dB(m)
    """
    return 10*np.log10(x)


def normalise_and_center(E):
    """
    Normalise and center the input field, by calculating the mean power for each polarisation separate and dividing by its square-root
    """
    if E.ndim > 1:
        E = E - np.mean(E, axis=-1)[:, np.newaxis]
        P = np.sqrt(np.mean(cabssquared(E), axis=-1))
        E /= P[:, np.newaxis]
    else:
        E = E.real - np.mean(E.real) + 1.j * (E.imag-np.mean(E.imag))
        P = np.sqrt(np.mean(cabssquared(E)))
        E /= P
    return E


def dump_edges(E, N):
    """
    Remove N samples from the front and end of the input field.
    """
    if E.ndim > 1:
        return E[:,N:-N]
    else:
        return E[N:-N]

def set_mid_point(E,mid_pos=0):
    """
    Move the (1-pol) signal's mid-position to given value
    """
    if np.iscomplexobj(E):
        ori_mid_pos = (E.real.max() + E.real.min())/2 + 1j*(E.imag.max() + E.imag.min())/2
        return E - ori_mid_pos + mid_pos
    if not np.iscomplexobj(E):
        ori_mid_pos = (E.max() + E.min())/2
        return E - ori_mid_pos + mid_pos


def rescale_signal(E,swing=1):
    """
    Rescale the (1-pol) signal to (-swing, swing).
    """
    if np.iscomplexobj(E):
        scale_factor = np.maximum(abs(E.real).max(), abs(E.imag).max())
        return E / scale_factor * swing

    if not np.iscomplexobj(E):
        scale_factor = abs(E).max()
        return E / scale_factor * swing

def set_mid_and_resale(E,mid_pos=0,swing=1):
    """
    Change (1-pol) signal mid-position to given value and rescale the real signal to (-swing, swing).
    """
    sig_out = set_mid_point(E, mid_pos)
    sig_out = rescale_signal(sig_out, swing)

    return sig_out
