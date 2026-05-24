# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import pagenumber
import tests
import tests.conftest

ARCHIVE = utilo.join(pagenumber.ROOT, 'tests/expected', exist=True)

PAGENUMBERS = utilotest.test_resources(tests.conftest.RESOURCES)


@utilotest.nightly
@pytest.mark.parametrize('source', PAGENUMBERS)
def test_validate(source, mp, td):
    Evaluate(
        source=source,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilotest.BaseLiner):

    def __init__(self, source, workdir, mp):
        super().__init__(
            program=functools.partial(
                tests.run,
                mp=mp,
            ),
            step='',
            source=source,
            pages=':',
            workdir=workdir,
            archive=ARCHIVE,
            loader=serializeraw.load_pagenumbers,
        )

    def raw(self, value) -> str:
        if not value:
            return ''
        if isinstance(value, tuple):
            # left right, or multiple pages positions
            value = value[0] + value[1]
        assert isinstance(value, list), f' page detection type {type(value)}'
        maxpage = value[-1].pdfpage
        collected = {pdfpage: '' for pdfpage in range(maxpage)}
        for item in value:
            collected[item.pdfpage] = str(item.detected)
        result: str = utilo.NEWLINE.join(collected.values()).rstrip()
        return result


@utilotest.requires(hoverpower.MASTER049_PDF)
def test_pagenumber_cleanup_pagenumber(td, mp):
    """Ensure that pagenumber->cleanup->pagenumber does not removes pagenumber.

    Before this patch pagenumber does not load hidden pagenumber out of the
    first step correctly.
    """
    source = hoverpower.link(hoverpower.MASTER049_PDF)
    utilo.copy_content(
        src=source,
        dst=td.tmpdir,
        unlock=True,
    )
    cmd = f'-i {td.tmpdir} -o {td.tmpdir}'
    tests.run(cmd=cmd, mp=mp)
    pages = serializeraw.load_pagenumbers(td.tmpdir)
    assert pages
    count = len(pages)
    utilo.cache_clear()
    cmd = f'cleanup -i {td.tmpdir} -o {td.tmpdir} --select=pagenumber'
    utilo.run(cmd)
    cmd = f'-i {td.tmpdir} -o {td.tmpdir}'
    tests.run(cmd=cmd, mp=mp)
    pages = serializeraw.load_pagenumbers(td.tmpdir)
    assert pages
    after = len(pages)
    assert count == after
