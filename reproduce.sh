set -exu

export LDB_DIR=.ldb


# starter baseline - but cleaned
AWS_PROFILE=hackathon-team-6 ldb index s3://ldb-hackathon-team-6/clean-up/train --format annot -p single-file=true
AWS_PROFILE=hackathon-team-6 ldb index s3://ldb-hackathon-team-6/clean-up/val --format annot -p single-file=true
AWS_PROFILE=hackathon-team-6 ldb index s3://ldb-hackathon-team-6/clean-up/labelbook --format annot -p single-file=true

# personal images
AWS_PROFILE=hackathon-team-6 ldb index s3://ldb-hackathon-team-6/data-lakes/serge --format infer --add-tag serge
AWS_PROFILE=hackathon-team-6 ldb index s3://ldb-hackathon-team-6/domas --format infer --add-tag domas
AWS_PROFILE=hackathon-team-6 ldb index s3://ldb-hackathon-team-6/data-lakes/oded --format infer --add-tag oded

# kaggle - chihuahua vs muffin: correctly labeled - dog (279) and muffin (273)
ldb index s3://ldb-public/remote/data-lakes/chihuahua_vs_muffin/ --format infer --add-tag kaggle,chihuahua_vs_muffin

# stanford - labeled by dog breads (10800 objects, check out stanford_breeds_count.txt for counts)
# I picked some large breeds in random
# TODO - add the entire dataset?
ldb index s3://ldb-public/remote/data-lakes/Stanford-dog-breeds/n02109525-Saint_Bernard/ --format infer --param base-label=dog --add-tag stanford
ldb index s3://ldb-public/remote/data-lakes/Stanford-dog-breeds/n02091831-Saluki/ --format infer --param base-label=dog --add-tag stanford
ldb index s3://ldb-public/remote/data-lakes/Stanford-dog-breeds/n02093256-Staffordshire_bullterrier/ --format infer --param base-label=dog --add-tag stanford
ldb index s3://ldb-public/remote/data-lakes/Stanford-dog-breeds/n02110185-Siberian_husky/ --format infer --param base-label=dog --add-tag stanford
ldb index s3://ldb-public/remote/data-lakes/Stanford-dog-breeds/n02092339-Weimaraner/ --format infer --param base-label=dog --add-tag stanford

# those maybe similar to cats
ldb index s3://ldb-public/remote/data-lakes/Stanford-dog-breeds/n02086910-papillon/ --format infer --param base-label=dog --add-tag stanford
ldb index s3://ldb-public/remote/data-lakes/Stanford-dog-breeds/n02115913-dhole/ --format infer --param base-label=dog --add-tag stanford

# google open images
ldb index google_prepared/ --format annot -p single-file=true --add-tag train

ldb eval -j --query label ds:root | sort | uniq -c

python reset_and_resplit.py
