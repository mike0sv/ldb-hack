import sys
import urllib.request
from csv import reader
from PIL import Image
from os.path import exists

csv_filename = sys.argv[1]
idx = 0
size = 400
with open(csv_filename, 'r') as csv_file:
    for line in reader(csv_file):
        try:
            im_path = str(idx) + '.png'
            if exists(im_path):
                idx += 1 
                continue

            req = urllib.request.Request(
                line[0], 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            im = Image.open(urllib.request.urlopen(req,timeout=3))
            im.thumbnail((size, size), Image.ANTIALIAS)
            im.save(im_path)
            print("Image saved for {0}".format(line[0]))
            idx += 1
        except Exception as e:
            print('Failed ' + line[0])
            print(e)

