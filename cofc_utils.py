import numpy as np
import pickle as pkl
import os, time, itertools, argparse
import cv2, dlib, openface
from matplotlib import pyplot as plt
from face_feats import get_deep_feature, get_deep_features, initialize_deep_models

class face_element:
    def __init__(self, fno, bbox, img, feat):
        self.fno = fno
        self.bbox = bbox
        self.img = img
        self.feat = feat
        
def display_cv_image(im, size=(10,10), label=""):
    if(len(im.shape) == 3):
        plt.figure(figsize=size)
        plt.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        plt.title(label)
        plt.show()
    else:
        plt.figure(figsize=size)
        plt.imshow(im, cmap="gray")
        plt.title(label)
        plt.show()
        
def get_dlib_detector():
    return dlib.get_frontal_face_detector()

def get_face_bboxes_in_frame(im, detector):
    dets = detector(img, 1)
    N = len(dets)
    print(N)
    np_rects = np.zeros((N, 4), int)
    for i, d in enumerate(dets):
        np_rects[i,:] = np.array([d.left(),d.top(),d.right(),d.bottom()])
    return np_rects

def shot_boundary(ppf, pf, f, thresh=60):
    #this method taken from Johan Mathe's code: https://github.com/johmathe/shotdetect
    d1 = np.sum(np.abs(ppf -pf))
    d2 = np.sum(np.abs(pf - f))
    diff = abs(d1-d2)
    
    if diff>thresh and d2>thresh:
        return True
    else
        return False

def extract_bboxes_and_features(ls_frames, detector, aligner, fnet):
    shot_data = []
    ii=0
    for frame in ls_frames:
        boxes = get_face_bboxes_in_frame(frame, detector)
        if(boxes.shape[0] == 0):
            continue 
        for i in range(boxes.shape[0]):
            im = frame[boxes[1]:boxes[3], boxes[0]:boxes[2]].copy()
            feat = get_deep_feature(im, aligner, fnet)
            ls_data.append(face_element(ii, boxes[i], im, feat))
        ii+=1
    return shot_data 
