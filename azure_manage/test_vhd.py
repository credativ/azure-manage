# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

from uuid import UUID

from .vhd import VHDFooter


def test_VHDFooter():
    assert VHDFooter._struct.size == 512


def test_VHDFooter_pack():
    p = VHDFooter(0x100010001000000, UUID(int=0), 0x10000000)
    assert len(p.pack()) == 512
