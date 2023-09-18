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
| 9:30-10:30 | Source Localization (Dipoles, multiple dipoles, MNE, dSPM, Beamformer) | Fred + Jeff | 
| 10:30 - 11:30 | Code | 
| 11:30 - 12:00 | Beamformer Specifics - Covariance, filtering, data rank, regularization | Allison |
| 12:00 - 1:00| Lunch |
| 1:00 - 2:00 | Single subject to group data | Jeff |
| 2:00 - 2:30 | Code |
| 2:30 - 3:30 | Statistics (parametric / log transform / resampling stats / clusters ) | Fred + Allison |
| 3:30 - 4:00 | Code | 
| 4:00 - 5:00 | Course Review and Overview of Additional Techniques| Allison + Amaia |

# Biowulf users (must be NIH associated)
Log into biowulf:  `ssh USERNAME@biowulf.nih.gov`
```
#Allocate resources for processing
sinteractive --mem=16G --cpus-per-task=12 --gres=lscratch:10 --tunnel --time=08:00:00
```
You will see a line like the below. Follow the instructions (start a new terminal into biowulf), then return to original terminal for the rest of the commands.
![Tunnel](extras/images/tunnel_prompt.png)

Copy notebooks to your local folder.  Change directories first if you don't want the code/data in your home folder.
```
module use --append /data/MEGmodules/modulefiles  #You can add this to your .bashrc for convenience
module load meg_workshop
# Copy the code and the data to your local folder
get_code 
get_data
```
Startup Notebook on Biowulf
```
cd MEG_workshop_2023
./notebook_start.sh
```
Enter this into the address bar of your web browser `localhost:<PORT>` <br>
![JupyterLogin](extras/images/Jupyter_login.png)



# Install (not required for biowulf users)
The following software is required to run all parts of the coding sections: afni + freesurfer + git + miniconda(/conda) <br>
To run the majority of the code: miniconda/conda + git are required <br><br>

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

## Install dataset
```
mamba create -n datalad -c conda-forge datalad gdown -y
conda activate datalad
```
This will pull the NIMH_hv OpenNeuro repository and associated files. <br>
This will download the freesurfer processed MRI files as well
```
 ./extras/datalad_pull.sh
```

## Install auxiliary code
Install freesurfer: https://surfer.nmr.mgh.harvard.edu/fswiki/rel7downloads <br>
Install Afni: https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/background_install/main_toc.html <br>


## Check installs
Run `./check_installation.sh` to check for freesurfer / afni / mne / jupyter installation.
