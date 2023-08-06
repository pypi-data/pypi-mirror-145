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

def Generator(img_dim):
    """
    input：target image (t), defocus blur map (t), luminance attenuation map (t)
    output：defocus blur map (t)
    """
    feature_num = 64
    bn_axis = -1
    nb_channels = img_dim[-1]
    min_s = min(img_dim[:-1])
    Input = layers.Input(shape=(min_s,min_s,3), name="input")
    target = layers.Lambda(lambda z:z[:,:,:,0:1])(Input) # target
    attention_blur = layers.Lambda(lambda z:z[:,:,:,1:2])(Input) # defocus blur map
    attention_attenuation = layers.Lambda(lambda z:z[:,:,:,2:3])(Input) # luminance attenuation map
    attention_map_blur = layers.Lambda(lambda z:K.repeat_elements(z,feature_num,-1))(attention_blur)
    attention_map_attenuation = layers.Lambda(lambda z:K.repeat_elements(z,feature_num,-1))(attention_attenuation)
    x=layers.Conv2D(64,(3,3),padding="same",kernel_initializer=he_normal())(target)    
    x = layers.BatchNormalization(axis=bn_axis)(x)
    x = layers.Activation("relu")(x)
    x = layers.Dropout(0.5)(x)
    x=layers.Conv2D(64,(3,3),padding="same",kernel_initializer=he_normal())(x)    
    x = layers.BatchNormalization(axis=bn_axis)(x)
    x = layers.Activation("relu")(x)
    x=layers.Conv2D(feature_num,(3,3),padding="same",kernel_initializer=he_normal())(x)    

    # resnet
    for i in range(2):
        x_res = layers.BatchNormalization(axis=bn_axis)(x)
        x_res = layers.Activation("relu")(x_res)
        if i==0:
            x_res = layers.Dropout(0.5)(x_res)
        x_res = layers.Conv2D(feature_num, (3,3), padding = "same",kernel_initializer=he_normal())(x_res)
        x_res = layers.BatchNormalization(axis=bn_axis)(x_res)
        x_res = layers.Activation("relu")(x_res)
        x_res = layers.Conv2D(feature_num, (3,3), padding = "same",kernel_initializer=he_normal())(x_res)
        x = layers.Add()([x,x_res])
    x_res = layers.BatchNormalization(axis=bn_axis)(x)
    x_res = layers.Activation("relu")(x_res)
    x_res = layers.Conv2D(feature_num, (3,3), padding = "same",kernel_initializer=he_normal())(x_res)
    x_res = layers.BatchNormalization(axis=bn_axis)(x_res)
    x_res = layers.Activation("tanh")(x_res)

    # Hadamard product of image features and defocus blur map
    x_res = layers.Multiply()([x_res,attention_map_blur])
    x = layers.Add()([x,x_res])    

    # resnet
    for i in range(2):
        x_res = layers.BatchNormalization(axis=bn_axis)(x)
        x_res = layers.Activation("relu")(x_res)
        if i ==0:    
            x_res = layers.Dropout(0.5)(x_res)
        x_res = layers.Conv2D(feature_num, (3,3), padding = "same",kernel_initializer=he_normal())(x_res)
        x_res = layers.BatchNormalization(axis=bn_axis)(x_res)
        x_res = layers.Activation("relu")(x_res)
        x_res = layers.Conv2D(feature_num, (3,3), padding = "same",kernel_initializer=he_normal())(x_res)
        x = layers.Add()([x,x_res])
    x_res = layers.BatchNormalization(axis=bn_axis)(x)
    x_res = layers.Activation("relu")(x_res)
    x_res = layers.Conv2D(feature_num, (3,3), padding = "same",kernel_initializer=he_normal())(x_res)
    x_res = layers.BatchNormalization(axis=bn_axis)(x_res)
    x_res = layers.Activation("tanh")(x_res)

    # Hadamard product of image features and luminance attenuation map

    x_res = layers.Multiply()([x_res,attention_map_attenuation])
    x = layers.Add()([x,x_res])

    x = layers.Conv2D(64, (3, 3) ,padding="same",kernel_initializer=he_normal())(x)
    x = layers.BatchNormalization(axis=bn_axis)(x)
    x = layers.Activation("relu")(x)
    x = layers.Conv2D(64, (3, 3) ,padding="same",kernel_initializer=he_normal())(x)
    x = layers.BatchNormalization(axis=bn_axis)(x)
    x = layers.Activation("relu")(x)  
    x = layers.Conv2D(1, (3, 3) ,padding="same",kernel_initializer=he_normal())(x)

     
    x = layers.Activation("sigmoid", name="generated_img")(x)
    output = layers.ReLU(max_value=1.0)(x)
    generator = Model(Input,output)
    return generator

def loadModel(img_dim,weightPath):
    CompensationNet = Generator(img_dim)
    CompensationNet.load_weights(weightPath)
    return CompensationNet