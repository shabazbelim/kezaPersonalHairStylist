from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import imutils
import dlib
import cv2
import numpy as np
from skimage.measure import compare_ssim as ssim
import os
import sys
from hairstylist import BASE_DIR

predictor = None
def hog_err(source_img,images):
    global predictor
    mags = []
    detector = dlib.get_frontal_face_detector()
    if(predictor == None):
        predictor = dlib.shape_predictor(BASE_DIR+"/hairstylist/pipeline/shape_predictor_68_face_landmarks.dat")
    fa = FaceAligner(predictor, desiredFaceWidth=256)
    for image in images:
        #image = imutils.resize(image, width=800)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 2)
        if(rects):
            (x, y, w, h) = rect_to_bb(rects[0])
            #print((x,y,w,h))
        # faceOrig = imutils.resize(image[y:y + h, x:x + w], width=256)
            faceAligned = fa.align(image, gray, rects[0])
            mags.append(cv2.resize(faceAligned, (255, 255)))
            temp = rects
        else:
            (x, y, w, h) = rect_to_bb(temp[0])
            #print((x,y,w,h))
        # faceOrig = imutils.resize(image[y:y + h, x:x + w], width=256)
            faceAligned = fa.align(image, gray, temp[0])
            mags.append(cv2.resize(faceAligned, (255, 255)))

    #image = imutils.resize(source_img, width=800)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 2)
    (x, y, w, h) = rect_to_bb(rects[0])
    # faceOrig = imutils.resize(image[y:y + h, x:x + w], width=256)
    faceAligned = fa.align(image, gray, rects[0])
    mags.append(cv2.resize(faceAligned, (255, 255)))
    images = mags[:-1]
    err = []
    for image in images:
        err.append(ssim(mags[-1], image, multichannel=True))

    return err