# MEG_workshop_2024  

## Day 1 (11/18/2024)
| Time  | Topic | Presenter |
| :---- | ---- | ---- |
| 9:00 - 9:15 | Bagel Config + Coffee Download + Computer Setup |
| 9:15 - 10:15 | Intro to MEG and general overview of source localization | Fred |
| 10:15 - 10:45 | MEG Hardware and Signal Generation / Collection | Stephen | 
| 10:45 - 11:00 | Break
| 11:00 - 11:45 | Stimuli, trigger processing, epochs, evoked data, bad chans | Tom + Anna |
|  |  bad epochs, filtering, abberant signals | 
| 11:45 - 12:30 | Lunch  
| 12:30 - 1:00 | [Lab 0 Basic Linux/Biowulf]() | Allison | 
| 1:00 - 1:30 | Filtering Data, averaging/evoked data, frequency analysis, hilbert transform, brain rhythms | Allison | 
| 1:30 - 2:00 | [Lab 1 Preprocessing](https://github.com/nih-megcore/NIMH_MEG_workshop/blob/main/Day1/Lab1_preprocessing.ipynb) | 
| 2:00 - 2:45 | [Lab 2 Frequency Analysis](https://github.com/nih-megcore/MEG_workshop_2023/blob/main/Day1/Lab2_frequency_analysis.ipynb) |
| 2:45 - 3:00 | Break | 
| 3:00 - 3:45 | MRI Processing, placing fiducials, coreg, source model (volume + surface) | Anna + Jeff |
| | BEM, Forward Model | 
| 3:45 - 4:30 | [Lab 3 MRI Integration](https://github.com/nih-megcore/MEG_workshop_2023/blob/main/Day1/Lab3_MRI_processing.ipynb) |

## Day 2 (10/04/2023)
| Time  | Topic | Presenter |
| :---- | ---- | ---- |
| 9:00 - 9:15 | Bagel Config + Coffee Download + Computer Setup | |
| 9:15 - 10:00 | Using the MEG lab and MEG core services | Anna | 
| 10:00 - 11:00 | Source Localization (Dipoles, multiple dipoles, MNE, dSPM, Beamformer) | Fred + Jeff | 
| 11:00 - 11:15 | Break | 
| 11:15 - 12:00 | [Lab 4](https://github.com/nih-megcore/MEG_workshop_2023/blob/main/Day2/Lab4_SourceLocalization.ipynb) | 
| 12:00 - 12:45 | Lunch |
| 12:45 - 1:30 | Single subject to group data | Jeff |
| 1:30  - 2:15 | [Lab 5 Beamforming](https://github.com/nih-megcore/MEG_workshop_2023/blob/main/Day2/Lab5_Beamforming.ipynb) + Lunch |
| 2:15 - 2:45 | Git | Jeff |
| ------- FIX Schedule Below ---------- |

| 2:00 - 2:30 | [Lab 6](https://github.com/nih-megcore/MEG_workshop_2023/blob/main/Day2/Lab6_MakingGroupData.ipynb)  |
| 2:30 - 3:30 | Statistics (parametric / log transform / resampling stats / clusters ) | Fred + Allison |
| 3:30 - 4:00 | Code | 
| 4:00 - 4:20 | Course Review | Allison |
| 4:20 - 5:00 | Additional Techniques: OPMs,  Connectivity | Amaia + Lucrezia |
| | Additional Techniques: Decoding, Dynamic Causal Modeling | Shruti + Jess |

# Biowulf users (must be NIH associated)
Log into biowulf:  `ssh -Y USERNAME@biowulf.nih.gov`
```
#You can type tmux before starting sinteractive to have a persistent session between disconnecting wifi
#Allocate resources for processing
sinteractive --mem=16G --cpus-per-task=12 --gres=lscratch:10 --tunnel --time=08:00:00
```
You will see a line like the below. Follow the instructions (start a new terminal into biowulf), then return to original terminal for the rest of the commands.
![Tunnel](extras/images/tunnel_prompt.png)

Copy notebooks to your local folder.  Change directories first if you don't want the code/data in your home folder.
```
module use --append /data/MEGmodules/modulefiles  #You can add this to your .bashrc for convenience
module load meg_workshop

get_code   #Copy the code to your current directory
get_data   #Copy and untar the data to your /data/${USER}/meg_data_workshop

cd MEG_workshop_2023
./start_notebook_Day1.sh  #Start the notebook for Day1 - allows for time series scrolling
#OR use for Day2 material  -- ./start_notebook_Day2.sh - Visualize the 3D brain renderings
```

Enter this into the address bar of your web browser `localhost:<PORT>` <br>
![JupyterLogin](extras/images/Jupyter_login.png)

**NOTE**:If you get something about a **token**: Copy it from the commandline<br><br>

# Install (not required for biowulf users)
The following software is required to run all parts of the coding sections: afni + freesurfer + git + miniconda(/conda) <br>
To run the majority of the code: miniconda/conda + git are required <br><br>

Miniconda will provide the minimum features for the installation:<br>
https://docs.conda.io/projects/miniconda/en/latest/    <br>
In a terminal, find your Download folder (typically `cd /home/<USERNAME>/Downloads`  or `cd /Users/<USERNAME>/Downloads`).  <br>
```
chmod +x Miniconda3-latest.....sh   #Make this file executable - Fill in the rest of name (it will be Linux / Mac/ or Windows)
./Miniconda3-latest...sh  #Run the installer.  Open a new terminal after finishing the installation directions
```

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
#Clone this repository - If you don't have git, just download the zip file from the green button at the top of page
git clone https://github.com/nih-megcore/MEG_workshop_2023.git

#Install MNE - Substitute conda for mamba if any errors
mamba create --override-channels --channel=conda-forge --name=MEG_workshop mne pip jupyterlab -y
conda activate MEG_workshop
pip install h5io pymatreader

#Install the Workshop files
cd MEG_workshop_2023
pip install -e .    #Install this code
pip install git+https://github.com/nih-megcore/nih_to_mne.git  #Install some auxilliary NIH code
```

## Install dataset - if you want to create from scratch.  Use the link provided by email if you want to download
```
mamba create -n datalad -c conda-forge datalad gdown -y
conda activate datalad
```
This will pull the NIMH_hv OpenNeuro repository and associated files. <br>
This will download the freesurfer processed MRI files as well
```
 ./extras/datalad_pull.sh
```

## Install auxiliary code - (not necessary for course Day1)
Install freesurfer: https://surfer.nmr.mgh.harvard.edu/fswiki/rel7downloads <br>
Install Afni: https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/background_install/main_toc.html <br>


## Check installs
Run `./check_requirements.sh` to check for freesurfer / afni / mne / jupyter installation.

# Data Format for code
Input data is in BIDS format from the NIH HV protocol. <br>
Data should be located in `/data/${USER}/meg_workshop_data` <br>
&nbsp;&nbsp; This will automatically be performed on biowulf with the `get_data` command. <br>
Derivatives data will be in `/data/${USER}/meg_workshop_data/{Day1,Day2}/${bids_id}/ses-01/meg/` <br>
&nbsp;&nbsp; Day2 derivatives will have pre-calculated bem, fwd, trans, src files <br>
