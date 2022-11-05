# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Page Numbers Extraction Step
============================

Start working on footer extractor.

Required resources:

    # PageSize
    # HorizontalLines
    # Text annotated with location

Required API:

    # before/ after method to determine items
"""

import serializeraw
import texmex

import pagenumber.strategy.numbers

VALID = texmex.TextState.VISIBLE | texmex.TextState.PAGENUMBER


def work(
    text: str,
    textpositions: str,
    pages: tuple = None,
) -> str:
    navigators = serializeraw.ptn_fromfile(
        text=text,
        textpositions=textpositions,
        pages=pages,
        state=VALID,
    )
    detected = pagenumber.strategy.numbers.determine_pagenumbers(navigators)
    detected_dumped = serializeraw.dump_pagenumbers(detected)
    return detected_dumped
