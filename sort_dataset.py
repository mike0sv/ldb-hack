import json
import sys


def main():
    path = sys.argv[1]

    with open(path, "r") as new:
        new_data = json.load(new)

    with open(path, "w") as old:
        json.dump(
            sorted(new_data, key=lambda x: x["data-object-info"]["path"]), old, indent=2)


if __name__ == '__main__':
    main()
