#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila

import pagenumber

DESCRIPTION = 'TODO'

WORKPLAN = [
    utila.create_step(
        'result',
        inputs=[
            utila.ResultFile(producer='rawmaker', name='text_text'),
            utila.ResultFile(producer='rawmaker', name='text_positions'),
        ],
        output=('result',),
    ),
    utila.create_step(
        'magic',
        inputs=[
            utila.ResultFile(producer='pagenumber', name='result_result'),
        ],
        output=('magic',),
    ),
    utila.create_step(
        'legacy',
        inputs=[
            utila.ResultFile(producer='pagenumber', name='result_result'),
            utila.ResultFile(producer='pagenumber', name='magic_magic'),
        ],
        output=('pagenumber', 'magic'),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=pagenumber.ROOT,
        featurepackage='pagenumber.feature',
        config=utila.FeaturePackConfig(
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
    path = utila.rreplace(
        path,
        pattern='pagenumber__legacy_pagenumber',
        replace='groupme__pagenumbers_pagenumbers',
    )
    path = utila.rreplace(
        path,
        pattern='pagenumber__legacy_magic',
        replace='groupme__pagenumbers_magic',
    )
    return path
