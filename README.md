# ldb-hack


Set up AWS credentials and python env
First time: run `init.sh`

Run `reproduce.sh` to reproduce datasets. It should create exact files in dataset/ (you can check it with diff)

Add new lines to `reproduce.sh` and rerun it

Commit everything. 
Add `sync` to commit message to upload datasets to team s3 bucket/repo/commit_sha
Add both `sync` and `submit` to commit message to trigger submit in hackaton repo
