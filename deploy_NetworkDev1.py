#!/usr/bin/python3

from maendeleolab_lib import *

regions_list = [
        'us-east-1',
        'us-west-2'
        ]

for region in regions_list:
    make_elastic_ip(
        Elastic_Ip='NetworkDev1_a',
        Tag_key='Type',
        Tag_value='Not-billable',
        Region=region
    )

    make_elastic_ip(
        Elastic_Ip='NetworkDev1_b',
        Tag_key='Type',
        Tag_value='Not-billable',
        Region=region
    )

# ---------------------- End -------------------------
