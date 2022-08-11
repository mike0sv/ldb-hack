#!/usr/bin/env python3

import json
import os.path
import math
import shutil
import subprocess

obj_classes = ["croissant", "muffin", "dog", "cat"]
split_weights = {"train": 0.6, "val": 0.2, "labelbook": 0.2}


def _echo_check_output(cmd):
    print(f"Running: {cmd}")
    result = subprocess.check_output(cmd, shell=True)
    print(result.decode())
    return result


def reset_split_datasets():
    print("Resetting train/val/labelbook tags")
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

    # split what's in your ds:root 60|20|20
    for split in split_weights:
        no_tags_args = " ".join([f"--no-tag {s}" for s in split_weights if s != split]).strip()
        for obj_class in ["croissant", "muffin", "dog", "cat"]:
            limit_arg = "--limit " + str(math.ceil(totals[obj_class] * split_weights[split]))

            cmd = f"ldb tag ds:root --query 'label == `{obj_class}`' {no_tags_args} --shuffle --add {split} {limit_arg}"
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

    def sort_dataset(path):
        with open(path, "r") as new:
            new_data = json.load(new)

        with open(path, "w") as old:
            json.dump(sorted(new_data, key=lambda x: x["data-object-info"]["path"]), old, indent=2)
        print(f"{path} dataset sorted")

    for split in split_weights:
        split_ds_path = f"dataset/{split}"
        shutil.rmtree(split_ds_path)
        cmd = f"ldb instantiate ds:root --tag {split} --format annot " \
              f"--param single-file=true --target {split_ds_path}"
        _echo_check_output(cmd)

        # sort it
        dataset_annotation_file = os.path.join(split_ds_path, "dataset.json")
        sort_dataset(dataset_annotation_file)


def main():
    reset_split_datasets()
    split_datasets()
    instantiate_datasets()


if __name__ == "__main__":
    main()
