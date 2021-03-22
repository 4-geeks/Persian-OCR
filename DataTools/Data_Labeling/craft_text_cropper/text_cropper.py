import sys
import os
import time
import argparse
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.autograd import Variable

from PIL import Image
import cv2
from skimage import io
import numpy as np
import craft_utils
import imgproc
import json
import zipfile

from craft import CRAFT
from collections import OrderedDict

def copyStateDict(state_dict):
    if list(state_dict.keys())[0].startswith("module"):
        start_idx = 1
    else:
        start_idx = 0
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = ".".join(k.split(".")[start_idx:])
        new_state_dict[name] = v
    return new_state_dict

def test_net(net, image, text_threshold, link_threshold, low_text, cuda, poly):
    t0 = time.time()

    # resize
    img_resized, target_ratio, size_heatmap = imgproc.resize_aspect_ratio(image, 1280, interpolation=cv2.INTER_LINEAR, mag_ratio=1.5)
    ratio_h = ratio_w = 1 / target_ratio

    # preprocessing
    x = imgproc.normalizeMeanVariance(img_resized)
    x = torch.from_numpy(x).permute(2, 0, 1)    # [h, w, c] to [c, h, w]
    x = Variable(x.unsqueeze(0))                # [c, h, w] to [b, c, h, w]
    if cuda:
        x = x.cuda()

    # forward pass
    with torch.no_grad():
        y, feature = net(x)

    # make score and link map
    score_text = y[0,:,:,0].cpu().data.numpy()
    score_link = y[0,:,:,1].cpu().data.numpy()

    # Post-processing
    boxes, polys = craft_utils.getDetBoxes(score_text, score_link, text_threshold, link_threshold, low_text, poly)

    # coordinate adjustment
    boxes = craft_utils.adjustResultCoordinates(boxes, ratio_w, ratio_h)
    polys = craft_utils.adjustResultCoordinates(polys, ratio_w, ratio_h)
    for k in range(len(polys)):
        if polys[k] is None: polys[k] = boxes[k]

    # render results (optional)
    render_img = score_text.copy()
    render_img = np.hstack((render_img, score_link))
    ret_score_text = imgproc.cvt2HeatmapImg(render_img)

    return boxes, polys, ret_score_text


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='craft_mlt_25k.pth', help='model path')
    parser.add_argument('--folder', type=str, default='data', help='dataset path')
    args = parser.parse_args()

    net = CRAFT()
    net.load_state_dict(copyStateDict(torch.load(args.model)))
    if True:
        net = net.cuda()
        net = torch.nn.DataParallel(net)
        cudnn.benchmark = False
    net.eval()

    os.makedirs('res', exist_ok=True)
    for item in tqdm(os.listdir(args.folder)):
        item_name = ''.join(item.split('.')[:-1])
        os.makedirs(f'res/{item_name}', exist_ok=True)
        counter = 0
        # craft
        image = imgproc.loadImage(args.folder + '/' + item)
        bboxes, polys, score_text = test_net(net, image, text_threshold=0.7, link_threshold=0.4, low_text=0.4, cuda=True, poly=False)
        for bbox in bboxes:
            xmin,ymin = bbox.min(0).astype(int)
            xmax,ymax = bbox.max(0).astype(int) 
            cv2.imwrite(f'res/{item_name}/{item_name}_{counter}.png', image[ymin:ymax, xmin:xmax][:,:,::-1])
            counter += 1
            
            # using polygon
            # bbox = bbox.reshape((-1, 1, 2)).astype(int)
            # isClosed = True
            # color = (255, 0, 0) 
            # thickness = 2
            # image = cv2.polylines(image, [bbox],isClosed, color, thickness) 
            # plt.imshow(image)
            # plt.show()