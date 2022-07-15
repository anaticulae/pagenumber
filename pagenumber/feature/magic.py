# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utila

import pagenumber.strategy.magic


def work(results: str, pages: tuple = None) -> str:
    pagenumbers = serializeraw.load_pagenumbers(
        results,
        pages=pages,
    )
    improved = dict()
    if pagenumbers:
        improved = pagenumber.strategy.magic.pagenumbers_fill(
            pagenumbers=pagenumbers,
            pdflength=len(pagenumbers),
        )
    improved_dumped = utila.yaml_dump(improved)
    return improved_dumped
