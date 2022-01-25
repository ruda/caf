# encoding: utf-8
#
# Copyright © 2018, 2022 Rudá Moura <ruda.moura@gmail.com>
#
# Permission to use, copy, modify, distribute, and sell this software and its
# documentation for any purpose is hereby granted without fee, provided that
# the above copyright notice appear in all copies and that both that
# copyright notice and this permission notice appear in supporting
# documentation.  No representations are made about the suitability of this
# software for any purpose.  It is provided "as is" without express or
# implied warranty.

"""Encode or decode chunks of Core Audio Format (CAF) files.
"""

from .chunk import Reader, Writer
from .codec import Decoder, Encoder


def open(f, mode=None):
    """Open file to encode or decode CAF."""
    if mode is None:
        if hasattr(f, 'mode'):
            mode = f.mode
        else:
            mode = 'rb'
    if mode in ('r', 'rb'):
        return Decoder(f)
    elif mode in ('w', 'wb'):
        return Encoder(f)
    else:
        raise IOError("mode must be 'r', 'rb', 'w', or 'wb'")
