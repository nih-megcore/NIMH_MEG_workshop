#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 18:02:20 2022

@author: jstout
"""

import glob
import mne
import os
import copy 
import numpy as np
from mne.beamformer import make_lcmv, apply_lcmv, apply_lcmv_epochs
from mne.datasets import fetch_fsaverage
import subprocess

topdir = '/fast/bids_ica'
os.chdir(topdir)

#Setup for fs average warping
subjects_dir = f'{topdir}/data/SUBJECTS_DIR'
fetch_fsaverage(subjects_dir, verbose=False)  # ensure fsaverage src exists
fname_fs_src = subjects_dir + '/fsaverage/bem/fsaverage-vol-5-src.fif'
src_fs = mne.read_source_spaces(fname_fs_src)


def get_morph_to_fsaverage(subject_fs, src):
    subjects_dir = f'{topdir}/data/SUBJECTS_DIR'
    from mne.datasets import fetch_fsaverage
    fetch_fsaverage(subjects_dir, verbose=False)  # ensure fsaverage src exists
    fname_fs_src = subjects_dir + '/fsaverage/bem/fsaverage-vol-5-src.fif'
    
    src_fs = mne.read_source_spaces(fname_fs_src)
    morph = mne.compute_source_morph(
        src, subject_from=subject_fs, src_to=src_fs, subjects_dir=subjects_dir,
        verbose=True)
    return morph

def return_subj_dsets(subjid, search_dir=None):
    stc_list=glob.glob(os.path.join(search_dir, subjid+'_*.stc'))
    t1_dset = f'{subjid}_T1.nii'
    return {'t1_dset':t1_dset,
            'stc_list':stc_list}
    

def process_morphs(subjid):
    forward = mne.read_forward_solution(f'{topdir}/data/fwds/{subjid}-task-haririhammer-fwd.fif')    
    src = forward['src']
    morph = get_morph_to_fsaverage(subjid, src)
    
    proc_list = return_subj_dsets(subjid, search_dir=f'{topdir}/hariri_results')
    if not os.path.exists(f'{topdir}/fsave_warped_outputs'): os.mkdir(f'{topdir}/fsave_warped_outputs')
    
    for fname in proc_list['stc_list']:
        stc = mne.read_source_estimate(fname)
        outname = os.path.basename(fname).split('-stc.fif')[0]+'_fsave.nii'
        morphed_stc = morph.apply(stc, verbose=False)
        morphed_stc.save_as_volume(f'{topdir}/fsave_warped_outputs/{outname}', src_fs) #f'{topdir}/results/stc_fs_ave_space_subtract/{subjid}_subtract_face_shape.nii', src_fs)
    
def convert_to_brik(fname):
    in_base = os.path.basename(fname)
    out_fname = in_base.replace('.nii','+tlrc.') 
    out_fname = os.path.join(os.path.dirname(fname), out_fname)
    if not os.path.exists(out_fname):
        cmd = f'3dcopy {fname} {out_fname}'
        subprocess.run(cmd.split())


mris = glob.glob(f'hariri_results/*_T1.nii')
subjids = [os.path.basename(i).split('_')[0] for i in mris]

for subjid in subjids:
    process_morphs(subjid)
    
for fname in glob.glob(f'fsave_warped_outputs/*.nii'):
    convert_to_brik(fname)


