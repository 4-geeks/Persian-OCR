import numpy as np
import PIL
import arabic_reshaper
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from bidi.algorithm import get_display
import os
from glob import glob
import cv2
from tqdm import tqdm
import sys
from time import time as t
if 'ipykernel' in sys.modules:
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm

def create_word(word, font_name, bg = None , size = 60 , word_loc = (0,0), color = None , bg_size = (100,300), bg_color = (200)):
    if bg is None:
        bg_size = np.array(bg_size).astype(int)
        background = np.ones((*bg_size,3) , dtype = 'uint8') * bg_color
        background = background.astype('uint8')
        background = Image.fromarray(background)
    else : background = bg
    
    if color is None:
        color = tuple(np.random.randint(low = 0, high = 70, size = 3))
    
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype(font_name, size=size)
    reshaped_text = arabic_reshaper.reshape(word)
    bidi_text = get_display(reshaped_text)
    x, y = bg_size[1]//2 , (bg_size[0]) //2
    x = x + int(np.random.randint(low = 0, high = bg_size[1]//15, size = 1))
    y = y - int(np.random.randint(low = bg_size[1]//35, high = bg_size[1]//20, size = 1))
    draw.text((x, y), bidi_text, fill=color, font=font, anchor = 'mm')
    return background

def get_all_fonts(fonts_dir):
    fonts_names = glob(os.path.join(fonts_dir , '*ttf'))
#     print(f'Found {len(fonts_names)} fonts in the given directory')
    return fonts_names

def get_all_bgs(bgs_dir):
    bgs_names = glob(os.path.join(bgs_dir , '*'))
#     print(f'Found {len(bgs_names)} backgrounds in the given directory')
    all_imgs = []
    for bg_name in bgs_names:
        bg = cv2.imread(bg_name)[...,::-1]
        all_imgs.append(bg)
    return all_imgs

def get_all_words(corpuses_dir):
    all_words = []
    corpus_names = glob(os.path.join(corpuses_dir , '*txt'))
    print(f'There are {len(corpus_names)} text files in the corpus')
    for txt_file in corpus_names:
        file = open(txt_file)
        lines = file.read()
        all_words.extend(lines.split('\n'))
#     print(f'Found {len(all_words)} words in the dataset.')
    return all_words

def img_to_bbx(img):
    img = np.array(img)
    args = np.argwhere(img[...,0]>0)
    y_max, x_max = np.max(args,0)
    y_min, x_min = np.min(args,0)
#     plt.imshow(img[y_min:y_max, x_min:x_max,:])
    bbx = (x_min,x_max), (y_min, y_max)
    sizes = np.array((y_max- y_min, x_max - x_min))
    return bbx, sizes

def get_rect_size_for_word(word, font, size):
    img = create_word(word, font_name = font, size = size, color = (255,255,255), 
                bg_size = (400,700), bg_color = (0,0,0) )
    return img_to_bbx(img)

def resize_bg(backgroud_img, target_size):
    bg  = backgroud_img.copy()
    y,x = target_size.astype(int)
    bg  = cv2.resize(bg, (x,y))
    bg = Image.fromarray(bg)
    return bg

def add_random_noise(img, p = 0.5):
    filters = [ImageFilter.GaussianBlur(), ImageFilter.SHARPEN()]
    epsilon = np.random.rand(1)
    if epsilon < 0.5:
        epsilon = int(epsilon * len(filters))
        f = filters[epsilon]
        if f.name == 'GaussianBlur':
            f.radius = np.random.rand(1) * 1.5
        img = img.filter(f)
    return img

def create_data_set(words, fonts, bgs ,size = None, noise_p = 0.5 ,output_dir = 'outputs/'):
    t1 = t()
    counter = 0
    print('Output directory craeted.')
    assert isinstance(words, str) or isinstance(all_words, list) , "words argument should be either list or str"
    if isinstance(words, str):
        words = get_all_words(words)
    assert isinstance(fonts, str) or isinstance(fonts, list)  , "fonts argument should be either list or str"
    if isinstance(fonts, str):
        fonts = get_all_fonts(fonts)
    assert isinstance(bgs, str) or isinstance(bgs, list)  , "bgs argument should be either list or str"
    if isinstance(bgs, str):
        bgs = get_all_bgs(bgs)
    os.makedirs(output_dir , exist_ok = True)
    print(f'Found {len(words)} words.')
    print(f'Found {len(fonts)} fonts.')
    print(f'Found {len(bgs)} background images.')
    print(f'In total {len(words) * len(fonts) * len(bgs)} Images will be created')
    for w_idx, word in enumerate(tqdm(words)):
        for f_idx, font in enumerate(fonts):
            for bg_idx, bg in enumerate(bgs):
                if isinstance(size, str):
                    pass
                elif isinstance(size, list):
                    size = np.random.choice(size)
                elif size == 'random' or size is None:
                    size = int(np.random.randint(110,150,1))
                    
                bbx, sizes = get_rect_size_for_word(word, font, size)
                bg = resize_bg(bg, 1.2 * sizes)
                img = create_word(word, font_name= font,bg = bg, bg_size = 1.2*sizes, size= int(size//1.2))
                img = add_random_noise(img, p = noise_p)
                img.save(os.path.join(output_dir , f'w_{w_idx:04d}f_{f_idx:04d}b_{bg_idx:04d}.png' ))
                counter += 1
    print(f'{counter} Images created')
    t2 = t()
    print(f'Time Taken : {np.round(t2-t1,2)} second')