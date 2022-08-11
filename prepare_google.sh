set -exu

export LDB_DIR=.ldb

ldb index s3://ldb-public/remote/data-lakes/open-images/ --add-tag google,train
mkdir google
ldb instantiate ds:root --tag google --query 'contains(detections[*].LabelName,`/m/0bt9lr`)' -t google/dog
ldb instantiate ds:root --tag google --query 'contains(detections[*].LabelName,`/m/01yrx`)' -t google/cat
ldb instantiate ds:root --tag google --query 'contains(detections[*].LabelName,`/m/015wgc`)' -t google/croissant
ldb instantiate ds:root --tag google --query 'contains(detections[*].LabelName,`/m/01tcjp`)' -t google/muffin
find google/ -name '*.json' -type f -delete
ldb index google/ --format tensorflow-inferred --annotation-update merge

ldb instantiate ds:root --tag google --format annot -p single-file=true -t google_prepared/

python prepare_google_dataset.py