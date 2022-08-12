import json
from collections import Counter

DATASETS = {
    "s3://ldb-public/remote/data-lakes/open-images": "open-images",
    "s3://ldb-public/remote/data-lakes/hackathon-starter": "started",
    "s3://ldb-public/remote/data-lakes/chihuahua_vs_muffin": "chihuahua_vs_muffin",
    "s3://ldb-public/remote/data-lakes/ISIA_500": "isia500",
    "s3://ldb-hackathon-team-6/data-lakes/serge": "serge",
    "s3://ldb-hackathon-team-6/data-lakes/domas": "domas",
    "s3://ldb-hackathon-team-6/data-lakes/david": "david",
    "s3://ldb-hackathon-team-6/data-lakes/oded": "oded",
    "s3://ldb-public/remote/data-lakes/Stanford-dog-breeds": "stanford"
}

def get_dataset(path):
    for d in DATASETS:
        if path.startswith(d):
            return DATASETS[d]
    return path

def main():
    all_hashes = Counter()
    for split in ["train", "val", "labelbook"]:
        with open(f"dataset/{split}/dataset.json") as f:
            data = json.load(f)

            print(split, len(data))
            counts = Counter(o["annotation"]["label"] for o in data)
            print("\n".join(
                f"{k}: {v / len(data) * 100:.2f}" for k, v in counts.items()))
            print()

            datasets = Counter(get_dataset(o["data-object-info"]["path"]) for o in data)
            print("\n".join(
                f"{k}: {v / len(data) * 100:.2f}" for k, v in datasets.items()))
            print()
            print()

            all_hashes.update(o["data-object-info"]["md5"] for o in data)

    print({k: v for k, v in all_hashes.items() if v > 1})


if __name__ == '__main__':
    main()
