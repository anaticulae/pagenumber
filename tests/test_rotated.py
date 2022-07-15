# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila

import pagenumbers.strategy.numbers


def test_rotated_master116page102():
    source = power.link(power.MASTER116_PDF)
    pages = (102, 103, 104, 105, 106, 107, 108)
    ptn = serializeraw.ptn_frompath(source, pages=pages)
    numbers = pagenumbers.strategy.numbers.determine_pagenumbers(ptn)
    assert len(numbers) == 7


def test_rotated_normal_mixed_master116page102():
    source = power.link(power.MASTER116_PDF)
    pages = utila.ranged_tuple(100, 117)
    ptn = serializeraw.ptn_frompath(source, pages=pages)
    numbers = pagenumbers.strategy.numbers.determine_pagenumbers(ptn)
    assert len(numbers) == 14
