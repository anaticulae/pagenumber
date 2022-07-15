#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila

import pagenumbers

DESCRIPTION = 'TODO'

WORKPLAN = [
    utila.create_step(
        'result',
        inputs=[
            utila.ResultFile(producer='rawmaker', name='text_text'),
            utila.ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('pagenumbers', 'magic'),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=pagenumbers.ROOT,
        featurepackage='pagenumbers.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=pagenumbers.PROCESS,
            pages=True,
            rename=rename,
            version=pagenumbers.__version__,
        ),
    )


def rename(path):
    if not isinstance(path, str):
        path = [rename(item) for item in path]
        return path
    path = utila.rreplace(
        path,
        pattern='pagenumbers__result_pagenumbers',
        replace='groupme__pagenumbers_pagenumbers',
    )
    path = utila.rreplace(
        path,
        pattern='pagenumbers__result_magic',
        replace='groupme__pagenumbers_magic',
    )
    return path
