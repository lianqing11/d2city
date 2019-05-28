import os
import copy
import xml.etree.ElementTree as ET
import os.path as osp
import json
import argparse
import pdb
from tqdm import tqdm

import imageio
import glob

from PIL import Image

import multiprocessing


def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert d2city video to image')
    parser.add_argument(
        "--dir",
        default="../",
    )
    return parser.parse_args()




def generate_coco_file(test_imgs, file_dir):
    image_num = len(test_imgs)
    images = list()
    for idx, img in tqdm(enumerate(test_imgs)):
        image = dict()
        image['file_name'] = img
        img = Image.open(osp.join(file_dir, img))
        image['height'] = img.size[1]
        image['width'] = img.size[0]
        image['id'] = idx+1
        images.append(image)
    attr_dict = {}
    attr_dict["categories"] = [
        {"supercategory": "none", "id": 1, "name": "car"},
        {"supercategory": "none", "id": 2, "name": "bus"},
        {"supercategory": "none", "id": 3, "name": "truck"},
        {"supercategory": "none", "id": 4, "name": "person rider"},
        {"supercategory": "none", "id": 5, "name": "bike"},
        {"supercategory": "none", "id": 6, "name": "motor"},
    ]
    attr_dict['images'] = images
    attr_dict['type'] = "instances"
    return attr_dict



if __name__ == '__main__':
    args = parse_arguments()

    test_img = glob.glob(osp.join(args.dir + "0009/*.jpg"))
    test_img_id = [i.split(args.dir)[1] for i in test_img]
    test_img_id.sort()
    attr_dict = generate_coco_file(test_img_id, args.dir)
    json_string = json.dumps(attr_dict)
    with open("test_0009.json", 'w') as f:
        f.write(json_string)

    test_img = glob.glob(osp.join(args.dir + "0010/*.jpg"))
    test_img_id = [i.split(args.dir)[1] for i in test_img]
    test_img_id.sort()
    attr_dict = generate_coco_file(test_img_id, args.dir)
    json_string = json.dumps(attr_dict)
    with open("test_0010.json", 'w') as f:
        f.write(json_string)

