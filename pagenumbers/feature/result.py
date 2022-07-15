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

import typing

import serializeraw
import utila

import pagenumbers.strategy.magic
import pagenumbers.strategy.numbers


def work(
    text: str,
    textpositions: str,
    pages: tuple = None,
) -> typing.Tuple[str, str]:
    utila.call('numbers')
    navigators = serializeraw.ptn_fromfile(
        text=text,
        textpositions=textpositions,
        pages=pages,
    )
    detected = pagenumbers.strategy.numbers.determine_pagenumbers(navigators)
    improved = pagenumbers.strategy.magic.pagenumbers_fill(
        pagenumbers=detected,
        pdflength=navigators[-1].page if navigators else 256,
    )
    detected_dumped = serializeraw.dump_pagenumbers(detected)
    improved_dumped = utila.yaml_dump(improved)
    return detected_dumped, improved_dumped
