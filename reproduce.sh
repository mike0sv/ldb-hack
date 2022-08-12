set -exu

export LDB_DIR=.ldb


# starter baseline - but cleaned
AWS_PROFILE=hackathon-team-6 ldb index s3://ldb-hackathon-team-6/clean-up/train --format annot -p single-file=true --add-tag starter
AWS_PROFILE=hackathon-team-6 ldb index s3://ldb-hackathon-team-6/clean-up/val --format annot -p single-file=true --add-tag starter
AWS_PROFILE=hackathon-team-6 ldb index s3://ldb-hackathon-team-6/clean-up/labelbook --format annot -p single-file=true --add-tag starter

# personal images
AWS_PROFILE=hackathon-team-6 ldb index s3://ldb-hackathon-team-6/data-lakes/serge --format infer --add-tag serge
AWS_PROFILE=hackathon-team-6 ldb index s3://ldb-hackathon-team-6/data-lakes/domas --format infer --add-tag domas
AWS_PROFILE=hackathon-team-6 ldb index s3://ldb-hackathon-team-6/data-lakes/oded --format infer --add-tag oded

# refuse invalid images (see verify_images.py)
ldb tag ds:root --tag domas --query 'label == `croissant`' --path "Image_114|Image_153|Image_135|Image_139|Image_120|Image_155|Image_112" --add refuse
ldb tag ds:root --tag serge --query 'label == `cat`' --path "Abyssinian_67|Persian_269" --add refuse
ldb tag ds:root --tag serge --query 'label == `croissant`' --path "croissant_61|croissant_75|croissant_11|croissant_12|croissant_13|/croissant_21" --add refuse
ldb tag ds:root --tag serge --query 'label == `muffin`' --path "muffin_13|muffin_215|muffin_361|muffin_73|muffin_299|muffin_115|muffin_130|muffin_294|muffin_185|muffin_344|muffin_23|muffin_5" --add refuse


# kaggle - chihuahua vs muffin: correctly labeled - dog (279) and muffin (273)
ldb index s3://ldb-public/remote/data-lakes/chihuahua_vs_muffin/ --format infer --add-tag kaggle,chihuahua_vs_muffin

# refuse invalid images (see verify_images.py)
ldb tag ds:root --tag chihuahua_vs_muffin --query 'label == `dog`' --path "00000057|00000020|00000050|00000333|00000088" --add refuse
ldb tag ds:root --tag chihuahua_vs_muffin --query 'label == `muffin`' --path "00000059|00000074|00000208|00000075|00000099" --add refuse

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
ldb index google_prepared/ --format annot -p single-file=true --add-tag google

# refusing invalid webp files
ldb tag ds:root --path ".webp" -a refuse

ldb eval -j --query label ds:root --no-tag refuse  --query "label" | sort | uniq -c

python reset_and_resplit.py
