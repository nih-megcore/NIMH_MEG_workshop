for dset in $(find sub-* -name '*airpuff*ds'); do megcore_prep_mri_bids.py -filename $dset; done
