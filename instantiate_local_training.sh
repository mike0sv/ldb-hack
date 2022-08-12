set -exu

export LDB_DIR=.ldb
export AWS_PROFILE=hackathon-team-6

rm -rf data/*

ldb instantiate ds:root --tag train --no-tag refuse --target data/train --format tensorflow-inferred
ldb instantiate ds:root --tag val --no-tag refuse --target data/val --format tensorflow-inferred
ldb instantiate ds:root --tag labelbook --no-tag refuse --target data/labelbook --format tensorflow-inferred

python verify_images.py data
