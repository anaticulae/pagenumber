# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw
import texmex
import utilatest

DOCU007 = power.link(power.DOCU007_PDF)
SIMPLE_PAGESIZE = iamraw.path.sizeandborder(DOCU007)
SIMPLE_HORIZONTAL = iamraw.path.horizontals(DOCU007)
SIMPLE_TEXT_POSITION = iamraw.path.textposition(DOCU007)
SIMPLE_TEXT = iamraw.path.text(DOCU007)


@pytest.fixture
def simple():
    utilatest.fixture_requires(power.DOCU007_PDF)
    pagesize = serializeraw.load_pageborders(SIMPLE_PAGESIZE)
    horizontals = serializeraw.load_horizontals(SIMPLE_HORIZONTAL)
    position = serializeraw.load_textpositions(SIMPLE_TEXT_POSITION)
    document = serializeraw.load_document(SIMPLE_TEXT)

    assert pagesize
    assert horizontals
    assert position

    navigator = texmex.create_ptns(
        text=document,
        textpositions=position,
    )
    return navigator, horizontals


@pytest.fixture
def simple_navigator(simple):  #pylint:disable=W0621
    navigator, _ = simple
    return navigator
