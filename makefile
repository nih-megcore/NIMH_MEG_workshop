
#>>>> https://stackoverflow.com/questions/53382383/makefile-cant-use-conda-activate
# Need to specify bash in order for conda activate to work.
SHELL=/bin/bash
# Note that the extra activate is needed to ensure that the activate floats env to the front of PATH
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate 
# <<<<

install:
	mamba create --override-channels --channel=conda-forge --name=MEG_workshop mne==1.5 pip jupyterlab -y
	($(CONDA_ACTIVATE) MEG_workshop ; pip install h5io pymatreader git+https://github.com/nih-megcore/nih_to_mne.git)
	($(CONDA_ACTIVATE) MEG_workshop ; pip install -e .)

