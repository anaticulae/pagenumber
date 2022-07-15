# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import configo
import elements
import elements.pagenumber
import iamraw
import texmex
import utila

# Header in the range of 0% till 20%
TOP_BORDER = configo.HV_PERCENT_PLUS(default=20)
# TODO: Think about scaling this value depending on result
# Footer is in range of 80% till 100%
BOTTOM_BORDER = configo.HV_PERCENT_PLUS(default=80)

BOTTOM_DIFFERENCE_MAX = configo.HV_FLOAT_PLUS(default=20.0)
# page number is not very big
BOTTOM_AREA_MAX = configo.HV_FLOAT_PLUS(default=2500.0)

PAGE_ELEMENTS_MIN = configo.HV_INT_PLUS(default=4)


def determine_pagenumbers(navigators) -> list:
    numbers = []
    rotated, normal = utila.partition(iswidepage, navigators)
    detected = header(normal) + footer(normal)
    if detected:
        numbers.extend(detected)
    if rotated:
        # do not rotate page cause some pages are wide page but not rotated
        detected_rotated = header(rotated) + footer(rotated)
        # rotate left ro determine rotated page numbers
        rotated = [texmex.rotate_left(page) for page in rotated]
        detected_rotated_roated = header(rotated) + footer(rotated)
        # TODO: USE BETTER DECIDER?!
        if len(detected_rotated) > len(detected_rotated_roated):
            numbers.extend(detected_rotated)
        else:
            numbers.extend(detected_rotated_roated)
    return pagenumbers(numbers)


def header(
    navigators,
    *,
    numbers_only: bool = True,
    remove_empty: bool = True,
) -> list:
    collected = [(page.page, page.before(TOP_BORDER)) for page in navigators]
    common = valid_content(
        collected,
        numbers_only=numbers_only,
        remove_empty=remove_empty,
    )
    return common


def footer(
    navigators,
    *,
    numbers_only: bool = True,
    remove_empty: bool = True,
) -> list:
    """Detect similar elements in footer area which are duplicated on
    different pages.

    Args:
        navigators(list): list of text navgiators
        numbers_only(bool): if True, remove all non numeric/romanic elements
        remove_empty(bool): remove empty elements, e.g. whitespaces
    Returns:
        A list of clustered page footer content which are expected of
        beeing the page numbers.
    """
    collected = [(page.page, page.after(BOTTOM_BORDER)) for page in navigators]
    common = valid_content(
        collected,
        numbers_only=numbers_only,
        remove_empty=remove_empty,
    )
    return common


def valid_content(
    navigators,
    max_area: float = BOTTOM_AREA_MAX,
    max_difference: float = BOTTOM_DIFFERENCE_MAX,
    min_elements: int = PAGE_ELEMENTS_MIN,
    numbers_only: bool = True,
    remove_empty: bool = True,
):
    """Detect similar elements which are duplicated on different pages."""
    filtered = []
    for pagenumber, footercontent in navigators:
        footercontent = split_ifrequired(footercontent)
        pagecontent = search_pagenumbers(
            pagenumber,
            footercontent,
            area_max=max_area,
            numbers_only=numbers_only,
            remove_empty=remove_empty,
        )
        if len(pagecontent) > POTENTIAL_PAGE_NUMBERS_PER_PER:
            # page with a lot of numbers
            utila.error('too many potential page numbers on page: '
                        f'{pagenumber} len: {len(pagecontent)}')
            continue
        filtered.append(pagecontent)
    common = utila.common_items(
        filtered,
        max_difference=max_difference,
        min_elements=min_elements,
    )
    return common


def search_pagenumbers(
    pagenumber,
    footercontent,
    area_max: float,
    numbers_only: bool = True,
    remove_empty: bool = True,
) -> list:
    pagecontent = []
    for item in footercontent:
        text = item.text.strip()
        if utila.rectangle_size(item.bounding) > area_max:
            # ignore to big items
            continue
        if remove_empty and not text:
            # filter empty items
            continue
        if numbers_only and not elements.ispagenumber(text):
            # remove non numeric items
            continue
        # support -1-, -2-, ...
        clean_number = text.replace('-', '', 2).strip()
        # 32/54
        clean_number = clean_number.split('/')[0]
        # remove gaps: 10 4
        clean_number = clean_number.replace(' ', '')
        # Page 6 of 16
        if matched := COMPLEX_PAGENUMBER.match(clean_number):
            clean_number = matched[3] or matched[3 + 4]
        # TODO: DELIVER RAW DATA FOR FOOTER PAGES STRATEGY DETECTION
        item = (item.bounding, clean_number, pagenumber)
        pagecontent.append(item)
    return pagecontent


COMPLEX_PAGENUMBER = elements.pagenumber.COMPLEX_PAGENUMBER

POTENTIAL_PAGE_NUMBERS_PER_PER = configo.HV_INT_PLUS(default=7)
# ( ) is required to avoid losing white space, because there are required
# to splitby_count correctly.
LONGWHITESPACE = utila.compiles(r'([ ]{4,10})')


def split_ifrequired(content) -> list:
    """Improve bad printed pdf.

    Zugverkehrsleitende und ihre Aufgaben       3
    """
    if not content:
        return content
    result = []
    for item in content:
        splitted = LONGWHITESPACE.split(item.text)
        if len(splitted) == 1:
            result.append(item)
            continue
        splitted = [len(item) for item in splitted]
        new = texmex.splitby_count(item, counts=splitted)
        # remove empty string
        new = [item for item in new if item.text.strip()]
        result.extend(new)
    return result


def iswidepage(navigator) -> bool:
    return navigator.width > navigator.height


def isrightpage(pdf_pagenumber: int) -> bool:
    """What pdf page is the left side?

    The first page is the right page?
    """
    # TODO: REQUIRE SMART ALTERNATIVE
    if utila.iseven(pdf_pagenumber):
        return True
    return False


Cluster = typing.List[typing.Tuple[iamraw.BoundingBox, str]]


def pagenumbers(clusters: typing.List[Cluster]) -> list:
    """Determine pagenumbers out of list of cluster

    Two scenarios are possible:

    * alternating left and right page numbers
    * page numbers are only on one possition

    Args:
        clusters: List of cluster -> List[List[(boundingbox, content)]]
    Returns:
        singlepage or (left, right)
    """
    result = []
    for cluster in clusters:
        if multiple_number_perpage(cluster):
            continue
        if not valid_cluster(cluster):
            continue
        if already_done(cluster, result):
            continue
        for _, (bounding, content, pdfpage) in cluster:
            content = str(content)
            # remove a single gap
            content = content.replace(' ', '', 1)
            if not elements.ispagenumber(content):
                continue
            try:
                content: int = int(content)
            except ValueError:
                # roman number
                pass
            # save number as tuple of pdf_page and detected page
            item = iamraw.PageNumber(
                pdfpage=pdfpage,
                bounding=bounding,
                detected=content,
                direction=determine_orientation(pdfpage, clusters),
            )
            result.append(item)
    # sort by pdfpage number
    result = sorted(result)
    return result


DUPLICATED_PAGE_NUMBER_MAX = configo.HV_PERCENT_PLUS(default=75)


def already_done(cluster, result) -> bool:
    """Check that page number is not detected twice on the same page.

    This can happen when headline number is also detected as a page
    number.

    See: master049
    """
    pages = set(item.pdfpage for item in result)
    dones = []
    for item in cluster:
        pdfpage = item[1][2]
        if pdfpage not in pages:
            continue
        dones.append(pdfpage)
    if not dones:
        return False
    rate = utila.rate_rel(len(dones), len(cluster))
    if rate > DUPLICATED_PAGE_NUMBER_MAX:
        utila.debug(f'multiple page number cluster on page: {dones}')
        return True
    return False


def determine_orientation(pdfpage, clusters) -> iamraw.PageNumberOrientation:
    multiple = morethanone(clusters)
    if not multiple:
        return iamraw.PageNumberOrientation.NORMAL
    if isrightpage(pdfpage):
        return iamraw.PageNumberOrientation.RIGHT
    return iamraw.PageNumberOrientation.LEFT


MORETHANONE_DIFF_MAX = configo.HV_FLOAT_PLUS(default=100.0)


def morethanone(clusters) -> bool:
    """Determine vector to position of detected page numbers.

    If this maxdistance/diff is higher than a threshold, we have left
    and right page numbers.
    """
    collected = []
    for cluster in clusters:
        for _, item in cluster:
            centered = utila.rectangle_center(item[0])
            length = utila.length(*(0, 0, centered[0], centered[1]))
            collected.append(length)
    collected = utila.make_unique(collected)
    if not collected:
        return False
    mins, maxs = utila.mins(collected), utila.maxs(collected)
    diff = maxs - mins
    result = diff > MORETHANONE_DIFF_MAX
    return result


def multiple_number_perpage(cluster) -> bool:
    """More than one number is detected as page number. Skip this cluster.

    TODO: Try to merge items to other cluster!
    """
    pdfpages = [page for page, _ in cluster]
    if len(pdfpages) != len(set(pdfpages)):
        return True
    return False


def valid_cluster(cluster) -> bool:
    pages = []
    for item in cluster:
        number = item[1][1]
        pages.append(parse_pagenumber(number))
    # pages = utila.notnone(pages)
    # diff=2 to support left right page numbers
    grouped = utila.groupby_diff(utila.notnone(pages), maxdiff=5)
    if len(grouped) <= 2:
        return True
    if len(pages) <= 5:
        # cluster too small
        return False
    notnone = utila.notnone(pages)
    if sorted(notnone) == notnone:
        return True
    return False


def parse_pagenumber(number: str) -> int:
    if utila.isarabic(number):
        return int(number)
    # if utila.isroman(number):
    #     return utila.arabic(number)
    return None
