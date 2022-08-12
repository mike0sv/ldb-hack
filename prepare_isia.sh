set -exu

export LDB_DIR=.ldb

rm -rf isia_prepared
rm -rf isia_instiated

ldb index s3://ldb-public/remote/data-lakes/ISIA_500/Croissant --format infer --param base-label=croissant --add-tag isia

# very little actual muffins here :(
#ldb index s3://ldb-public/remote/data-lakes/ISIA_500/Blueberry_pie --format infer --param base-label=blueberry --add-tag isia
#
#mkdir -p isia_instiated
#ldb instantiate ds:root --tag isia --query 'label == `blueberry`' --pipe clip-text 'a muffin' --target isia_instiated/muffin
#
#find isia_instiated/ -name '*.json' -type f -delete
#ldb index isia_instiated/ --format tensorflow-inferred --annotation-update merge

ldb eval ds:root -j --tag 'isia' --no-tag refuse --query 'label' | sort | uniq -c
ldb instantiate ds:root --tag isia --format annot -p single-file=true -t isia_prepared/

