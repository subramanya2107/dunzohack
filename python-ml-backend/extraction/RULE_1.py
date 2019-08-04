"""
Table extraction rule 1:



this rule assumes mapped json object wrt to its table elements. I.e - table json which has columns linked to it.
Not handling headers.
Extract column values and make a dataframe out of it.
Sample:

    [{'bbox': [36, 545, 1227, 1303],
      'columns': [{'bbox': [729, 576, 844, 1233],
                   'label': 'column',
                   'prob': 0.9998},
                  {'bbox': [1066, 584, 1182, 1248],
                   'label': 'column',
                   'prob': 0.9998},
                  {'bbox': [87, 548, 175, 1236], 'label': 'column', 'prob': 0.9998},
                  {'bbox': [526, 575, 639, 1231],
                   'label': 'column',
                   'prob': 0.9998},
                  {'bbox': [403, 574, 475, 1239],
                   'label': 'column',
                   'prob': 0.9997},
                  {'bbox': [910, 606, 1017, 1241],
                   'label': 'column',
                   'prob': 0.9986}],
      'header': {'bbox': [103, 521, 1230, 581], 'label': 'header', 'prob': 0.9297},
      'label': 'table',
      'prob': 0.9726}]

Rules:


Fail-points:
1.if the column starts with blank line.tesseract wont return blank line.so tagging it back to row fails.
    can be solved by using row count and checking if any words comes in -> return words else return None/new line.

2. table localisation is not perfect yet. so often you'll receive junk values in the beginning due to incorrect line crop.


Improvements:
add max datatype check and remove rows that doesnt follow that datatype.


Works best for:
homogeneous table where the elements in the table are similar in terms or structure and data type.


"""
from helpers.image import get_words, search
import numpy as np

def get_filled_image(input_image, words_list):
    import cv2
    out_image = np.zeros(input_image.shape[:2])
    for ele in words_list:
        xmin, ymin, xmax, ymax, [c_x, c_y], c, text = ele
        # print(xmin, ymin, xmax, ymax, [c_x, c_y], c, text)
        xmin=int(xmin)
        ymin=int(ymin)
        xmax=int(xmax)
        ymax =int(ymax)
        cv2.rectangle(out_image, (xmin, ymin), (xmax, ymax), (255), cv2.FILLED)
    return out_image


def get_row_columns(input_image, table_json):
    x1, y1, x2, y2 = table_json['bbox']
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    print(x1,y1,x2,y2)
    cropped_image = input_image[y1:y2, x1:x2]
    from helpers.image import getline
    W, H, lines = getline(cropped_image)
    # print(lines)
    lines = [(ele[0] + y1, ele[1] + y1) for ele in lines]
    # print(lines)
    table_json['row_index'] = lines
    col = []
    for column in table_json['columns']:
        x1, y1, x2, y2 = column['bbox']
        col.append((x1, x2))

    table_json['column_index'] = sorted(col,key=lambda x:x[0])
    return table_json


def extract(filename,predict_json,word_list):
    words = word_list
    import cv2
    img = cv2.imread(filename, 1)
    out = get_filled_image(img, words)
    result_table=[]
    for table in predict_json:
        new_json=get_row_columns(out, table)
        table_json={}
        for row_index,row in enumerate(new_json['row_index']):
            y1,y2=row
            row_json={}
            for col_index,col in enumerate(new_json['column_index']):
                x1,x2=col
                col_str=search(words, (x1, y1, x2, y2))
                row_json[col_index]=col_str
            table_json[row_index]=row_json
        result_table.append(table_json)
    return result_table