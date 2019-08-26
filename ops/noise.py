from skimage.util import random_noise
import re
import numpy as np
from os import walk, getcwd
import os

CODE = 'noise'
REGEX = re.compile(r"^" + CODE + "_(?P<var>[.0-9]+)")

class Noise:
    def __init__(self, var):
        l = str(var).replace('.', '_')
        self.code = CODE + str(l)
        self.var = var

    def process(self, img):
        return random_noise(img, mode='gaussian', var=self.var)

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
            return Noise(float(d['var']))
