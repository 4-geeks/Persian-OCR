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

if __name__ == '__main__':
    create_data_set(words = opt.word_bank,
                    fonts = opt.fonts_dir,
                    bgs = opt.bg_dir ,
                    size = None,
                    noise_p = opt.noise_prob,
                    output_dir = opt.output_dir)