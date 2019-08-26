from skimage.filters import gaussian
from skimage.exposure import rescale_intensity
import re
import numpy as np
from os import walk, getcwd
import os


CODE = 'blur'
REGEX = re.compile(r"^" + CODE + "_(?P<sigma>[.0-9]+)")

class Blur:
    def __init__(self, sigma):
        l = str(sigma).replace('.', '_')
        self.code = CODE + str(l)
        self.sigma = sigma

    def process(self, img):
        is_colour = len(img.shape)==3
        return rescale_intensity(gaussian(img, sigma=self.sigma, multichannel=is_colour))

    def crt_label(self, dir, file, out_file_name):

        filename, file_extension = os.path.splitext(out_file_name)
        of, oe = os.path.splitext(file)

        for (dirpath, dirnames, filenames) in walk(dir):
            for file_name in filenames:
                f, e = os.path.splitext(file_name)
                if f == of:
                    if e == ".txt":
                        read = open(dirpath + '/' + file_name, 'r')
                        if read.mode == 'r':
                            lines = read.read().split("\n")

                        for line in lines:
                            elems = line.split(' ')
                            if elems[0] != '':
                                print ("Line : ", line, " \n")
                                c = elems[0]
                                x = elems[1]
                                y = elems[2]
                                w = elems[3]
                                h = elems[4]

                                file_label = open(os.path.join(dir, filename) + '.txt', 'a+')
                                file_label.write(c + ' ' + x + ' ' + y + ' ' + w + ' ' + h + '\n')

    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Blur(float(d['sigma']))
