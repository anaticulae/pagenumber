# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def pagenumbers_fill(pagenumbers: list, pdflength: int) -> dict:
    result = {page.pdfpage: page.detected for page in pagenumbers}
    try:
        result = fill_pages_magic(result, pdflength=pdflength)
    except ValueError as error:
        # backup strategy
        utila.error(f'use page fill backup strategy: {error}')
        result = fill_pages(result, pdflength=pdflength)
    return result


def fill_pages(pages: dict, pdflength: int) -> dict:
    """\
    >>> fill_pages({0: "I", 1: "II", '3': "IV", 4: "V", '5': "1", '6': "2", '8': "4"}, pdflength=10)
    {0: 'I', 1: 'II', 2: '[3]', 3: 'IV', 4: 'V', 5: '1', 6: '2', 7: '[8]', 8: '4', 9: '[10]'}
    """
    pages = {int(key): value for key, value in pages.items()}
    for page in range(pdflength):
        if page in pages:
            continue
        # expected page
        pages[page] = f'[{page+1}]'
    # sort dict by page number
    pages = {key: pages[key] for key in sorted(pages.keys())}
    return pages


def fill_pages_magic(pages: dict, pdflength: int) -> dict:  # pylint:disable=R1260
    """Fill expected page number due look right and left neighbor page numbers.

    >>> fill_pages_magic({0: "I", 1: "II", '3': "IV", 4: "V", '5': "1", '6': "2", '8': "4"}, pdflength=10)
    {0: 'I', 1: 'II', 2: '[III]', 3: 'IV', 4: 'V', 5: '1', 6: '2', 7: '[3]', 8: '4', 9: '[5]'}
    >>> fill_pages_magic(pages={}, pdflength=5)
    Traceback (most recent call last):
        ...
    ValueError: no progress: {0: None, 1: None, 2: None, 3: None, 4: None}, 5
    >>> fill_pages_magic({2: "II", 3: "IV", 5: "VI", 7: "2", 8: "3"}, pdflength=10)
    {0: '[0]', 1: '[I]', 2: 'II', 3: 'IV', 4: '[V]', 5: 'VI', 6: '[1]', 7: '2', 8: '3', 9: '[4]'}
    """
    pages = {int(key): value for key, value in pages.items()}
    for page in range(pdflength):
        if page in pages:
            continue
        # expected page
        pages[page] = None
    # sort dict by page number
    pages = {key: pages[key] for key in sorted(pages.keys())}
    nones = [pdfpage for pdfpage, value in pages.items() if value is None]
    while nones:
        # go from right to left pdf pages and use the right before the
        # left page for replacing.
        for pdfpage in reversed(nones):
            if pdfpage + 1 < pdflength:
                after = pages[pdfpage + 1]
                if after is not None:
                    after = str(after).strip('[]')
                    try:
                        current = utila.pagenumber_minus(after)
                    except (ValueError, KeyError):
                        current = utila.arabic(after) - 1
                    pages[pdfpage] = f'[{current}]'
                    continue
            if pdfpage > 0:
                before = pages[pdfpage - 1]
                if before is not None:
                    before = str(before).strip('[]')
                    current = utila.pagenumber_plus(before)
                    pages[pdfpage] = f'[{current}]'
                    continue
        # update nones
        new = [pdfpage for pdfpage, value in pages.items() if value is None]
        if nones == new:
            raise ValueError(f'no progress: {pages}, {pdflength}')
        nones = new
    return pages
