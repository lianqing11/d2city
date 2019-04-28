import os
import copy
import xml.etree.ElementTree as ET
import json
import argparse
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



def convert(i):
    print(i)
    vid = imageio.read(i)
    for num, img in enumerate(vid.iter_data()):
        save_dir = i.split(".mp4")[0]
        save_dir = save_dir+ "_{}.png".format(num)
        img = Image.fromarray(img)
        img.save(save_dir)

def dd2coco(images, xml_file):
    id2images = copy.deepcopy(images)
    id2images = [''].extend(id2images)
    image_num = len(images)
    image2id = {images[i]: i+1 for i in range(image_num)}
    images = list()
    empty_images = []
    annotations = list()
    annotation_id = 1
    for xml_name in tqdm(xml_file):
        frame_name = xml_name.split(args.dir)[-1].split(".xml")[0]
        xml = ET.parse(xml_name).getroot()
        meta = xml[1]
        invalid_label = set()
        frame_num = int(meta[0].text)
        width = int(meta[1].text)
        height = int(meta[2].text)
        for track_list in xml[2:]:
            track_label = track_list.attrib['label']
            if track_label not in label2id.keys():
                invalid_label.add(track_label)
                continue
            track_label_id = label2id[track_label]

            for track in track_list:
                annotation = dict()
                attrib = track.attrib
                frame = attrib['frame']
                x1 = int(float(attrib['xtl']))
                y1 = int(float(attrib['ytl']))
                x2 = int(float(attrib['xbr']))
                y2 = int(float(attrib['ybr']))
                annotation['image_id'] = image2id[frame_name+"_{}.png".format(frame)]
                annotation['area'] = float((x2-x1) * (y2-y1))
                annotation['bbox'] = [x1, y1, x2-x1, y2-y1]
                annotation['id'] = annotation_id
                annotation_id+=1
                annotation['ignore'] = 0
                annotation['segmentation'] = [[x1, y1, x1, y2, x2, y2, x2, y1]]
                annotation['category_id'] = track_label_id
                annotations.append(annotation)

        for frame_id in range(frame_num):
            image = dict()
            image['file_name'] = frame_name+'_{}.png'.format(frame_id)
            image['height'] = height
            image['width'] = width
            image['id'] = image2id[image['file_name']]
            images.append(image)
    attr_dict = {}
    attr_dict['images'] = images
    attr_dict['annotations'] = annotations
    attr_dict['type'] = "instances"
    return attr_dict


if __name__ == '__main__':
    args = parse_arguments()
    train_image_id = []
    train_xmls = []
    label2id = {}
    label2id['car'] = 3
    label2id['bus'] = 4
    label2id['truck'] = 5
    label2id['van'] = 3
    label2id['person'] = 1
    label2id['bicycle'] = 6
    label2id['motorcycle'] = 7
    label2id['open-tricycle'] = 7
    label2id['closed-tricycle'] = 7
    for i in range(7):
        train_image_id.extend(glob.glob(args.dir + "/000{}/*.png".format(i)))
        train_xmls.extend(glob.glob(args.dir + "/000{}/*.xml".format(i)))
    train_image_id = [i.split(args.dir)[1] for i in train_image_id]
    dd2coco(train_image_id, train_xmls)
    val_image_id = glob.glob(args.dir + "/0008/*.png")
    val_xml = glob.glob(args.dir + "/0008*.xml")
    dd2coco(val_image_id, val_xmls)
