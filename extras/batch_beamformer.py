#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 13:26:49 2023

@author: Allison Nugent and Jeff Stout
"""

import mne
import mne_bids
from mne_bids import BIDSPath
import os, os.path as op
import nilearn
import matplotlib.pyplot as plt
import numpy as np
import nih2mne
import glob

#from nilearn import *
from nih2mne.utilities.bids_helpers import get_mri_dict
n_jobs = 30 #Number of parrallel operations

# first let's set up directories

# bids_root = '/data/jstout/meg_workshop_data'
bids_root = '/data/MEGmodules/modules/meg_workshop_2023_extras/ds004215'
#bids_root = op.join('/data',os.environ['USER'], 'meg_workshop_data') 
deriv_root = op.join(bids_root, 'derivatives')
project_root = op.join(deriv_root, 'Day2')
fs_subjects_dir = op.join(deriv_root,'freesurfer','subjects')



def proc_stc(subject, filt_freqs=[]):
    fs_subject = 'sub-' + subject
    data_dict = nih2mne.utilities.bids_helpers.get_mri_dict(subject,bids_root, task='airpuff', project='Day2')
    
    # load in all the MRI stuff
    bem = data_dict['bem'].load()
    fwd = data_dict['volfwd'].load()
    src = fwd['src']
    trans = data_dict['trans'].load()
    
    #Load the Raw data
    bids_path = BIDSPath(root=bids_root, subject=subject, task='airpuff', run='01',session='01')
    project_path = bids_path.copy().update(root=project_root, check=False)
                                           
                                           
    raw = mne.io.read_raw_ctf(bids_path.fpath, clean_names=True, preload=True, verbose=False)
    # put a bandpass on the raw, and a notch
    raw.filter(filt_freqs[0], filt_freqs[1], n_jobs=n_jobs)
    raw.notch_filter(freqs=[60])

   
    # We also want to load in the empty room dataset so we can calculate a noise covariance 
    noise_path = bids_path.copy().update(task='noise') 
    noise = mne.io.read_raw_ctf(noise_path.fpath, clean_names=True, preload=True, verbose=False)
    noise = noise.filter(filt_freqs[0], filt_freqs[1], n_jobs=n_jobs)
    
    # Now lets extract the events, make epochs
    evts, evtsid = mne.events_from_annotations(raw)

    epochs = mne.Epochs(raw, evts, evtsid, tmin=-0.1, tmax=0.2, preload=True)
    epochs.apply_hilbert()
    # epochs.crop(tmin=-0.1, tmax=0.2)  #Get rid of edge effects -- this has a weird issue
    # epochs.apply_baseline(baseline=(-0.1, 0))

    # let's also average the epochs to visualize the evoked responses
    evk_stim = epochs['stim'].average()
    evk_missingstim = epochs['missingstim'].average()

    cov_all = mne.compute_covariance(epochs, tmin=-0.1, tmax = 0.2, n_jobs=n_jobs)
    
    noise_cov = mne.make_ad_hoc_cov(raw.info)
    
    # Let's say we want to project the evoked response into source space
    # notice here that I'm using the covariance from ALL the marks, not just the stimuli
    filters = mne.beamformer.make_lcmv(evk_stim.info, fwd, cov_all, reg=0.05, pick_ori='max-power',
                                       noise_cov = noise_cov, weight_norm='unit-noise-gain')
    
    #Send data through beamformer
    stc_stim=mne.beamformer.apply_lcmv(evk_stim, filters)
    stc_missingstim=mne.beamformer.apply_lcmv(evk_missingstim, filters)
    
    #Get envelope of hilbert at the source
    stc_stim._data = np.abs(stc_stim._data)
    stc_missingstim._data = np.abs(stc_missingstim._data)
    
    #Output Paths
    stc_stim_path = project_path.copy().update(suffix=f'stc{filt_freqs[0]}to{filt_freqs[1]}', description='stim',extension=None)#, datatype='meg')
    stc_missingstim_path = project_path.copy().update(suffix=f'stc{filt_freqs[0]}to{filt_freqs[1]}', description='missingstim',extension=None)#, datatype='meg')
    
    #Get the envelope
    stc_stim.save(stc_stim_path, overwrite=True)
    stc_missingstim.save(stc_missingstim_path, overwrite=True)
    
subjects = glob.glob(op.join(bids_root, 'sub-*'))
subjects = [i.split('-')[1] for i in subjects]

for subject in subjects:
    for filt_freqs in [[1,3], [3,6], [8,12], [13,30], [30,50]]:
        proc_stc(subject, filt_freqs=filt_freqs)
        



# # You probably noticed the dreaded Beamformer Sign Ambiguity 

# # what happens if we use the normals from the freesurfer cortical surface? 
# fwd_src_ori = mne.convert_forward_solution(fwd, surf_ori=True)
# filters_src_ori = mne.beamformer.make_lcmv(evk_stim.info, fwd_src_ori, cov_all, reg=0.05, pick_ori='normal',
#                                    noise_cov = noise_cov, weight_norm='unit-noise-gain')
# stc_src_ori=mne.beamformer.apply_lcmv(evk_stim, filters)

# brain=stc_src_ori.plot(hemi='both', subjects_dir=fs_subjects_dir, subject=fs_subject)

# # You might *think* that looks worse, but now, the sign of the output is following the surface. 
# # In opposing sulci, the surface normals are oriented opposite eachother. 

# # Frequently what we do is to invoke a sign "flip"

# # I've figured out that index 166 corresponds to roughly the peak of the evoked response.
# # There are 8196 vertices
# for i in range(8196):
#     if stc.data[i,166] < 0:
#         stc.data[i,:] *= -1
# # You need to remember here, however, that you are also flipping vertices that aren't particularly active
# # so you'll also be ensuring that all the noise in that time point is positive.

# brain=stc.plot(hemi='both', subjects_dir=fs_subjects_dir, subject=fs_subject)

# # We can make the time course for the missing stim as well
# stc_missing=mne.beamformer.apply_lcmv(evk_missingstim, filters)

# # plot it 
# brain=stc_missing.plot(hemi='both', subjects_dir=fs_subjects_dir, subject=fs_subject)

# # interesting, there does seem to be something out around 150ms, doesn't there.... but again the flip thing...

# # Remember our time frequency plots for this person - wasn't there something in alpha around that time? 
# # Maybe we should look at alpha power

# cov_all_alpha = mne.compute_covariance(epochs_alpha, tmin=0.1, tmax = 0.2, n_jobs=n_jobs)
# cov_stim_alpha = mne.compute_covariance(epochs_alpha['stim'], tmin=.1, tmax = 0.2, n_jobs=n_jobs)
# cov_missingstim_alpha = mne.compute_covariance(epochs_alpha['missingstim'], tmin=0.1, tmax = 0.2, n_jobs=n_jobs)

# filters_alpha = mne.beamformer.make_lcmv(epochs_alpha.info, fwd, cov_all_alpha, reg=0.05, noise_cov=noise_cov)

# stc_stim_alpha = mne.beamformer.apply_lcmv_cov(cov_stim_alpha, filters_alpha)
# stc_missing_alpha = mne.beamformer.apply_lcmv_cov(cov_missingstim_alpha, filters_alpha)

# stc_contrast.data=stc_stim_alpha.data/stc_missing_alpha.data

# brain=stc_contrast.plot(hemi='both', subjects_dir=fs_subjects_dir, subject=fs_subject)



# # Okay, now lets loop over all the subjects!!
# subjects=['ON02811','ON03748','ON22671','ON42107','ON52662','ON61373','ON62003','']
