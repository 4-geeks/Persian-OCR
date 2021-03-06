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
import json
import datetime
from time import time as t
if 'ipykernel' in sys.modules:
    from tqdm.notebook import tqdm
else:
    from tqdm import tqdm

def create_word(word, font_name ,sizes = None ,O_old = (0,0),
                for_size_detection = False , bg = None ,shift = True ,
                size = 60, color = None , bg_size = (100,300), bg_color = (200),
                size_factor = 1.2, tight = False):
    if bg is None:
        bg_size = np.array(bg_size).astype(int)
        background = np.ones((*bg_size,3) , dtype = 'uint8') * bg_color
        background = background.astype('uint8')
        background = Image.fromarray(background)
    else : background = bg
    
    if color is None:
        color = tuple(np.random.randint(low = 0, high = 70, size = 3))
    
    
    if not for_size_detection:
        O_old = np.array(O_old) // size_factor
        x, y = np.array(background.size) // 2 - O_old 
        size = int(size // size_factor)
        size_y, size_x = sizes // size_factor
        margin_x = int((background.size[0] - size_x)//2)
        margin_y = int((background.size[1] - size_y)//2 // 1.2) 

    else:
        size_factor = 1
        margin_x, margin_y = 0,0
        x,y = 0,0
    
    
    
    if shift :
        if margin_x:
            x = x + int(np.random.randint(low = -margin_x, high = margin_x, size = 1))
        if margin_y:
            y = y + int(np.random.randint(low = -margin_y, high = margin_y, size = 1))

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype(font_name, size=size)
    reshaped_text = arabic_reshaper.reshape(word)
    bidi_text = get_display(reshaped_text)
    draw.text((x, y), bidi_text, fill=color, font=font)
    return background

def generate_name(output_dir):
    name = str(datetime.datetime.now()).replace('-','').replace(':','').replace(' ','_').replace('.','_') + '.png'
    name = os.path.join(output_dir, name)
    return name

def get_all_fonts(fonts_dir):
    fonts_names = glob(os.path.join(fonts_dir , '*ttf'))
    return fonts_names

def get_all_bgs(bgs_dir):
    bgs_names = glob(os.path.join(bgs_dir , '*'))
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
    all_words = list(filter(lambda x:len(x), all_words))
    return all_words

def img_to_bbx(img):
    img = np.array(img)
    args = np.argwhere(img[...,0]>0)
    y_max, x_max = np.max(args,0)
    y_min, x_min = np.min(args,0)
    bbx = (x_min,x_max), (y_min, y_max)
  
    o_x_offset = ((x_min + x_max) / img.shape[1] ) - 1
    o_y_offset = ((y_min + y_max) / img.shape[0] ) - 1
    offsets = [o_x_offset , o_y_offset]

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


def gaussian_noise(image):
    epsilon = np.random.rand()
    if epsilon >= 0.7:
        return image
    image = np.array(image)[...,:3]
    row,col,ch= image.shape
    mean = 0
    var = 50
    sigma = var**0.5
    gauss = np.random.normal(mean,sigma,(row,col,ch))
    gauss = gauss.reshape(row,col,ch)
    noisy = image + gauss
    noisy = noisy.astype('uint8')
    noisy = Image.fromarray(noisy)
    return noisy

def salt_and_pepper(image):
    prob = np.random.randint(0,100) / 1000
    epsilon = np.random.rand()
    if epsilon <= 0.6:
        return image
    arr = np.asarray(image)
    original_dtype = arr.dtype
    intensity_levels = 2 ** (arr[0, 0].nbytes * 8)

    min_intensity = 0
    max_intensity = intensity_levels - 1
    random_image_arr = np.random.choice(
        [min_intensity, 1, np.nan], p=[prob / 2, 1 - prob, prob / 2], size=arr.shape
    )
    salt_and_peppered_arr = arr.astype(np.float) * random_image_arr
    salt_and_peppered_arr = np.nan_to_num(
        salt_and_peppered_arr, nan=max_intensity
    ).astype(original_dtype)

    return Image.fromarray(salt_and_peppered_arr)


def generate_name(output_dir, data_type = 'img'):
    if data_type == 'img':
        name = str(datetime.datetime.now()).replace('-','').replace(':','').replace(' ','_').replace('.','_') + '.png'
        name = os.path.join(output_dir , name)
    else :
        name = str(datetime.datetime.now()).replace('-','').replace(':','').replace(' ','_').replace('.','_')+'.json'
        name = os.path.join(output_dir , name)

    return name

def create_label(img, name, word):
    current_data = {}
    current_data['imagePath'] = name
    current_data['imageHeight'] = img.size[1]
    current_data['imageWidth'] = img.size[0]
    current_data['label'] = word
    return current_data


def create_data_set(words, fonts, bgs ,size = None, augment_p = 0.7 ,
                    output_dir = 'outputs/',keep_rate = 0.5 , tight = False):

    labels = {}
    labels['version'] = "1.0.0"
    labels['Created By'] = '4-Geeks'
    right_now = str(datetime.datetime.now())
    labels['date'] = right_now
    exp_name = right_now.replace('-','').replace(':','').replace(' ','_').replace('.','_')
    output_name = os.path.join(output_dir, exp_name + '.json')
    output_dir = os.path.join(output_dir , exp_name)
    
    all_data = []


    t1 = t()
    counter = 0
    os.makedirs(output_dir , exist_ok = True)
    # os.makedirs(os.path.join(output_dir,'images') , exist_ok = True)
    # os.makedirs(os.path.join(output_dir,'labels') , exist_ok = True)

    print('Output directory created.')
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
    print(f'In total, there are {(len(words) * len(fonts) * len(bgs) )} different combinations of images')
    for w_idx, word in enumerate(tqdm(words[:])):
        for f_idx, font in enumerate(fonts[:]):
            for bg_idx, bg in enumerate(bgs):
                create_this_combination = np.random.randn()
                if create_this_combination > keep_rate:
                    continue
                if isinstance(size, int):
                    pass
                elif isinstance(size, list):
                    size = np.random.choice(size)
                elif size == 'random' or size is None:
                    size = int(np.random.randint(110,150,1))
                    
                O_old, sizes = get_rect_size_for_word(word, font, size)
                if not tight:
                    size_factor = np.random.randint(120,150) / 100
                    x_factor = 1.5 + np.random.rand()
                    y_factor = 1 + np.random.rand() // 4
                else: x_factor, y_factor, size_factor = 1 , 1 , 1.05
                bg = resize_bg(bg, sizes, x_factor = x_factor, y_factor=y_factor)
                img = create_word(word, font_name= font,bg = bg, size= size, shift=True,
                                  O_old = O_old, sizes = sizes, size_factor=size_factor)
                img = augment(img, p = augment_p)

                img = salt_and_pepper(img)

                img = gaussian_noise(img)

                name = generate_name(output_dir, 'img')
                img.save(name)
                label = create_label(img,name,word)
                all_data.append(label)
                counter += 1
    print(f'{counter} Images created')
    print('Exporing labels....')
    
    labels['data'] = all_data
    outfile = open(output_name, 'w',encoding="utf-8")
    json.dump(labels, outfile, indent=4, ensure_ascii=False)
    outfile.close()
    
    t2 = t()
    print(f'Time Taken : {np.round(t2-t1,2)} second')
