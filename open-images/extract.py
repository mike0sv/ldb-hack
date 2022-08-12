from itertools import count
from xml.dom import INDEX_SIZE_ERR
from PIL import Image
import os, json

path_folder = './open-images/'
path_dest = './processed'
json_files = [pos_json for pos_json in os.listdir(path_folder) if pos_json.endswith('.json')]

labels = {
    '/m/01tcjp': 'muffin',
    '/m/01yrx': 'cat',
    '/m/0bt9lr': 'dog',
    '/m/015wgc': 'croissant'
}

counts = {
    'muffin': 0,
    'cat': 0,
    'dog': 0,
    'croissant': 0,
}

failed = 0

for json_file in json_files:
    im_path = path_folder + json_file
    try:
        with open(im_path, 'r') as f:
            data = json.load(f)
            im = Image.open(im_path.replace('.json', '.jpg'))

            idx = 0
            for segment in data['detections']:
                if segment['LabelName'] not in labels: continue

                label = labels[segment['LabelName']].replace('/m/', '')

                width, height = im.size
                left = width * segment['XMin']
                top = height * segment['YMin']
                right = width * segment['XMax']
                bottom = height * segment['YMax']

                # Xcenter = (right - left) / 2
                # Ycenter = (bottom - top) / 2

                # left = max(0, Xcenter - 125)
                # top = max(0, Ycenter - 125)
                # right = max(width, Xcenter + 125)
                # bottom = max(height, Ycenter + 125)

                im1 = im.crop((left, top, right, bottom))
                width, height = im1.size
                if (width >= 256 and height >= 256):
                    path_class = path_dest + '/' + label
                    if not os.path.exists(path_class):
                        os.makedirs(path_class)
                
                    counts[label] += 1
                    im1.save(path_class + '/' + label + '-' + data['id'] + str(idx) + '.jpg')
                    idx += 1
    except Exception as err:
        print('failed file: ' + im_path)
        print(err)
        failed += 1

print(counts)
print(failed)

