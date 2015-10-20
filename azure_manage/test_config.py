# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

from .config import Config


def test_Config():
    c = Config('a: a')
    assert len(c) == 1
    assert 'a' in c
