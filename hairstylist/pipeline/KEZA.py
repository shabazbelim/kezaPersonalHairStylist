import cv2
import numpy as np
import dlib
import pandas as pd
from hairstylist.pipeline.hog2 import hog_err
from hairstylist import TRAIN_DATA
from pyagender import PyAgender
from hairstylist.pipeline.bottleneck_keras import min_dist_image
import glob

from hairstylist import BASE_DIR, STATIC_IMAGE_PATH

import time
from hairstylist.pipeline.face_wrapping import face_wrapping
agender = PyAgender()

def return_image(source_img_path):
    source_image_path=source_img_path

    faces = agender.detect_genders_ages(cv2.imread(source_image_path))
    if not len(faces) > 0:
        return False
    gendr=faces[0]['gender']
    predictor = dlib.shape_predictor(BASE_DIR+"/hairstylist/pipeline/shape_predictor_68_face_landmarks.dat")

    # gendr = gender('/home/lokesh/rajesh_goc/curl_girl2.jpg')
    if(gendr>=0.30):
        gendr = 'F'
    else:
        gendr = 'M'


    def get_target_list(train_dir,test_dir):
        file_list=glob.glob(train_dir+'data/*')
        file_selected=min_dist_image(test_dir,train_dir)
        file_selected=[file_list[i] for i in file_selected]
        print(file_selected)

        source_img_vec=cv2.imread(source_image_path)
        target_img_vec_list=[cv2.imread(name) for name in file_selected]
        err_list=pd.Series(hog_err(source_img_vec,target_img_vec_list))
        print(err_list.values)

        err_list_ind=list(err_list.index)
        file_selected_2=[file_selected[i] for i in err_list_ind]
        print(file_selected_2)

        t_a_list=[agender.detect_genders_ages(cv2.imread(n))[0]['age'] for n in file_selected_2]
        print(t_a_list)

        source_age=agender.detect_genders_ages(cv2.imread(source_image_path))[0]['age']

        print(source_age)
        diff_age_sqr=[np.abs(source_age - t_a)**2 for t_a in t_a_list]
        print(diff_age_sqr)
        D_score=[diff_age_sqr[i]+50*err_list[i] for i in range(len(diff_age_sqr))]
        D_scoreInd=list(pd.Series(D_score).sort_values().index)
    #     print(D_scoreInd)
        file_selected_3=[file_selected_2[i] for i in D_scoreInd]
        return file_selected_3[:5]

    st1=time.time()
    if gendr =='F':
        female_train_path= TRAIN_DATA+'female_train/'
        female_test_path=TRAIN_DATA+'female_test/'
        target_list=get_target_list(female_train_path,female_test_path)
    else:
        male_train_path=TRAIN_DATA+'male_train/'
        male_test_path=TRAIN_DATA+'male_test/'
        target_list=get_target_list(male_train_path,male_test_path)
    st2=time.time()
    print(st2-st1)

    st3=time.time()
    image_list = []
    for im in target_list:
        img=face_wrapping(cv2.imread(source_image_path),cv2.imread(im),predictor)
        source_img_s=source_image_path.split('/')[-1]
        source_img_s =  source_img_s.split('.')[0]
        target_img_s=im.split('/')[-1]
        cv2.imwrite(STATIC_IMAGE_PATH+source_img_s+"__"+target_img_s, img)
        image_list.append(source_img_s+"__"+target_img_s)
    st4=time.time()
    print(st4-st3)
    return image_list