'''
Using Bottleneck Features for Multi-Class Classification in Keras
We use this technique to build powerful (high accuracy without overfitting) Image Classification systems with small
amount of training data.
The full tutorial to get this code working can be found at the "Codes of Interest" Blog at the following link,
https://www.codesofinterest.com/2017/08/bottleneck-features-multi-class-classification-keras.html
Please go through the tutorial before attempting to run this code, as it explains how to setup your training data.
The code was tested on Python 3.5, with the following library versions,
Keras 2.0.6
TensorFlow 1.2.1
OpenCV 3.2.0
This should work with Theano as well, but untested.
'''
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications
from keras.utils.np_utils import to_categorical
# import matplotlib.pyplot as plt
import math
import cv2
from sklearn.metrics.pairwise import cosine_similarity

# dimensions of our images.
img_width, img_height = 224, 224

#top_model_weights_path = 'bottleneck_fc_model.h5'
#train_data_dir = train_dir
#validation_data_dir = 'data/validation'

# number of epochs to train top model
epochs = 50
# batch size used by flow_from_directory and predict_generator
batch_size = 16


# def save_bottlebeck_features():
#     # build the VGG16 network
#     model = applications.VGG16(include_top=False, weights='imagenet')
#
#     datagen = ImageDataGenerator(rescale=1. / 255)
#
#     generator = datagen.flow_from_directory(
#         train_data_dir,
#         target_size=(img_width, img_height),
#         batch_size=batch_size,
#         class_mode=None,
#         shuffle=False)
#
#     print(len(generator.filenames))
#     print(generator.class_indices)
#     print(len(generator.class_indices))
#
#     nb_train_samples = len(generator.filenames)
#
#     predict_size_train = int(math.ceil(nb_train_samples / batch_size))
#
#     bottleneck_features_train = model.predict_generator(
#         generator, predict_size_train)
#
#     np.save('/home/lokesh/rajesh_goc/train/data/bottleneck_features_train.npy', bottleneck_features_train)
#     return bottleneck_features_train

#bottleneck = save_bottlebeck_features()
#bottleneck.reshape((8,7*7*512))
import pandas as pd
def min_dist_image(image_path,gender_path):
    model = applications.VGG16(include_top=False, weights='imagenet')
    datagen = ImageDataGenerator(rescale=1. / 255)
    generator = datagen.flow_from_directory(
        image_path,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
#     print(len(generator.filenames))
#     print(generator.class_indices)
#     print(len(generator.class_indices))
    nb_train_samples = len(generator.filenames)
    predict_size_train = int(math.ceil(nb_train_samples / batch_size))
    bottleneck_features_test = model.predict_generator(
        generator, predict_size_train)
    bottleneck_features_test = bottleneck_features_test.reshape(1,-1)
    bottleneck_features_train = np.load(gender_path+'bottleneck_features_train.npy')
    bottleneck_features_train = bottleneck_features_train.reshape(bottleneck_features_train.shape[0],-1)
    cosine_similarity_list = []
    for i in range(bottleneck_features_train.shape[0]):
         cosine_similarity_list.append(cosine_similarity(bottleneck_features_train[i,:].reshape(1,-1),bottleneck_features_test)[0][0])
    temp = list(pd.Series(cosine_similarity_list).sort_values(ascending=False).index)
    return temp
  

