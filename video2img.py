import os
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
        save_dir = save_dir+ "_{}.jpg".format(num)
        img = Image.fromarray(img)
        img.save(save_dir)



if __name__ == '__main__':
    args = parse_arguments()

    video_list = glob.glob(args.dir + "000*/*.mp4")
    print("transfer video num {}".format(len(video_list)))

    p = multiprocessing.Pool(48)
    b = p.map(convert, video_list)
    print("final transformation")

