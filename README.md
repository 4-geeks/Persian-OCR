# Persian-OCR
We do persian OCR!

Firstly, run the following command to install the required modules.
```
$ pip install -r requirements.txt
```
## Generating Images
To generate data, go to ``` DataTools/Data_Generation/``` and put the fonts and backgroud images in ```fonts/``` and ```backgrounds/``` respectively.
Please note that the fonts must be in ttf format. Add your bank of words as text files with each line containing only one word in ```word_bank/```.
After doing so, you are able to run ```generator.py``` to generate your images or ```test_generator.py``` to generate one word per font to see how your fonts look.
To run the generator run the following command:

```$ python generator.py```

Moreover, to test for your fonts run the command below:

```$ python test_generator.py```

Note that there the aformentioned folders contain the required material so you can easily generate images without the need to add backgrounds, fonts or words.

Designed by 4Geeks.
