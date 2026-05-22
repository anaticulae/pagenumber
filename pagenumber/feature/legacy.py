# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo


def work(xresult: str, xmagic: str) -> tuple[str, str]:
    xresult = utilo.file_read(xresult)
    xmagic = utilo.file_read(xmagic)
    return xresult, xmagic
