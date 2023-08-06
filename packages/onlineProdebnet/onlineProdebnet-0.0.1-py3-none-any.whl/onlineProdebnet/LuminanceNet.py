import cv2
import h5py
import keras.backend as K
import numpy as np
import os
import random
import sys
import tensorflow as tf
import tensorflow_probability as tfp
from keras.models import Model
from keras.optimizers import Adam, SGD
from keras.preprocessing.image import load_img, img_to_array, array_to_img,random_rotation
from keras.utils import generic_utils, np_utils, plot_model
from keras import layers
from keras.callbacks import ModelCheckpoint
from keras.initializers import he_normal

def Extractor(img_dim):
    """
    input：projection image (t), projectd result (t), defocus blur map (t-1)
    output：defocus blur map (t)
    """
    bn_axis = -1
    # mis_s = min(width, height) 
    min_s = min(img_dim[:-1])
    # num of convolution
    nb_conv = int(np.floor(np.log(min_s) / np.log(2)))
    # num of filtes
    nb_filters = 32
    list_nb_filters = [nb_filters * min(8, (2 ** i)) for i in range(nb_conv-1)]
    Input = layers.Input(shape=(min_s,min_s,3), name="input")
    list_encoder=[]
    x=layers.Conv2D(list_nb_filters[0],(3,3),padding="same",kernel_initializer=he_normal())(Input)    
    x = layers.BatchNormalization(axis=bn_axis)(x)
    list_encoder.append(x)
    for i, f in enumerate(list_nb_filters[1:]):
        x = layers.Activation("relu")(x)
        x = layers.Conv2D(f, (3, 3), strides=(2,2), name="unet_conv2D_%s" % (i + 1), padding="same",kernel_initializer=he_normal())(x)
        x = layers.BatchNormalization(axis=bn_axis)(x)
        list_encoder.append(x)
    list_nb_filters = list_nb_filters[:-1][::-1]
    for i, f in enumerate(list_nb_filters):
        x = layers.Activation("relu")(x)
        x = layers.UpSampling2D(size=(2, 2))(x)
        x = layers.Conv2D(f, (3, 3), name="unet_upconv2D_%s"% (i + 1), padding="same",kernel_initializer=he_normal())(x)
        x = layers.BatchNormalization(axis=bn_axis)(x)
        if i <= 1:
            x = layers.Dropout(0.5)(x)            
        x = layers.Concatenate(axis=bn_axis)([x, list_encoder[-(i+2)]])
    x = layers.Activation("relu")(x) 
    x = layers.Conv2D(1, (3, 3), name="last_conv" ,padding="same",kernel_initializer=he_normal())(x)
    x = layers.BatchNormalization(axis=bn_axis)(x)
    
    outputMap = layers.Activation("sigmoid",name="outputMap")(x)   
    extractor = Model(Input,outputMap)
    return extractor

def loadModel(img_dim,weightPath):
    luminanceNet = Extractor(img_dim)
    luminanceNet.load_weights(weightPath)
    return luminanceNet
