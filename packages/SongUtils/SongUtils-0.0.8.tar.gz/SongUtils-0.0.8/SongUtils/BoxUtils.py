import cv2
import numpy as np
import matplotlib.pyplot as plt


def xyxy2xywh(box2d):
    """
        input   : [n, 4] [x1, y1, x2, y2]
        return  : [n, 4] [x, y, w, h]
        numpy accelerated
    """
    center_x = 0.5 * (box2d[:, 0] + box2d[:, 2])
    center_y = 0.5 * (box2d[:, 1] + box2d[:, 3])
    width_x  = box2d[:, 2] - box2d[:, 0]
    width_y  = box2d[:, 3] - box2d[:, 1]
    result = np.zeros_like(box2d)
    result[:, 0] = center_x
    result[:, 1] = center_y
    result[:, 2] = width_x
    result[:, 3] = width_y
    return result

def xywh2xyxy(box2d):
    """
        input   :  [n, 4] [x, y, w, h]
        return  :  [n, 4] [x1, y1, x2, y2]
    """
    halfw = 0.5*box2d[:, 2]
    halfh = 0.5*box2d[:, 3]

    result = np.zeros_like(box2d)
    result[:, 0] = box2d[:, 0] - halfw
    result[:, 1] = box2d[:, 1] - halfh
    result[:, 2] = box2d[:, 0] + halfw
    result[:, 3] = box2d[:, 1] + halfh
    return result

def bbox2d_area(bbox2d):
    """
        input:
            [n, 4] [x1, y1, x2, y2]
        return:
            [n, ]
    """
    dx = bbox2d[:, 2] - bbox2d[:, 0]
    dy = bbox2d[:, 3] - bbox2d[:, 1]
    dx[np.where(dx < 0)] = 0
    dy[np.where(dy < 0)] = 0
    area = dx * dy
    return area


def iou_2d_combination(box2d_0, box2d_1):
    """
        input:
            [n, 4] [x1, y1, x2, y2]
            [k, 4] [x1, y1, x2, y2]
        return:
            [n, k]
    """
    n = box2d_0.shape[0]
    k = box2d_1.shape[0]
    result = np.zeros((n, k))
    bbox_2d_repeated = np.zeros((k, 4))
    for i in range(n):
        bbox_2d_0 = box2d_0[i] #[1, 4]
        for j in range(k):
            bbox_2d_repeated[j] = bbox_2d_0
        result[i] = iou_2d(bbox_2d_repeated, box2d_1)
    return result


def iou_2d(box2d_0, box2d_1):
    """
        input:
            [n, 4] [x1, y1, x2, y2]
            [n, 4] [x1, y1, x2, y2]
        return:
            [n, ]
    """
    n = box2d_0.shape[0]
    result = np.zeros(n)

    area_0 = bbox2d_area(box2d_0)
    area_1 = bbox2d_area(box2d_1)
    
    for i in range(n):
        x1 = max(box2d_0[i, 0], box2d_1[i, 0])
        x2 = min(box2d_0[i, 2], box2d_1[i, 2])
        y1 = max(box2d_0[i, 1], box2d_1[i, 1])
        y2 = min(box2d_0[i, 3], box2d_1[i, 3])
        dx = x2 - x1
        dy = y2 - y1
        if dx <= 0 or dy <= 0:
            result[i] = 0
        else:
            area = dx * dy
            result[i] = area / (area_0[i] + area_1[i] - area)
    return result




if __name__ == "__main__":
    box1 = np.array([10, 10, 20, 20]).reshape(1, 4)
    box2 = np.array([15, 15, 25, 25]).reshape(1, 4)

    xywh = xyxy2xywh(box)
    print(xywh2xyxy(xywh))