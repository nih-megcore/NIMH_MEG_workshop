#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 11:20:29 2023

@author: jstout
"""

import glob, os
import shutil

subjects = glob.glob('sub-*')

# glob.glob('sub-*/ses-01/anat/*.nii.gz')

def remove_extras(subject):
    t1_files = glob.glob(f'{subject}/ses-01/anat/*T1w.nii.gz')
    if len(t1_files) > 1:
        for filename in t1_files:
            if 'rec-SCIC' in filename:
                try:
                    shutil.rmtree(filename)
                    json_fname = filename.replace('.nii.gz', '.json')
                    shutil.rmtree(json_fname)
                except:
                    try:
                        os.unlink(filename)
                        json_fname = filename.replace('.nii.gz', '.json')
                        shutil.rmtree(json_fname)
                    except:
                        print(f'Cant remove {filename}')
    else:
        print(f'Only 1 MRI: {subject}')

def remove_extra_jsons(subject):
    t1_files = glob.glob(f'{subject}/ses-01/anat/*T1w.json')
    if len(t1_files) > 1:
        for filename in t1_files:
            if 'rec-SCIC' in filename:
                try:
                    os.remove(filename)
                except:
                    print(f'Cant remove {filename}')
    else:
        print(f'Only 1 MRI: {subject}')

for subject in subjects:
    remove_extra_jsons(subject)


for subject in subjects:
    remove_extras(subject)
            
            
    