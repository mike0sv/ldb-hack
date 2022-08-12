set -exu

export LDB_DIR=.ldb
# export AWS_PROFILE if not set
export AWS_PROFILE="${AWS_PROFILE:-hackathon-team-6}"

mkdir -p tmp

# instantiate non refused, filter by croissant, change this to whatever
ldb instantiate ds:root --tag oded --no-tag refuse --query 'label == `croissant`' --target tmp/oded
ldb instantiate ds:root --tag david --no-tag refuse --query 'label == `croissant`' --target tmp/david
ldb instantiate ds:root --tag serge --no-tag refuse --query 'label == `croissant`' --target tmp/serge
ldb instantiate ds:root --tag domas --no-tag refuse --query 'label == `croissant`' --target tmp/domas

ldb instantiate ds:root --tag starter --no-tag refuse --query 'label == `croissant`' --target tmp/starter

# you'll catch the culprit by the path name :), then refuse the images in reproduce.sh
python ./verify_images.py tmp