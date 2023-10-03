#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 11:35:29 2021

@author: jstout
"""
import glob
import mne
import os
import copy 
import numpy as np
from mne.beamformer import make_lcmv, apply_lcmv, apply_lcmv_epochs
from mne.datasets import fetch_fsaverage
from itertools import product


topdir = '/data/NIMH_MEGCoregroup/Hariri_tutorial_stats'
os.chdir(topdir)

#Setup for fs average warping
subjects_dir = f'{topdir}/data/SUBJECTS_DIR'
fetch_fsaverage(subjects_dir, verbose=False)  # ensure fsaverage src exists
fname_fs_src = subjects_dir + '/fsaverage/bem/fsaverage-vol-5-src.fif'
src_fs = mne.read_source_spaces(fname_fs_src)

 
def get_drop_idx(drop_log):
    '''Return list of epoch indices to be dropped
    Useful in assessing on wideband data and applying to narrowband data'''
    drop_idxs=[]
    drop_log_trimmed = [i for i in drop_log if 'IGNORED' not in i]

    for idx,entry in enumerate(drop_log_trimmed):
        if len([i for i in entry if i[0]=='M'])>0:
            drop_idxs.append(idx)
    return drop_idxs


def full_process(filename, l_freq=None, h_freq=None, outdir=None):
    #Have to link ica outputs to topdir/data/hariri_data
    # filename='sub-ON89475_js_manual-raw.fif'
    subjid = os.path.basename(filename).split('_')[0]
    # ctf_filename = glob.glob(f'{topdir}/input/{subjid}*haririhammer*meg.ds')[0]
    # ctf_filename='/fast/bids_ica/input/sub-ON89475_ses-01_task-haririhammer_run-01_meg.ds'
    raw = mne.io.read_raw_ctf(filename)
    subjects_dir = f'{topdir}/data/SUBJECTS_DIR'
    
    subject_fs = subjid
    trans = mne.read_trans(f'{topdir}/data/transfiles/{subjid}-trans.fif')
    
    in_fname = os.path.basename(filename)
    raw=raw.load_data() #mne.io.read_raw_ctf(f'{topdir}/data/hariri_data/{in_fname}', preload=True)
    raw.resample(300).notch_filter([60,120])
    
    if not os.path.exists(f'{topdir}/data/SUBJECTS_DIR/{subjid}/bem/inner_skull.surf'):
                          mne.bem.make_watershed_bem(subject=subject_fs, subjects_dir=f'{topdir}/data/SUBJECTS_DIR',
                                                     overwrite=True)
    task = os.path.basename(filename).split('_')[2]
    fwd_fname = f'{topdir}/data/fwds/{subjid}-{task}-fwd.fif'
    if not os.path.exists(fwd_fname):
        bem = mne.make_bem_model(subject_fs, subjects_dir=f'{topdir}/data/SUBJECTS_DIR', conductivity=[0.3])
        bem_sol = mne.make_bem_solution(bem)
        src = mne.source_space.setup_volume_source_space(subject=subject_fs, subjects_dir=f'{topdir}/data/SUBJECTS_DIR', mri='T1.mgz', bem=bem_sol)
        forward = mne.make_forward_solution(raw.info, trans, src, bem_sol, meg=True, eeg=False)
        mne.forward.write_forward_solution(fwd_fname, forward)
    else:
        forward = mne.forward.read_forward_solution(fwd_fname)
    src = forward['src']

    # =============================================================================
    # Load raw data and assess bad epochs before filtering  (already at 1-100Hz)
    # =============================================================================
    raw = raw.load_data().filter(1.0, None) #mne.io.read_raw_ctf(filename, preload=True)
    events, event_ids = mne.events_from_annotations(raw)
    event_ids = {key:event_ids[key] for key in event_ids.keys() if key in ['go','nogo']} 

    reject_dict=dict(mag=2500e-15)
    epochs = mne.Epochs(raw, events, event_id=event_ids, tmin=-0.2, tmax=0.8, reject_tmax=0,
                    reject=reject_dict, preload=True, baseline=(-0.2,None))
    drop_log = copy.copy(epochs.drop_log)
    drop_idxs = get_drop_idx(drop_log)
    
    del epochs
    
    #Filter the data 
    # if not (l_freq==None) and (h_freq==None):
    raw.filter(l_freq, h_freq)    
        
    # if l_freq==None:
    #     l_freq=int(raw.info['highpass'])
    # if h_freq==None:
    #     h_freq=int(raw.info['lowpass'])
    
    events, event_ids = mne.events_from_annotations(raw) 
    event_ids = {key:event_ids[key] for key in event_ids.keys() if key in ['go','nogo']}
    epochs = mne.Epochs(raw, events, event_id=event_ids, tmin=0, tmax=0.4, reject_tmax=0,
                    preload=False, baseline=None) #(-0.2,None))
    epochs.drop(drop_idxs)  #Drop based on the wideband threshold
    epochs.load_data()
    from mne.epochs import equalize_epoch_counts
    
    # epochs.apply_baseline(baseline=(-0.4, 0))
    epochs.pick_types(meg=True)    
    
    #Create single stim epochs and evoked data
    go_evoked = epochs['go'].average()
    go_epochs = epochs['go']
    nogo_evoked = epochs['nogo'].average()
    nogo_epochs = epochs['nogo']
    equalize_epoch_counts([go_epochs, nogo_epochs])
    
    # common_cov = mne.compute_covariance(epochs, tmin=-0.4, tmax=1.0, 
    #                                     method='empirical')
    
    noise_fname=f'{topdir}/data/MEG_EmptyRoom_20190508_01.ds'
    noise_raw = mne.io.read_raw_ctf(noise_fname) #'/home/jstout/Desktop/TEST4/neurofeedback_proj/data/emptyroom/MEG_EmptyRoom_20190508_01.ds')
    noise_raw.load_data()
    noise_raw.resample(300).notch_filter([60,120]).filter(l_freq, h_freq)
    noise_cov = mne.compute_raw_covariance(noise_raw, method='empirical')
    
    rank = mne.compute_rank(epochs, tol=1e-6, tol_kind='relative')
    print(rank)
    # filters = make_lcmv(epochs.info, forward, common_cov, noise_cov=noise_cov, reg=0.05, 
    #                     pick_ori='max-power',
    #                         reduce_rank=True, rank=rank) #, depth = 0)
    
    common_cov = mne.compute_covariance(epochs, tmin=0, tmax=.4, 
                                        method='empirical')
    go_cov = mne.compute_covariance(go_epochs, tmin=0, tmax=.4, 
                                        method='empirical')
    nogo_cov = mne.compute_covariance(nogo_epochs, tmin=0, tmax=0.4, 
                                        method='empirical')
    
    
    filters = make_lcmv(epochs.info, forward, common_cov, noise_cov=noise_cov, 
                        reg=0.01, rank=rank, pick_ori='max-power')

    from mne.beamformer import apply_lcmv_cov
    go_power = apply_lcmv_cov(go_cov, filters, verbose = None)
    nogo_power = apply_lcmv_cov(nogo_cov, filters, verbose = None)
    noise_power = apply_lcmv_cov(noise_cov, filters, verbose = None)

    lograt = copy.deepcopy(go_power)
    lograt._data= np.log(go_power._data/nogo_power._data)
    # face_power._data = face_power._data/noise_power._data
    # shape_power._data = shape_power._data/noise_power._data
    
    # =============================================================================
    # Save outputs
    # =============================================================================
    if type(l_freq) in [int, float]: l_freq=str(int(l_freq))
    if type(h_freq) in [int, float]: h_freq=str(int(h_freq))    
    
    if outdir==None:
        outdir=f'{topdir}/output'
    out_go_fname = f'{outdir}/{subjid}_{l_freq}_{h_freq}_go_pow.nii'
    go_power.save_as_volume(out_go_fname, src)
    out_nogo_fname = f'{outdir}/{subjid}_{l_freq}_{h_freq}_nogo_pow.nii'
    nogo_power.save_as_volume(out_nogo_fname, src)
    out_lograt_fname = f'{outdir}/{subjid}_{l_freq}_{h_freq}_lograt_pow.nii'
    lograt.save_as_volume(out_lograt_fname, src)
    
    out_go_stc_fname = f'{outdir}/{subjid}_{l_freq}_{h_freq}_go_pow-stc.fif'
    out_nogo_stc_fname = f'{outdir}/{subjid}_{l_freq}_{h_freq}_nogo_pow-stc.fif'
    out_lograt_stc_fname = f'{outdir}/{subjid}_{l_freq}_{h_freq}_lograt_pow-stc.fif'
    go_power.save(out_go_stc_fname)
    nogo_power.save(out_nogo_stc_fname)
    lograt.save(out_lograt_stc_fname)
    
    # =============================================================================
    # Convert to Afni
    # =============================================================================
    import subprocess
    subj_t1_mgz = os.path.join(subjects_dir, subject_fs, 'mri','T1.mgz')
    out_fname = os.path.join(outdir, subjid+'_T1.nii')
    cmd=f'mri_convert {subj_t1_mgz} {out_fname}'
    subprocess.run(cmd.split())
    
    del cmd
    out_fname_brik =  os.path.join(outdir, subjid)
    cmd = f'3dcopy {out_fname} {out_fname_brik}'
    subprocess.run(cmd.split())
    del cmd
    go_source_brik = os.path.join(outdir, subjid+f'_{l_freq}_{h_freq}_go_pow+orig')
    cmd = f'3dcopy {out_go_fname} {go_source_brik}'
    subprocess.run(cmd.split())
    del cmd
    nogo_source_brik = os.path.join(outdir, subjid+f'_{l_freq}_{h_freq}_nogo_pow+orig')
    cmd = f'3dcopy {out_nogo_fname} {nogo_source_brik}'
    subprocess.run(cmd.split())
    del cmd
    lograt_source_brik = os.path.join(outdir, subjid+f'_{l_freq}_{h_freq}_lograt+orig')
    cmd = f'3dcopy {out_lograt_fname} {lograt_source_brik}'
    subprocess.run(cmd.split())
    
    
    

    
def proc_filename(filename, output_dir):
    freq_bin_list=[[3,7],[7,13],[13,35],[1,100]]
    for freqs in freq_bin_list:
        print(freqs, filename)
        try:
            full_process(filename, l_freq=freqs[0], h_freq=freqs[1], outdir=output_dir)
        except:
            subjid=os.path.basename(filename).split('_')[0]
            with open(f'{topdir}/ERROR_{subjid}.txt', 'w') as w:
                w.write('Error')    
    


    
    
# def iterate_subjects():
#     filenames = glob.glob(f'{topdir}/ica_output/*aw_manual*-raw.fif')
#     # filenames = [os.path.basename(i) for i in filenames]
#     freq_bin_list=[[3,7],[7,13],[13,35],[1,100]]
#     for freqs,filename in product(freq_bin_list, filenames):
#         print(freqs, filename)
#         try:
#             full_process(filename, l_freq=freqs[0], h_freq=freqs[1])
#         except:
#             subjid=os.path.basename(filename).split('_')[0]
#             with open(f'{topdir}/ERROR_{subjid}.txt', 'w') as w:
#                 w.write('Error')

# def normalize_stc_on_prestim(stc):
#     #Identify time zero and calculate a noise normalization
#     idx_t0 = stc.time_as_index(0)[0]
#     src_noise_mat =  stc._data[:,:idx_t0]
#     noise_vals = src_noise_mat.mean(axis=1)   
#     stc._data = stc._data / np.expand_dims(noise_vals, axis=1)
#     return stc

def normalize_stc_on_prestim(group_stack, idx_t0=120):
    #Identify time zero and calculate a noise normalization
    # idx_t0 =120
    src_noise_mat =  group_stack[:,:,:,:idx_t0]
    noise_mean = src_noise_mat.mean(axis=-1) 
    noise_var = src_noise_mat.var(axis=-1)
    z_mat = (group_stack - noise_mean[:,:,:,:,np.newaxis]) / noise_var[:,:,:,:,np.newaxis]
    return z_mat
                
def group_results():
    results_dir = f'{topdir}/results/stc_fs_ave_space_subtract'
    
    av_niis = glob.glob(os.path.join(results_dir, '*_stim_nogo.nii'))
    import nibabel as nb
    affine = nb.load(av_niis[0]).affine
    group_mats = []
    for dset in av_niis:
        group_mats.append(nb.load(dset).get_fdata())
    group_stack = np.stack(group_mats, axis=0)
    group_median = np.median(group_stack, axis=0)
    group_mean = np.mean(group_stack, axis=0)
    
    out_mean = nb.Nifti1Image(group_mean, affine)
    out_mean.to_filename(os.path.join(results_dir, 'group_mean.nii'))
    
    out_med = nb.Nifti1Image(group_median, affine)
    out_med.to_filename(os.path.join(results_dir, 'group_median.nii'))
    
    zmat=normalize_stc_on_prestim(group_stack, idx_t0=120)
    z_mean = zmat.mean(axis=0)
    zout_mean = nb.Nifti1Image(z_mean, affine)
    zout_mean.to_filename(os.path.join(results_dir, 'group_zstat_mean.nii'))    
    
                        
    
        
        

if __name__=='__main__':
    import sys
    outdir=f'{topdir}/gonogo_results'
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    proc_filename(sys.argv[1],outdir)
    # group_results()

