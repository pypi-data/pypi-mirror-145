import torch
import torchvision.transforms as transforms
import numpy as np
from PIL import Image
import cv2
import os
import os.path as osp

import json
import pickle

def readByLines(file_name, strip=True):
    with open(file_name, 'r') as f:
        f_lines = f.readlines()
    if strip:
        return [line.strip() for line in f_lines]
    else:
        return f_lines

def read_json(json_file):
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    return json_data

def read_pkl(pkl_file):
    with open(pkl_file, 'rb') as f:
        pkl_data = pickle.load(f)
    return pkl_dat

def readSingleImagePIL(image_path, rgb=True):
    img = Image.open(image_path)
    if rgb:
        return img.convert("RGB") 
    else:
        return img

def readSingleImageCV2(image_path):
    img = cv2.imread(image_path)
    img = img[:, :, ::-1]       # bgr 2 rgb
    return img

def readTensorImage(image_path, expand=False, through='pil', transform=None, size=None):
    if through == 'pil':
        img = readSingleImagePIL(image_path)
        img_tensor = pil2tensor(img, transform, size)
    elif through == 'opencv':
        arr = readSingleImageCV2(image_path)
        img_tensor = cv2tensor(arr.copy())
    else:
        raise KeyError

    if expand:
        return img_tensor.unsqueeze(dim=0)
    else:
        return img_tensor

def readBatchImages(images_dir, rgb=False):
    images_list = os.listdir(images_dir)
    for image_name in imaegs_list:
        image_path = osp.join(images_dir, image_name)
    # TODO

def cv2tensor(arr, transform=None):
    if transform is not None:
        return transform(arr)
    else:
        arr = arr.transpose(2, 0, 1).astype(np.float32) / 255.  # HWC 2 CHW && normalize
        img_tensor = torch.from_numpy(arr)
        return img_tensor

def tensor2cv(img_tensor, convert_rgb=True):
    arr = img_tensor.detach().permute(1, 2, 0).numpy() * 255.
    if convert_rgb:
        return arr[:, :, ::-1]
    else:
        return arr

def pil2tensor(img, transform=None, size=None):
    if size is not None:
        p = transforms.Resize(size)
        img = p(img)
    if transform is not None:
        img_tensor = transform(img)
    else:
        img_tensor = transforms.functional.to_tensor(img)
    return img_tensor

def tensor2pil(img_tesnor):
    img = transforms.functional.to_pil_image(img_tensor)
    return img

def getTransforms(crop=None, resize=None):
    t = []
    if crop is not None:
        t.append(transforms.Crop(crop))
    if resize is not None:
        t.append(transforms.Resize(resize))

    return transforms.Compose(t)

def save_tensor_image(path, tensor):
    img = tensor.permute(1, 2, 0).numpy()[:, :, ::-1] * 255.
    cv2.imwrite(path, img)



if __name__ == "__main__":
    image_path = "/ssd1t/song/Datasets/AVA/shortEdge256/125.jpg"
    ten = readTensorImage(image_path, through="opencv")
    img = tensor2cv(ten, True)
    cv2.imwrite("test.jpg", img)

