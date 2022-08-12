import json

class_mapping = {
    "/m/0bt9lr": "dog",
    "/m/01yrx": "cat",
    "/m/015wgc": "croissant",
    "/m/01tcjp": "muffin",
}


def main():
    with open("google_prepared/dataset.json", "r") as f:
        data = json.load(f)

    new = []
    for obj in data:
        classes = [c for c in obj["annotation"]["classifications"] if
                   c["Confidence"] == 1 and c["LabelName"] in class_mapping]
        if len(classes) != 1:

            # drop multiclass
            continue
        obj["annotation"] = {"label": class_mapping[classes[0]["LabelName"]]}
        new.append(obj)

    with open("google_prepared/dataset.json", "w") as f:
        json.dump(new, f, indent=2)


if __name__ == '__main__':
    main()
