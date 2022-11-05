# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import pytest
import serializeraw
import utila
import utilatest

import pagenumber
import tests

ARCHIVE = utila.join(pagenumber.ROOT, 'tests/expected', exist=True)

PAGENUMBERS = utilatest.test_resources(tests.conftest.RESOURCES)


@utilatest.nightly
@pytest.mark.parametrize('source', PAGENUMBERS)
def test_validate(source, mp, td):
    Evaluate(
        source=source,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

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
        result: str = utila.NEWLINE.join(collected.values()).rstrip()
        return result


@utilatest.requires(power.MASTER049_PDF)
def test_pagenumber_cleanup_pagenumber(testdir, mp):
    """Ensure that pagenumber->cleanup->pagenumber does not removes pagenumber.

    Before this patch pagenumber does not load hidden pagenumber out of the
    first step correctly.
    """
    source = power.link(power.MASTER049_PDF)
    utila.copy_content(
        src=source,
        dst=testdir.tmpdir,
        unlock=True,
    )
    cmd = f'-i {testdir.tmpdir} -o {testdir.tmpdir}'
    tests.run(cmd=cmd, mp=mp)
    pages = serializeraw.load_pagenumbers(testdir.tmpdir)
    assert pages
    count = len(pages)
    utila.cache_clear()
    cmd = f'cleanup -i {testdir.tmpdir} -o {testdir.tmpdir} --select=pagenumber'
    utila.run(cmd)
    cmd = f'-i {testdir.tmpdir} -o {testdir.tmpdir}'
    tests.run(cmd=cmd, mp=mp)
    pages = serializeraw.load_pagenumbers(testdir.tmpdir)
    assert pages
    after = len(pages)
    assert count == after
