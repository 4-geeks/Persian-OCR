import argparse
from glob import glob
import os
from tqdm import tqdm
from pdf2image import convert_from_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, default='dataset', help='path to pdf folder')

    args = parser.parse_args()
    os.makedirs('pdf images',exist_ok=True)
    for pdf_file in tqdm(glob(f'{args.folder}/*.pdf')):
        pdf_name = pdf_file.split('\\')[-1].split('.pdf')[0]
        pages = convert_from_path(pdf_file)
        for i, page in enumerate(pages):
            page.save(f'pdf images/{pdf_name}_{i}.png','PNG')