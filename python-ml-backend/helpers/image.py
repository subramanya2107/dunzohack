from bs4 import BeautifulSoup
import tempfile
import subprocess
import numpy as np
import cv2
import config

def get_words(filename, psm=11):
    result = []
    with tempfile.TemporaryFile() as tempf:
        proc = subprocess.Popen(['tesseract','-l','eng','--psm', str(psm), filename, 'stdout', 'hocr'], stdout=tempf)
        proc.wait()
        tempf.seek(0)
        soup = BeautifulSoup(tempf, "html.parser")
        for ele in soup.find_all('span', {'class': 'ocrx_word'}):
            if not ele.text.isspace():
                # print(ele)
                location, conf = ele['title'].split(";")
                __, xmin, ymin, xmax, ymax = location.split(" ")
                xmin, ymin, xmax, ymax = map(int, [xmin, ymin, xmax, ymax])
                if xmin == 0 and ymin == 0:
                    continue
                c_x = (xmax + xmin) / 2
                c_y = (ymin + ymax) / 2
                __, c = conf.split()

                result.append([xmin, ymin, xmax, ymax, (c_x, c_y), c, ele.text])
    return result


def group_consecutives(vals, step=1):
    """Return list of consecutive lists of numbers from vals (number list)."""
    run = []
    result = [run]
    expect = None
    for v in vals:
        if (v == expect) or (expect is None):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + step
    final_result=[]
    for l in result:
        if len(l)>=2:
            first,last=l[0],l[-1]
            final_result.append((first,last))
        else:
            pass
    return final_result


def vertical_histogram(input_image):
    """
    |  |    ||
    |  |    ||
    |  | -> ||
    |  |    ||
    |  |    ||

    :param input_image:
    :return:
    """
    return cv2.reduce(input_image, 1, cv2.REDUCE_AVG).reshape(-1)

def getline(input_image):
    """
    make sure the image sent to the module is a binary image with word level.
    :param input_image:
    :return:
    """
    lines=[]
    H, W = input_image.shape[:2]
    hist=vertical_histogram(input_image)
    # print(hist.tolist())
    find=np.array((hist>1).nonzero()).tolist()[0]
    print(find)
    if len(find) >= 2:
        lines=group_consecutives(find)
    else:
        lines=[]
    # print(lines)
    return W, H, lines

def search(words, coord):
    xmin, ymin, xmax, ymax = coord
    result = []
    for word in words:
        x1, y1, x2, y2, (center_x, center_y), confidence, text = word

        if center_x > xmin and center_x < xmax and center_y > ymin and center_y < ymax:
            result.append(text)
    return " ".join(result)





import io
from google.cloud import vision

import os

def get_words_from_vision(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    result = []
    for text in texts[1:]:
        vertices = ([(vertex.x, vertex.y)
                     for vertex in text.bounding_poly.vertices])
        (xmin,ymin),(xmax,ymax) = vertices[0],vertices[2]
        text = text.description
        c_x = (xmax + xmin) / 2
        c_y = (ymin + ymax) / 2
        c=100
        result.append([xmin, ymin, xmax, ymax, (c_x, c_y), c, text])

    return result


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized


# im = cv2.imread("/Users/chandangm/PycharmProjects/dunzo-app/temp/temp0.png",1)
# im = image_resize(im,height=600)
# cv2.imwrite("temp.png",im)

# filename="/Users/chandangm/PycharmProjects/dunzo-app/temp/temp0.png"
# im = cv2.imread(filename,1)
# binary_image = np.zeros((im.shape[:2])).astype('uint8')
#
# word_list = get_words_from_vision(filename)
# for word in word_list:
#     xmin, ymin, xmax, ymax, (c_x, c_y), c, text = word
#     # xmin, ymin, xmax, ymax = xmin+offset, ymin+offset, xmax-offset, ymax-offset
#     cv2.rectangle(binary_image,(xmin,ymin),(xmax,ymax),255,cv2.FILLED)
#
#
# thr,binary_inverse = cv2.threshold(binary_image,240,255,cv2.THRESH_BINARY_INV)
# cv2.imwrite("test.png",binary_inverse)
# cv2.waitKey(0)

