# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Extract footer out of document."""

import typing

import iamraw
import power
import pytest
import serializeraw
import utila

import pagenumbers.strategy.numbers


def test_simple_example(simple):
    navigator, horizontals = simple
    assert len(horizontals) == 1  # first page contains horizontals
    assert len(navigator) == 7


def test_footer_simple(simple):
    navigator, _ = simple
    result = pagenumbers.strategy.numbers.footer(navigator)
    # cluster with page numbers
    assert len(result) == 1


def test_header_simple(simple):
    navigator, _ = simple
    result = pagenumbers.strategy.numbers.header(navigator)
    assert not result


def test_footer_docu027():
    source = power.link(power.DOCU027_PDF)
    navigators = serializeraw.create_pagetextnavigators_frompath(source)
    result = pagenumbers.strategy.numbers.footer(
        navigators,
        numbers_only=False,
    )
    # cluster with page numbers
    # 2 Pages and some header text lines
    assert len(result) == 3, utila.log_raw(result)


def test_header_docu027():
    source = power.link(power.DOCU027_PDF)
    navigators = serializeraw.create_pagetextnavigators_frompath(source)
    result = pagenumbers.strategy.numbers.footer(navigators)
    # Example:
    # (5,
    # (BoundingBox(x_bottom=72.00, y_bottom=746.33, x_top=336.99, y_top=758.84),
    # 'The RestructuredText Book Documentation, Release 0.1'))
    # 2 lines of header, one for the left and one for the right page/side
    assert len(result) == 2, utila.log_raw(result)


def test_pagenumbers_docu027():
    source = power.link(power.DOCU027_PDF)
    navigators = serializeraw.create_pagetextnavigators_frompath(source)
    result = pagenumbers.strategy.numbers.footer(navigators)
    expected = ['i', 'ii'] + utila.ranged_list(start=1, end=24)
    numbers = pagenumbers.strategy.numbers.pagenumbers(result)
    # yapf:disable
    assert any(item for item in numbers if item.direction == iamraw.PageNumberOrientation.LEFT)
    assert any(item for item in numbers if item.direction == iamraw.PageNumberOrientation.RIGHT)
    # yapf:enable
    # left and right page
    assert len(numbers) == 25
    detected = [item.detected for item in numbers]
    assert detected == expected


def test_pagenumbers_simple(simple_navigator):
    result = pagenumbers.strategy.numbers.footer(simple_navigator)
    # single page
    numbers = pagenumbers.strategy.numbers.pagenumbers(result)
    assert isinstance(numbers, typing.Iterable), numbers
    assert numbers


@pytest.fixture
def pagenumbers_simple(simple_navigator):
    result = pagenumbers.strategy.numbers.footer(simple_navigator)
    # single page
    numbers = pagenumbers.strategy.numbers.pagenumbers(result)
    assert isinstance(numbers, typing.Iterable), numbers
    assert numbers
    return numbers


def test_numbers_docu027_without_title():
    """Ensure to extract correct pdf page on document which starts with
    empty page.

    Before this patch, the pdfpages started with zero instead of one.
    """
    source = power.link(power.DOCU027_PDF, folder='notitle')
    navigator = serializeraw.create_pagetextnavigators_frompath(source)
    numbers = pagenumbers.strategy.numbers.determine_pagenumbers(navigator)
    numbers = sorted(numbers)
    expected_pdfpages = utila.ranged_list(1, 26)
    current = [item[0] for item in numbers]
    assert current == expected_pdfpages, str(current)
