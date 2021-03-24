import numpy as np
import PIL
import arabic_reshaper
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
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

def create_word(word, font_name ,O_old = (0,0), offsets = (0,0) ,for_size_detection = False , bg = None ,shift = True ,size = 60, color = None , bg_size = (100,300), bg_color = (200)):
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
#     o_x_offset, o_y_offset = offsets
#     print(background.size)
#     print(o_x_offset,o_y_offset)
#     o_x_offset = -int(o_x_offset * background.size[0])
#     o_y_offset = -int(o_y_offset * background.size[1])
#     print(o_x_offset,o_y_offset)
#     x, y = background.size[0]//2 + o_x_offset ,background.size[1]//2 + o_y_offset
    if not for_size_detection:
        O_old = np.array(O_old)
        x, y = np.array(background.size) // 2 - O_old
    else:
        x,y = 0,0
    if shift:
        x = x + int(np.random.randint(low = -background.size[0]//30, high = background.size[0]//30, size = 1))
        y = y + int(np.random.randint(low = -background.size[1]//30, high = background.size[1]//30, size = 1))
    draw.text((x, y), bidi_text, fill=color, font=font)
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
        try:
            file = open(txt_file, encoding="utf8")
            lines = file.read()
        except:
            file = open(txt_file)
            lines = file.read()
        
        all_words.extend(lines.split('\n'))
#     print(f'Found {len(all_words)} words in the dataset.')
    all_words = list(filter(lambda x:len(x), all_words))
    return all_words

def img_to_bbx(img):
    img = np.array(img)
    args = np.argwhere(img[...,0]>0)
    y_max, x_max = np.max(args,0)
    y_min, x_min = np.min(args,0)
#     plt.imshow(img[y_min:y_max, x_min:x_max,:])
#     plt.imshow(img)
    bbx = (x_min,x_max), (y_min, y_max)
#     print(y_min,y_max)
    
#     
    o_x_offset = ((x_min + x_max) / img.shape[1] ) - 1
    o_y_offset = ((y_min + y_max) / img.shape[0] ) - 1
    offsets = [o_x_offset , o_y_offset]
#     print(o_x_offset,o_y_offset)
    sizes = np.array((y_max- y_min, x_max - x_min))
    return offsets, sizes, bbx

def get_rect_size_for_word(word, font, size, bg_size = None):
    if bg_size is None:
        bg_size = (400, 70 * len(word))
        bg_size = np.array(bg_size) * (1+size / 200)
        bg_size = tuple((np.array(bg_size)).astype(int))
    img = create_word(word, font_name = font,shift = False, size = size, color = (255,255,255), 
                bg_size = bg_size, bg_color = (0,0,0), O_old = (0,0), for_size_detection = True)
    offsets, sizes, bbx = img_to_bbx(img)
    (x_min,x_max), (y_min, y_max) = bbx
    O_old = np.array([(x_min+x_max)//2 , (y_min + y_max)//2])
#     O_target = np.array(bg_size)[::-1] // 2
#     x_new, y_new = O_target - O_old
    return O_old , sizes


def resize_bg(backgroud_img, target_size, x_factor = None, y_factor = None):
    bg  = backgroud_img.copy()
    y,x = target_size.astype(int)
    if x_factor is None:
        x_factor = 1.1 + np.random.rand() / 6
    if y_factor is None:
        y_factor = 1.2 + np.random.rand() / 4
    x = int(x*x_factor)
    y = int(y*y_factor)       
    bg  = cv2.resize(bg, (x,y))
    bg = Image.fromarray(bg)
    return bg


def augment(img, p = 0.5):
    filters = [ImageFilter.GaussianBlur(), ImageFilter.SHARPEN()]
    epsilon = np.random.rand(1)
    if epsilon < p:
        epsilon = int(epsilon * len(filters))
        f = filters[epsilon]
        if f.name == 'GaussianBlur':
            f.radius = np.random.rand(1) * 1.5
        img = img.filter(f)
        
        epsilon = np.random.rand(1)
        if epsilon < 0.4:
            img = img.rotate(np.random.randint(-4,4,1))

        epsilon = np.random.rand(1)
        if epsilon < 0.4:
            img = ImageEnhance.Contrast(img).enhance(np.random.rand(1) + 0.5)
    
    return img

def create_data_set(words, fonts, bgs ,size = None, noise_p = 0.5 ,output_dir = 'outputs/'):
    t1 = t()
    counter = 0
    os.makedirs(output_dir , exist_ok = True)
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
    print(f'Found {len(words)} words.')
    print(f'Found {len(fonts)} fonts.')
    print(f'Found {len(bgs)} background images.')
    print(f'In total {len(words) * len(fonts) * len(bgs)} Images will be created')
    for w_idx, word in enumerate(tqdm(words)):
        for f_idx, font in enumerate(fonts):
            for bg_idx, bg in enumerate(bgs):
                if isinstance(size, int):
                    pass
                elif size == 'random' or size is None:
                    size = int(np.random.randint(110,150,1))
                    
                O_old, sizes = get_rect_size_for_word(word, font, size)
                bg = resize_bg(bg, sizes)
                img = create_word(word, font_name = font,bg = bg, size= int(size//1.0) , O_old = O_old)
                img = augment(img, p = noise_p)
                img.save(os.path.join(output_dir , f'w_{w_idx:04d}f_{f_idx:04d}b_{bg_idx:04d}.png' ))
                counter += 1
    print(f'{counter} Images created')
    t2 = t()
    print(f'Time Taken : {np.round(t2-t1,2)} second')