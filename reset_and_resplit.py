#!/usr/bin/env python3

import math
import shutil
import subprocess
import collections

obj_classes = ["croissant", "muffin", "dog", "cat"]
splits = ["train", "val", "labelbook"]


def _echo_check_output(cmd):
    print(f"Running: {cmd}")
    result = subprocess.check_output(cmd, shell=True)
    print(result.decode())
    return result


def reset_split_datasets():
    print("Resetting train/va/labelbook tags")
    cmd = "ldb tag ds:root -r train,val,labelbook"
    _echo_check_output(cmd)


def split_datasets():
    print("Getting totals")
    totals = {}
    for obj_class in obj_classes:
        cmd = f"ldb list ds:root --summary --query 'label == `{obj_class}`'"
        out = _echo_check_output(cmd)
        totals[obj_class] = int(out.strip())
    print(f"Totals: {totals}")

    # ## split what's in your ds:root 60|20|20
    # because of ldb limit bug we'll take train last and not use --limit there
    split_weights = collections.OrderedDict([
        ("val", 0.2),
        ("labelbook", 0.2),
        ("train", 0.6),
    ])
    for split in split_weights:
        no_tags_args = " ".join([f"--no-tag {s}" for s in splits if s != split]).strip()
        for obj_class in ["croissant", "muffin", "dog", "cat"]:

            limit_arg = "--limit " + str(math.ceil(totals[obj_class] * split_weights[split]))

            # for the last split (train) - don't use limit, ldb's limit got some weird bugs, and we'll get unused
            # images
            if split == list(split_weights.keys())[-1]:
                limit_arg = ""

            cmd = f"ldb tag ds:root --query 'label == `{obj_class}`' --shuffle {limit_arg} {no_tags_args} --add {split}"
            _echo_check_output(cmd)

    # untagged images :\
    for obj_class in obj_classes:
        cmd = f"ldb list ds:root --summary --query 'label == `{obj_class}`' " \
              f"--no-tag val --no-tag train --no-tag labelbook"
        out = _echo_check_output(cmd)
        print(f"We've got {int(out)} unused {obj_class} images (out of {totals[obj_class]})!")


def instantiate_datasets():
    """
    This will override ./dataset contents !!
    """
    for split in splits:
        shutil.rmtree(f"dataset/{split}")
        cmd = f"ldb instantiate ds:root --tag {split} --format annot " \
              f"--param single-file=true --target dataset/{split}"
        _echo_check_output(cmd)


def main():
    reset_split_datasets()
    split_datasets()
    instantiate_datasets()


if __name__ == "__main__":
    main()
