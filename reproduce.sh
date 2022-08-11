set -exu

export LDB_DIR=.ldb


ldb index s3://ldb-hackathon-team-6/clean-up/train --format annot -p single-file=true --add-tag train
ldb index s3://ldb-hackathon-team-6/clean-up/val --format annot -p single-file=true --add-tag val
ldb index s3://ldb-hackathon-team-6/clean-up/labelbook --format annot -p single-file=true --add-tag labelbook
#ldb index s3://ldb-public/remote/data-lakes/chihuahua_vs_muffin/ --format infer --add-tag kaggle

rm -rf dataset/train
rm -rf dataset/val
rm -rf dataset/labelbook
ldb instantiate ds:root --tag train --format annot -p single-file=true -t dataset/train/
ldb instantiate ds:root --tag val --format annot -p single-file=true -t dataset/val/
ldb instantiate ds:root --tag labelbook --format annot -p single-file=true -t dataset/labelbook/
python sort_dataset.py dataset/train/dataset.json
python sort_dataset.py dataset/val/dataset.json
python sort_dataset.py dataset/labelbook/dataset.json