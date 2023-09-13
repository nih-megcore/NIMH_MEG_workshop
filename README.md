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

# Biowulf users (must be NIH associated)
Log into biowulf
```
sinteractive --mem=16G --cpus-per-task=12 --gres=lscratch:10 --tunnel
module use --append /data/MEGmodules/modulefiles
module load meg_workshop
```
Copy the line from the terminal above that looks something like the below and paste into a new terminal
```
ssh  -L PORTNUMBER:localhost:PORTNUMBER USERNAME@biowulf.nih.gov   
```

Copy notebooks to your local folder.  Change directories first if you don't want the code/data in your home folder.
```
#Make sure to load the module beforehand
get_code
get_data
```
Startup Notebook on Biowulf
```
cd MEG_workshop_2023
./notebook_start.sh
```


# Install (not required for biowulf users)
Mamba is not required, but will install faster than conda (functionally they are the same) <br>
To install mamba - `conda install --channel=conda-forge --name=base mamba`
<br><br>
### Install (version1) - requires make, mamba, git
```
git clone https://github.com/nih-megcore/MEG_workshop_2023.git
cd MEG_workshop_2023
make install 
```

### Install (version2) 
```
#Clone this repository
git clone https://github.com/nih-megcore/MEG_workshop_2023.git

#Install MNE
mamba create --override-channels --channel=conda-forge --name=MEG_workshop mne pip jupyterlab -y
conda activate MEG_workshop
pip install h5io pymatreader

#Install the Workshop files
cd MEG_workshop_2023
pip install -e .    #Install this code
pip install git+https://github.com/nih-megcore/nih_to_mne.git  #Install some auxilliary NIH code
```

## Install auxiliary code
Install freesurfer: https://surfer.nmr.mgh.harvard.edu/fswiki/rel7downloads
Install Afni: https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/background_install/main_toc.html


## Check installs
Run `./check_installation.sh` to check for freesurfer / afni / mne / jupyter installation.
