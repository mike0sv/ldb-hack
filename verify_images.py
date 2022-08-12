#!/usr/bin/env python3

from pathlib import Path
import imghdr
import sys


def main(data_dir):
    img_type_accepted_by_tf = ["bmp", "gif", "jpeg", "png"]
    print(f"Checking {data_dir}...\n")
    invalid_images = 0
    for filepath in Path(data_dir).rglob("**/*"):
        if not filepath.is_file():
            continue
        invalid = False

        img_type = imghdr.what(filepath)
        if img_type is None:
            print(f"{filepath} is not an image")
            invalid = True
        elif img_type not in img_type_accepted_by_tf:
            print(f"{filepath} is a {img_type}, not accepted by TensorFlow")
            invalid = True
        if invalid:
            invalid_images += 1
            # filepath.unlink()

    if invalid_images:
        print(f"found {invalid_images} invalid images")
        exit(1)


if __name__ == "__main__":

    test_data = None
    if len(sys.argv) >= 2:
        test_data = sys.argv[1]
    else:
        print(f"Usage: python {sys.argv[0]} <some data directory>")
        quit()

    main(test_data)
