import json
import argparse
import random
import numpy as np

def parse_arguments():
    parser = argparse.ArgumentParser(description='BDD100K to COCO format')
    parser.add_argument(
          "-l", "--label_dir",
          default="val_label_transfer.json",
          help="root directory of BDD label Json files",
    )
    return parser.parse_args()


args = parse_arguments()
val = json.load(open(args.label_dir))
images = val['images']
sample_images = np.random.choice(images, 100, replace=False)
sample_images_id = [i['id'] for i in sample_images]
annotations = val['annotations']
sample_annotation = []
for i in annotations:
    if i['image_id'] in sample_images_id:
        sample_annotation.append(i)

attr_dict = {}
attr_dict['images'] = list(sample_images)
attr_dict['annotations'] = sample_annotation
attr_dict['type'] = "instances"
attr_dict['categories'] = val['categories']
json_string = json.dumps(attr_dict)
with open("val_label_transfer_sample.json", 'w') as f:
    f.write(json_string)
