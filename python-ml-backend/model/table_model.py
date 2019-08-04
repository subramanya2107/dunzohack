import config
import requests
import json
from loguru import logger
import cv2
import os
import helpers.image as image_helpers


class ModelNetwork(object):
    def __init__(self):
        self.result=None
        self.url=config.TABLE_URL
        self.class_name="table"

    def __predict(self,path, thresh=config.CONF):
        files = {'image': open(path, 'rb')}
        r = requests.post(self.url, files=files)
        if r.status_code == 200:
            input_dict = json.loads(r.text)
        else:
            input_dict={"objects":[]}
            logger.exception("Different status code {} , probably cant connect to {}, PLEASE CHECK".format(r.status_code,self.url))
        r.close()
        # Filter python objects with list comprehensions
        obj = input_dict['objects']
        output = []
        for dict_ele in obj:
            if dict_ele['prob'] > thresh and dict_ele['label'] == self.class_name:
                output.append(dict_ele)

        return {"objects": output}

    def __preprocess(self,path):
        import os
        filename = self.class_name+"_"+os.path.basename(path)
        col_img = cv2.imread(path)
        img = cv2.imread(path, 0)
        # kernel = np.ones((5, 5), np.uint8)
        # img = cv2.erode(img,kernel,iterations=3)
        retval, img = cv2.threshold(img, 123, 255, cv2.THRESH_BINARY)
        b = cv2.distanceTransform(img, distanceType=cv2.DIST_L2, maskSize=3)
        g = cv2.distanceTransform(img, distanceType=cv2.DIST_L2, maskSize=3)
        r = cv2.distanceTransform(img, distanceType=cv2.DIST_L2, maskSize=3)
        # merge the transformed channels back to an image
        transformed_image = cv2.merge((b, g, r))
        # transformed_image=img
        transformed_image = cv2.cvtColor(transformed_image, cv2.COLOR_BGR2GRAY)
        write_lovation = os.path.join(config.TEMP_FOLDER,filename)
        cv2.imwrite(write_lovation, transformed_image)
        return col_img, write_lovation, filename

    def detect(self,path,queue=None):
        input_image, processed_file, file_name = self.__preprocess(path)
        logger.debug("Image shape -- {} ".format(input_image.shape[:2]))
        obj_json = self.__predict(processed_file)
        logger.debug("prediction for class {} -- {}".format(self.class_name,obj_json))
        if queue is not None:
            queue[self.class_name]=obj_json
        return obj_json


table_network = ModelNetwork()


def clean(table_dict,column_dict,header_dict):
    result=[]
    for table_ele in table_dict['objects']:
        [table_xmin, table_ymin, table_xmax, table_ymax] = table_ele['bbox']
        table_result={
            "bbox":table_ele['bbox'],
            "label":table_ele['label'],
            "prob":table_ele['prob'],
            "columns":[],
            "header":None
        }

        for column_ele in column_dict['objects']:
            [xmin,ymin,xmax,ymax]=column_ele['bbox']
            x_center=(xmin+xmax)/2
            y_center=(ymin+ymax)/2

            if (x_center>=table_xmin and y_center>=table_ymin and x_center<=table_xmax and y_center<=table_ymax):
                logger.debug("adding column element -- {}".format(column_ele))
                table_result['columns'].append(column_ele)

        for header_ele in header_dict['objects']:
            [xmin, ymin, xmax, ymax] = header_ele['bbox']
            x_center = (xmin + xmax) / 2
            y_center = (ymin + ymax) / 2

            if (x_center>=table_xmin and y_center>=table_ymin and x_center<=table_xmax and y_center<=table_ymax):
                logger.debug("adding header element -- {} ".format(header_ele))
                table_result['header']=header_ele

        result.append(table_result)

    logger.debug("Cleaned prediction -- {}".format(result))
    return result


import numpy as np
def get_column(word_list,input_image):
    offset = 10
    blank_image = np.zeros((input_image.shape[:2]))
    H,W = blank_image.shape[:2]
    for word in word_list:
        xmin, ymin, xmax, ymax, (c_x, c_y), c, text = word
        xmin, ymin, xmax, ymax = xmin + offset, ymin + offset, xmax - offset, ymax - offset
        cv2.rectangle(blank_image,(xmin,ymin),(xmax,ymax),255,cv2.FILLED)
    squash = cv2.reduce(blank_image, 0, cv2.REDUCE_MAX)
    find = np.array((squash > 1).nonzero()).tolist()
    columns = image_helpers.group_consecutives(find[1])
    print(columns)

    result = []
    for column in columns:
        xmin,xmax = column

        result.append({
            "bbox": [
                xmin,
                0,
                xmax,
                H
            ],
            "label": "column",
            "prob": 1
        })

    return {"objects":result}


def get_table_data(path):
    print("insode")
    json_ret = table_network.detect(path)
    # json_ret = {'objects': [{'bbox': [4, 374, 451, 546], 'label': 'table', 'prob': 0.9971}]}

    #for debug
    img = cv2.imread(path,1)

    for index,obj in enumerate(json_ret['objects']):
        xmin,ymin,xmax,ymax = obj['bbox']
        cv2.rectangle(img,(xmin,ymin),(xmax,ymax),(255,0,0),2)
        crop = img[ymin:ymax,xmin:xmax]

        #increase the height to stop overlapping coord.
        crop = image_helpers.image_resize(crop,height=1000)
        crop_H,crop_W = crop.shape[:2]
        crop_save_str = os.path.join(config.TEMP_FOLDER,"temp"+str(index)+".png")
        cv2.imwrite(crop_save_str,crop)
        word_list = image_helpers.get_words_from_vision(crop_save_str)
        column_prediction = get_column(word_list,crop)
        table_prediction = {"objects":[{'bbox': [0, 0, crop_W,crop_H ], 'label': 'table', 'prob': obj['prob']}]}
        header_prediction = {
                "objects": []
            }
        detection = clean(table_prediction,column_prediction,header_prediction)
        from extraction import RULE_1

        extraction = RULE_1.extract(path, detection, word_list)
        print(extraction)
        result = []
        for row in list(sorted(extraction[0].keys())):
            col_index = list(sorted(extraction[0][row].keys()))
            col = extraction[0][row]
            col_data = [col[i] for i in col_index]
            result.append(col_data)
        print(result)
        yield result



