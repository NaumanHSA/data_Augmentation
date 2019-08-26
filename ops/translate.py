from skimage.transform import AffineTransform
from skimage import transform as tf
import re
from PIL import Image
import numpy as np
from os import walk, getcwd
import os

CODE = 'trans'
REGEX = re.compile(r"^" + CODE + "_(?P<x_trans>[-0-9]+)_(?P<y_trans>[-0-9]+)")

class Translate:
    def __init__(self, x_trans, y_trans):
        self.code = CODE + str(x_trans) + '_' + str(y_trans)
        self.x_trans = x_trans
        self.y_trans = y_trans

    def process(self, img):
        return tf.warp(img, AffineTransform(translation=(-self.x_trans, -self.y_trans)))

    def crt_label(self, dir, file, out_file_name):

        img_split = file.split('.')
        out_split = out_file_name.split('.')

        for (dirpath, dirnames, filenames) in walk(dir):
            for file_name in filenames:
                f = file_name.split('.')
                if f[0] == img_split[0]:
                    if f[1] == "txt":
                        read = open(dirpath + '/' + file_name, 'r')
                        if read.mode == 'r':
                            lines = read.read().split("\n")

                        for line in lines:
                            elems = line.split(' ')
                            if elems[0] != '':
                                print ("Line : ", line, " \n")
                                c = elems[0]
                                x_norm = float(elems[1])
                                y_norm = float(elems[2])
                                w_norm = float(elems[3])
                                h_norm = float(elems[4])

                                im = Image.open(dir + '/' + file)
                                img_width = im.size[0]
                                img_height = im.size[1]

                                x = ((float(x_norm) * img_width) + self.x_trans)
                                w = (w_norm * img_width)
                                y = ((float(y_norm) * img_height) + self.y_trans)
                                h = (h_norm * img_height)

                                x_max = (x + (w/2))
                                x_min = (x - (w/2))
                                y_max = (y + (h/2))
                                y_min = (y - (h/2))

                                xn = x/img_width
                                yn = y/img_height

                                print(img_height, y_max)

                                if x_min < 0:
                                    xn = (x_max/2)/img_width
                                    w_norm = (x_max)/img_width

                                if x_max > img_width:
                                    x_max = img_width
                                    w_norm = (x_max - x_min)/x_max
                                    xn = (x_max - ((w_norm * img_width)/2))/img_width

                                if y_min < 0:
                                    yn = (y_max/2)/img_height
                                    h_norm = y_max/img_height

                                if y_max > img_height:
                                    y_max = img_height
                                    h_norm = (y_max - y_min)/y_max
                                    yn = (y_max - ((h_norm * img_height)/2))/img_height

                                file_label = open(os.path.join(dir, out_split[0]) + '.txt', 'a+')
                                file_label.write(c + ' ' + str(xn) + ' ' + str(yn) + ' ' + str(w_norm) + ' ' + str(h_norm) + '\n')
    @staticmethod
    def match_code(code):
        match = REGEX.match(code)
        if match:
            d = match.groupdict()
            return Translate(int(d['x_trans']), int(d['y_trans']))