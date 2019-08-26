import numpy as np
from os import walk, getcwd
import os

CODE = 'fliph'


class FlipH:
    def __init__(self):
        self.code = CODE

    def process(self, img):
        return np.fliplr(img)

    def crt_label(self, dir, file, out_file_name):
        file_split = file.split('.')
        out_split = out_file_name.split('.')

        for (dirpath, dirnames, filenames) in walk(dir):
            for file_name in filenames:
                f = file_name.split('.')
                if f[0] == file_split[0]:
                    if f[1] == "txt":
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

                                xn = 1 - float(x)
                                file_label = open(os.path.join(dir, out_split[0]) + '.txt', 'a+')
                                file_label.write(c + ' ' + str(xn) + ' ' + y + ' ' + w + ' ' + h + '\n')

    @staticmethod
    def match_code(code):
        if code == CODE:
            return FlipH()
