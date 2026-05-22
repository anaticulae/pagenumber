#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utilo

import pagenumber

DESCRIPTION = 'TODO'

WORKPLAN = [
    utilo.create_step(
        'result',
        inputs=[
            utilo.ResultFile(producer='rawmaker', name='text_text'),
            utilo.ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('result',),
    ),
    utilo.create_step(
        'magic',
        inputs=[
            utilo.ResultFile(producer='pagenumber', name='result_result'),
        ],
        output=('magic',),
    ),
    utilo.create_step(
        'legacy',
        inputs=[
            utilo.ResultFile(producer='pagenumber', name='result_result'),
            utilo.ResultFile(producer='pagenumber', name='magic_magic'),
        ],
        output=('pagenumber', 'magic'),
    ),
]


def main():
    utilo.featurepack(
        workplan=WORKPLAN,
        root=pagenumber.ROOT,
        featurepackage='pagenumber.feature',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=pagenumber.PROCESS,
            pages=True,
            rename=rename,
            version=pagenumber.__version__,
        ),
    )


def rename(path):
    if not isinstance(path, str):
        path = [rename(item) for item in path]
        return path
    path = utilo.rreplace(
        path,
        pattern='pagenumber__legacy_pagenumber',
        replace='groupme__pagenumbers_pagenumbers',
    )
    path = utilo.rreplace(
        path,
        pattern='pagenumber__legacy_magic',
        replace='groupme__pagenumbers_magic',
    )
    return path
