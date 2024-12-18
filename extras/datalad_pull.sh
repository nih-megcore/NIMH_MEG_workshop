datalad install https://github.com/OpenNeuroDatasets/ds004215.git

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

cd ds004215

# [22671 70467 62003 72082 85305 52662 89475 42107 61373 89474 03748 84896 02811]

#Download all the airpuf and T1w data for the following subjects
for i in 22671 70467 62003 72082 85305 52662 89475 42107 61373 89474 03748 84896 02811; do datalad get sub-ON${i}/ses-01/meg/*airpuff*  sub-ON${i}/ses-01/anat/*T1w* sub-ON${i}/ses-01/meg/*noise*.ds; done

#Get oddball task for single subject
datalad get sub-ON02811/ses-01/meg/*oddball*

#Unlock the data - makes copying easier
for i in 22671 70467 62003 72082 85305 52662 89475 42107 61373 89474 03748 84896 02811; do datalad unlock sub-ON${i}/ses-01/meg/*airpuff* sub-ON${i}/ses-01/anat/*T1w* sub-ON${i}/ses-01/meg/*noise*  ; done

#Clean channel names -- need to update OPENNEURO
for i in $(find sub-* -name '*channels.tsv') ; do sed -i 's/-1609//g' $i ; sed -i 's/-2104//g' $i ; done


#Eliminate unused data - this are small files currently since we didn't pull them
git rm -rf sub-ON80038 sub-ON72409 sub-ON96555 sub-ON99633 sub-ON31551 sub-ON02693 sub-ON96565 sub-ON97252 sub-ON87725 sub-ON08571 sub-ON88512 sub-ON94131 sub-ON34766 sub-ON99547 sub-ON98362 sub-ON94110 sub-ON43210 sub-ON41606 sub-ON87616 sub-ON23897 sub-ON25939 sub-ON23483 sub-ON84478 sub-ON48984 sub-ON98175 sub-ON88555 sub-ON96602 sub-ON08155 sub-ON09760 sub-ON87631 sub-ON18047 sub-ON09766 sub-ON98664 sub-ON97451 sub-ON06421 sub-ON08392 sub-ON85010 sub-ON44262 sub-ON65733 sub-ON87304 sub-ON84651 sub-ON87642 sub-ON87655 sub-ON85616 sub-ON92067 sub-ON82798 sub-ON97604 sub-ON83320 sub-ON97654 sub-ON34754 sub-ON95422 sub-ON95214 sub-ON81734 sub-ON65412 sub-ON25658 sub-ON79309 sub-ON10965 sub-ON00400 sub-ON08792 sub-ON93426 sub-ON66401 sub-ON52220 sub-ON66243 sub-ON87313 sub-ON13986 sub-ON87362 sub-ON65403 sub-ON98130 sub-ON99703 sub-ON96440 sub-ON55820 sub-ON21976 sub-ON05311 sub-ON58053 sub-ON85981 sub-ON95520 sub-ON97515 sub-ON40397 sub-ON59735 sub-ON71932 sub-ON50015 sub-ON78603 sub-ON84201 sub-ON76525 sub-ON92220 sub-ON88614 sub-ON11411 sub-ON35773 sub-ON04111 sub-ON73200 sub-ON97503 sub-ON53213 sub-ON43001 sub-ON96353 sub-ON52992 sub-ON97504 sub-ON87455 sub-ON88753 sub-ON30080 sub-ON99943 sub-ON64410 sub-ON05530 sub-ON66199 sub-ON65553 sub-ON02747 sub-ON40757 sub-ON33221 sub-ON73969 sub-ON85400 sub-ON11394 sub-ON85301 sub-ON56044 sub-ON66452 sub-ON91906 sub-ON26309 sub-ON22662 sub-ON96252 sub-ON87777 sub-ON09474 sub-ON66557 sub-ON88700 sub-ON17159 sub-ON76144 sub-ON43585 sub-ON94856 sub-ON08643 sub-ON08760 sub-ON98745 sub-ON86202 sub-ON67121 sub-ON56250 sub-ON38044 sub-ON51005 sub-ON43016 sub-ON48555 sub-ON95003 sub-ON75450 sub-ON85514 sub-ON82948 sub-ON67563 sub-ON13545 sub-ON62200 sub-ON33827 sub-ON63704 sub-ON30535 sub-ON54886 sub-ON93016 sub-ON97526 sub-ON76510 sub-ON54268 sub-ON75100 sub-ON08710 sub-ON93503 sub-ON01016 sub-ON26854 sub-ON07392 sub-ON65232 sub-ON09540 sub-ON97765 sub-ON98018 sub-ON63734 sub-ON88762 sub-ON96522 sub-ON23419 sub-ON28693 sub-ON98806 sub-ON99299 sub-ON11111 sub-ON06910 sub-ON87054 sub-ON63335 sub-ON09681 sub-ON21959 sub-ON98502 sub-ON98602 sub-ON82386 sub-ON99620 sub-ON48925 sub-ON97427 sub-ON51111 sub-ON77753 sub-ON69092 sub-ON96510 sub-ON52733 sub-ON62592 sub-ON52083 sub-ON96240 sub-ON23776 sub-ON41090 sub-ON87550 sub-ON89045 sub-ON12666 sub-ON37194 sub-ON99871 sub-ON87743 sub-ON05258 sub-ON99881 sub-ON74320 sub-ON86779 sub-ON26105 sub-ON63221 sub-ON35920 sub-ON39099 sub-ON47254 sub-ON98642 sub-ON49080 sub-ON12688 sub-ON22299 sub-ON42941 sub-ON33159 sub-ON50636 sub-ON01802 sub-ON93222 sub-ON46717 sub-ON39384 sub-ON62955 sub-ON62623 sub-ON95259 sub-ON87092 sub-ON76625 sub-ON75413 sub-ON85330 sub-ON99731 sub-ON65697 sub-ON61087 sub-ON76320 sub-ON94663 sub-ON96530 sub-ON80356 sub-ON21834 sub-ON87538 sub-ON74065 sub-ON23664 sub-ON98826 sub-ON98098 sub-ON95742 sub-ON48190 sub-ON67435



# Clear out extra MRIs
chmod -R 777 ./*
../extras/fix_hv_dsets.py
