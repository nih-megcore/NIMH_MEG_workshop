echo If no messages are printed below - everything is good
if [ -z $(which recon-all) ]; then echo 'freesurfer not installed' ; fi
if [ -z $(which jupyter) ]; then echo 'jupyter not installed' ; fi
mne_=$(pip list | grep mne)
if [ ${#mne_[@]} -eq 0 ]; then echo 'mne not installed'; fi
