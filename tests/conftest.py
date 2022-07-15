# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import genex.config
import power
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

import pagenumber
from tests.fixtures.simple import simple  # pylint:disable=W0611
from tests.fixtures.simple import simple_navigator  # pylint:disable=W0611

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = pagenumber.PROCESS

RESOURCES = [
    (power.DISS218_PDF, '0:100'),
    (power.DISS287_PDF, '0:100'),
    (power.DISS406_PDF, '0:75,100:150'),
    (power.MASTER116_PDF, '50:117'),
    genex.todo(power.DOCU007_PDF, tablero=True, rawmaker=genex.config.CONFIG),
    power.BACHELOR085_PDF,
    power.BACHELOR111_PDF,
    power.DISS148_PDF,
    power.DISS170B_PDF,
    power.DISS480_PDF,
    power.DOCU027_PDF,
    power.HC_DISS128,
    power.HC_DISS148,
    power.HC_DISS166,
    power.HC_DISS171,
    power.HC_DISS193,
    power.HOME007_PDF,
    power.HOME009B_PDF,
    power.MASTER049_PDF,
    power.MASTER072_PDF,
    power.MASTER091A_PDF,
    power.MASTER110_PDF,
    power.MASTER127_PDF,
    power.PAPER14B_PDF,
    power.PAPER18_PDF,
    power.TECH024_PDF,
]

WORKER = 5


def pytest_sessionstart(session):  # pylint:disable=W0613
    power.run()


CONFIG = genex.config.CONFIG.strip()
RAWMAKER = f'--text --fonts --border --line --horizontals {CONFIG}'
# disable oneline extraction
ONELINE = None


def extract(resources):
    genex.extract(
        resources,
        rawmaker=RAWMAKER,
        oneline=ONELINE,
        worker=WORKER,
    )


RESOURCES_NOTITLE = [
    power.DOCU027_PDF,
]


def extract_notitle(resources):
    genex.extract_removepages(
        resources,
        rawmaker=RAWMAKER,
        oneline=ONELINE,
        removepages='0',
        folder='notitle',
        pages='0:10',
        worker=1,
    )
