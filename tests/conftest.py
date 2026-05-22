# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import resinf
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

from tests.fixtures.simple import simple  # pylint:disable=W0611
from tests.fixtures.simple import simple_navigator  # pylint:disable=W0611

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

RESOURCES = [
    resinf.todo(
        hoverpower.DOCU007_PDF,
        tablero=True,
        pagenumber=True,
        footnote=True,
        groupme='--content',
        rawmaker=gennex.CONFIG,
    ),
    hoverpower.BACHELOR045A_PDF,
    hoverpower.BACHELOR051_PDF,
    hoverpower.BACHELOR085_PDF,
    hoverpower.BACHELOR111_PDF,
    hoverpower.DISS148_PDF,
    hoverpower.DISS170B_PDF,
    hoverpower.DISS218_PDF,
    hoverpower.DISS287_PDF,
    hoverpower.DISS406_PDF,
    hoverpower.DISS480_PDF,
    hoverpower.DOCU027_PDF,
    hoverpower.HC_DISS128,
    hoverpower.HC_DISS148,
    hoverpower.HC_DISS166,
    hoverpower.HC_DISS171,
    hoverpower.HC_DISS193,
    hoverpower.HOME007_PDF,
    hoverpower.HOME009B_PDF,
    hoverpower.HOME015_PDF,
    hoverpower.HOME016A_PDF,
    hoverpower.HOME017C_PDF,
    hoverpower.HOME019B_PDF,
    hoverpower.HOME019_PDF,
    hoverpower.HOME021B_PDF,
    hoverpower.HOME022B_PDF,
    hoverpower.HOME022_PDF,
    hoverpower.MASTER049_PDF,
    hoverpower.MASTER072_PDF,
    hoverpower.MASTER091A_PDF,
    hoverpower.MASTER110_PDF,
    hoverpower.MASTER116_PDF,
    hoverpower.MASTER127_PDF,
    hoverpower.PAPER14B_PDF,
    hoverpower.PAPER18_PDF,
    hoverpower.TECH024_PDF,
]

WORKER = utilotest.worker_count(5, onci=len(RESOURCES))


def pytest_sessionstart(session):  # pylint:disable=W0613
    hoverpower.run()


CONFIG = gennex.CONFIG.strip()
RAWMAKER = f'--text --fonts --border --line --horizontals {CONFIG}'
# disable oneline extraction
ONELINE = None


def extract(resources):
    gennex.extract(
        resources,
        rawmaker=RAWMAKER,
        oneline=ONELINE,
        worker=WORKER,
    )


RESOURCES_NOTITLE = [
    hoverpower.DOCU027_PDF,
]


def extract_notitle(resources):
    gennex.extract_removepages(
        resources,
        rawmaker=RAWMAKER,
        oneline=ONELINE,
        removepages='0',
        folder='notitle',
        pages='0:10',
        worker=len(RESOURCES_NOTITLE),
    )
