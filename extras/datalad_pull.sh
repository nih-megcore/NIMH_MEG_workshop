datalad install https://github.com/OpenNeuroDatasets/ds004215.git

cd ds004215

# [22671 70467 62003 72082 85305 52662 89475 42107 61373 89474 03748 84896 02811]

#Download all the airpuf and T1w data for the following subjects
for i in 22671 70467 62003 72082 85305 52662 89475 42107 61373 89474 03748 84896 02811; do datalad get sub-ON${i}/ses-01/meg/*airpuff*  sub-ON${i}/ses-01/anat/*T1w* sub-ON${i}/ses-01/meg/*noise*.ds; done

#Unlock the data - makes copying easier
for i in 22671 70467 62003 72082 85305 52662 89475 42107 61373 89474 03748 84896 02811; do datalad unlock sub-ON${i}/ses-01/meg/*airpuff* sub-ON${i}/ses-01/anat/*T1w* sub-ON${i}/ses-01/meg/*noise*  ; done

#Clean channel names -- need to update OPENNEURO
for i in $(find sub-* -name '*channels.tsv') ; do sed -i 's/-1609//g' $i ; sed -i 's/-2104//g' $i ; done

#Eliminate unused data - this are small files currently since we didn't pull them
git rm -r sub-ON55820 sub-ON35773 sub-ON35920 sub-ON62623 sub-ON12666 sub-ON28693 sub-ON84651 sub-ON48190 sub-ON66199 sub-ON39384 sub-ON67435 sub-ON41606 sub-ON75450 sub-ON05258 sub-ON63704 sub-ON82386 sub-ON39099 sub-ON05530 sub-ON97451 sub-ON61087 sub-ON25939 sub-ON82948 sub-ON11111 sub-ON48984 sub-ON89045 sub-ON63734 sub-ON43585 sub-ON51005 sub-ON43016 sub-ON06910 sub-ON98098 sub-ON86202 sub-ON98018 sub-ON01802 sub-ON37194 sub-ON71932 sub-ON48925 sub-ON22299 sub-ON69092 sub-ON72409 sub-ON33159 sub-ON87054 sub-ON87092 sub-ON23483 sub-ON82798 sub-ON85616 sub-ON23776 sub-ON52733 sub-ON79309 sub-ON76510 sub-ON74065 sub-ON86779 sub-ON63335 sub-ON50015 sub-ON02693 sub-ON65733 sub-ON18047 sub-ON13986 sub-ON87538 sub-ON52992 sub-ON13545 sub-ON02747 sub-ON50636 sub-ON93016 sub-ON56250 sub-ON94663 sub-ON85981 sub-ON05311 sub-ON43001 sub-ON78603 sub-ON56044 sub-ON67121 sub-ON26105 sub-ON58053 sub-ON62955 sub-ON84478 sub-ON30535 sub-ON26854 sub-ON23664 sub-ON41090 sub-ON12688 sub-ON73969 sub-ON92067 sub-ON80038 sub-ON33827 sub-ON08643 sub-ON54886 sub-ON80356 sub-ON99871 sub-ON81734 sub-ON34766 sub-ON95003 sub-ON08792 sub-ON11411 sub-ON96522 sub-ON23897 sub-ON52083 sub-ON01016 sub-ON07392 sub-ON95259 sub-ON23419 sub-ON65553 sub-ON54268 sub-ON62592 sub-ON95742 sub-ON22662 sub-ON25658 sub-ON17159 sub-ON98806 sub-ON09474 sub-ON65697 sub-ON47254 sub-ON38044 sub-ON87313 sub-ON26309 sub-ON30080 sub-ON10965 sub-ON91906 sub-ON08392 sub-ON21834 sub-ON99299 sub-ON88614 sub-ON21976 sub-ON66557 sub-ON94856 sub-ON95422 sub-ON59735 sub-ON31551 sub-ON08571 sub-ON42941 sub-ON40397 sub-ON08155 sub-ON97504 sub-ON67563 sub-ON44262 sub-ON99620 sub-ON34754 sub-ON48555 sub-ON46717 sub-ON21959 sub-ON49080 sub-ON93426 sub-ON40757 sub-ON11394

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
${SCRIPT_DIR}/extras/fix_hv_dsets.py
