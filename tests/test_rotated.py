# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila
import utilatest

import pagenumber.strategy.numbers


@utilatest.requires(power.MASTER116_PDF)
def test_rotated_master116page102():
    source = power.link(power.MASTER116_PDF)
    pages = (102, 103, 104, 105, 106, 107, 108)
    ptn = serializeraw.ptn_frompath(source, pages=pages)
    numbers = pagenumber.strategy.numbers.determine_pagenumbers(ptn)
    assert len(numbers) == 7


@utilatest.requires(power.MASTER116_PDF)
def test_rotated_normal_mixed_master116page102():
    source = power.link(power.MASTER116_PDF)
    pages = utila.rtuple(100, 117)
    ptn = serializeraw.ptn_frompath(source, pages=pages)
    numbers = pagenumber.strategy.numbers.determine_pagenumbers(ptn)
    assert len(numbers) == 14
