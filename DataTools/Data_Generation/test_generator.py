from generation_utils import *
import argparse
parser = argparse.ArgumentParser(description='Input arguments for the data generation tool.')
parser.add_argument('--word-bank', type=str, default='word_bank',
 help='Directory that contains the text files')
parser.add_argument('--fonts-dir', type=str, default='fonts',
 help='Directory that contains the ttf files for your fonts')
parser.add_argument('--bg-dir', type=str, default='backgrounds',
 help='Directory that contains the backgrounds')
parser.add_argument('--output-dir', type=str, default='outputs/fonts_test',
 help='Directory to save the output images')
parser.add_argument('--size', type = int, default= None,
 help='size of the words that you want to create.')
parser.add_argument('--augment-prob', type = float, default= 0.5,
 help='augmentation rate')
parser.add_argument('--tight', action = 'store_true' , help =  'Wether you want the text to tightly fit the background')
parser.add_argument('--keep-rate', type = float, help = 'The ratio for saving the images.' , default=0.5)

opt = parser.parse_args()


def create_data_set(words, fonts, bgs ,size = None, augment_p = 0.7 ,
                    output_dir = 'outputs/fonts_test',keep_rate = 0.5 , tight = False):
    t1 = t()
    counter = 0
    
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
    print('Output directory craeted.')
    # print(f'Found {len(words)} words.')
    print(f'Found {len(fonts)} fonts.')
    # print(f'Found {len(bgs)} background images.')
    # print(f'In total {len(words) * len(fonts) * len(bgs)} Images will be created')
    words = [words[0]]
    bgs = [bgs[0]]
    for w_idx, word in enumerate(tqdm(words)):
        for f_idx, font in enumerate(fonts):
            for bg_idx, bg in enumerate(bgs):
                if isinstance(size, int):
                    pass
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
                                  
                font_name = os.path.split(font)[-1].split('.')[0]
                img.save(os.path.join(output_dir , f'{font_name}.png') )
                counter += 1
    print(f'{counter} Images created')
    t2 = t()
    print(f'Time Taken : {np.round(t2-t1,2)} second')


if __name__ == '__main__':
    create_data_set(words = opt.word_bank,
                    fonts = opt.fonts_dir,
                    bgs = opt.bg_dir ,
                    size = None,
                    augment_p = opt.augment_prob,
                    output_dir = opt.output_dir,
                    tight= opt.tight,
                    keep_rate = opt.keep_rate)