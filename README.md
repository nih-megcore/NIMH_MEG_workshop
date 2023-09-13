# MEG_workshop_2023

## Day 1 (09/27/2023)
| Time  | Topic | Presenter |
| :---- | ---- | ---- |
| 9:00 - 9:15 | Bagel Config + Coffee Download + Computer Setup |
| 9:15 - 9:30 | Course Intro + MEGcore Intro | MEGcore |
| 9:30 - 10:30 | Intro to MEG and general overview of source localization | Fred |
| 10:30 - 11:00 | MEG Hardware and Signal Generation / Collection | Stephen | 
| 11:30 - 12:00 | Code + Coffee (Load, plot, display channel data) |
| 12:00 - 1:00 | Lunch | 
| 1:00 - 2:00 | Stimuli, trigger processing, epochs, evoked data, bad chans | Tom + Anna |
|  |  bad epochs, filtering, abberant signals |  
| 2:00 - 2:30 | Code  ( channel preprocessing ) |
| 2:30 - 3:30 | Filtering Data, Frequency Analysis, Hilbert, Brain Rythms, and Artifacts | Allison | 
| 3:30 - 4:00 | Code 
| 4:00 - 5:00 | MRI Processing, placing fiducials, coreg, source model (volume + surface) | Anna + Jeff |
| | BEM, Forward Model | 

## Day 2 (10/04/2023)
| Time  | Topic | Presenter |
| :---- | ---- | ---- |
| 9:30-10:30 | Inverse Solutions (Dipoles, multiple dipoles, MNE, dSPM, Beamformer) | Fred + Jeff | 
| 10:30 - 11:30 | Code | 
| 11:30 - 12:00 | Beamformer Specifics - Covariance, filtering, data rank, regularization | Allison |
| 12:00 - 1:00| Lunch |
| 1:00 - 2:00 | Single subject to group data | Jeff |
| 2:00 - 2:30 | Code |
| 2:30 - 3:30 | Statistics (parametric / log transform / resampling stats / clusters ) | Fred + Allison |
| 3:30 - 4:00 | Code | 
| 4:00 - 5:00 | Review | Allison |

# Install (not required for biowulf users)
Mamba is not required, but will install faster than conda (functionally they are the same) <br>
To install mamba - `conda install --channel=conda-forge --name=base mamba`
<br><br>
Course install
```
#Clone this repository
git clone https://github.com/nih-megcore/MEG_workshop_2023.git
#Install MNE
mamba create --override-channels --channel=conda-forge --name=MEG_workshop mne pip
conda activate MEG_workshop
cd MEG_workshop_2023
#Install the Workshop files
pip install -e .  
pip install git+https://github.com/nih-megcore/nih_to_mne.git
```
