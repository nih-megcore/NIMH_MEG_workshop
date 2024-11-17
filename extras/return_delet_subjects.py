#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 10:27:32 2024

@author: jstout
"""

import datalad
import glob
import shutil

target_subjects = ['22671', '70467', '62003', '72082', '85305', '52662', '89475', '42107',
            '61373', '89474', '03748', '84896', '02811']
target_subjects = ['sub-ON'+i for i in target_subjects]

all_subjects = glob.glob('sub-*')
for i in target_subjects:
    all_subjects.remove(i)
    

print(' '.join(all_subjects))
