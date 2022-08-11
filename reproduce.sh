set -exu

export LDB_DIR=.ldb


ldb index s3://ldb-hackathon-team-6/clean-up/train --format annot -p single-file=true --add-tag train
ldb index s3://ldb-hackathon-team-6/clean-up/val --format annot -p single-file=true --add-tag val
ldb index s3://ldb-hackathon-team-6/clean-up/labelbook --format annot -p single-file=true --add-tag labelbook
ldb index s3://ldb-public/remote/data-lakes/chihuahua_vs_muffin/ --format infer --add-tag kaggle,train

ldb index s3://ldb-public/remote/data-lakes/Stanford-dog-breeds/n02109525-Saint_Bernard/ --format infer --param base-label=dog --add-tag stanford,train

ldb index google_prepared/ --format annot -p single-file=true --add-tag train

ldb eval -j --query label ds:root | sort | uniq -c

python reset_and_resplit.py
python sort_dataset.py dataset/train/dataset.json
python sort_dataset.py dataset/val/dataset.json
python sort_dataset.py dataset/labelbook/dataset.json