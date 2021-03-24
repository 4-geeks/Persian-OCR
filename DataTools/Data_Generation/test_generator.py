from generation_utils import *
import argparse
parser = argparse.ArgumentParser(description='Input arguments for the data generation tool.')
parser.add_argument('--word-bank', type=str, default='word_bank',
 help='Directory that contains the text files')
parser.add_argument('--fonts-dir', type=str, default='fonts',
 help='Directory that contains the ttf files for your fonts')
parser.add_argument('--bg-dir', type=str, default='backgrounds',
 help='Directory that contains the backgrounds')
parser.add_argument('--output-dir', type=str, default='outputs',
 help='Directory to save the output images')
parser.add_argument('--size', type = int, default= None,
 help='size of the words that you want to create.')
parser.add_argument('--noise-prob', type = int, default= 0.5,
 help='Directory that contains the backgrounds')

opt = parser.parse_args()


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
    words = [words[0]]
    bgs = [bgs[0]]
    for w_idx, word in enumerate(tqdm(words)):
        for f_idx, font in enumerate(fonts):
            for bg_idx, bg in enumerate(bgs):
                if isinstance(size, str):
                    pass
                elif isinstance(size, list):
                    size = np.random.choice(size)
                elif size == 'random' or size is None:
                    size = int(np.random.randint(110,150,1))
                    
                offsets, sizes = get_rect_size_for_word(word, font, size)
                bg = resize_bg(bg, 1.25 * sizes)
                img = create_word(word,offsets = offsets ,font_name= font,bg = bg , size= int(size//1.2))
                img = augment(img, p = noise_p)
                img.save(os.path.join(output_dir , f'w_{w_idx:04d}f_{f_idx:04d}b_{bg_idx:04d}.png' ))
                counter += 1
    print(f'{counter} Images created')
    t2 = t()
    print(f'Time Taken : {np.round(t2-t1,2)} second')


if __name__ == '__main__':
    create_data_set(words = opt.word_bank,
                    fonts = opt.fonts_dir,
                    bgs = opt.bg_dir ,
                    size = None,
                    noise_p = opt.noise_prob,
                    output_dir = opt.output_dir)