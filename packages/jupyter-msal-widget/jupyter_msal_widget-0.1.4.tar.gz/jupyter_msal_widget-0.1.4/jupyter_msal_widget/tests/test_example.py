#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Felipe Oucharski.
# Distributed under the terms of the Modified BSD License.

import pytest

from ..widget import MsalWidget


def test_example_creation_blank():
    w = MsalWidget()
    assert w.signed_in == False
