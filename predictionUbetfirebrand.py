# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import keras
from keras.models import Model
from keras.layers import Conv2D, MaxPooling2D, Input, Conv2DTranspose, Concatenate, BatchNormalization, UpSampling2D
from keras.layers import  Dropout, Activation
from keras.optimizers import Adam, SGD
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from keras import backend as K
from keras.utils import plot_model
import tensorflow as tf
import glob
import random
import cv2
from random import shuffle
import json



def mean_iou(y_true, y_pred):
    yt0 = y_true[:,:,:,0]
    yp0 = K.cast(y_pred[:,:,:,0] > 0.5, 'float32')
    inter = tf.math.count_nonzero(tf.logical_and(tf.equal(yt0, 1), tf.equal(yp0, 1)))
    union = tf.math.count_nonzero(tf.add(yt0, yp0))
    iou = tf.where(tf.equal(union, 0), 1., tf.cast(inter/union, 'float32'))
    return iou

def unet(sz = (256, 256, 3)):
  x = Input(sz)
  inputs = x

  #down sampling
  f = 8
  layers = []

  for i in range(0, 6):
    x = Conv2D(f, 3, activation='relu', padding='same') (x)
    x = Conv2D(f, 3, activation='relu', padding='same') (x)
    layers.append(x)
    x = MaxPooling2D() (x)
    f = f*2
  ff2 = 64

  #bottleneck
  j = len(layers) - 1
  x = Conv2D(f, 3, activation='relu', padding='same') (x)
  x = Conv2D(f, 3, activation='relu', padding='same') (x)
  x = Conv2DTranspose(ff2, 2, strides=(2, 2), padding='same') (x)
  x = Concatenate(axis=3)([x, layers[j]])
  j = j -1

  #upsampling
  for i in range(0, 5):
    ff2 = ff2//2
    f = f // 2
    x = Conv2D(f, 3, activation='relu', padding='same') (x)
    x = Conv2D(f, 3, activation='relu', padding='same') (x)
    x = Conv2DTranspose(ff2, 2, strides=(2, 2), padding='same') (x)
    x = Concatenate(axis=3)([x, layers[j]])
    j = j -1


  #classification
  x = Conv2D(f, 3, activation='relu', padding='same') (x)
  x = Conv2D(f, 3, activation='relu', padding='same') (x)
  outputs = Conv2D(1, 1, activation='sigmoid') (x)

  #model creation
  model = Model(inputs=[inputs], outputs=[outputs])
  model.compile(optimizer = 'rmsprop', loss = 'binary_crossentropy', metrics = [mean_iou])

  return model

model = unet()

model.load_weights('unet.h5')

folder_path = "frames./subfolder_9"
files = os.listdir(folder_path)
files.sort()

index = 0

filename = 'filename.txt'

if os.path.exists(filename):
    os.remove(filename)
    print(f"'{filename}' deleted successfully.")
else:
    print(f"'{filename}' does not exist.")


# Iterate through each file
for file in files:
  print(file)
  result = {}
  image_path = os.path.join(folder_path, file)
  raw = Image.open(image_path)
  raw = np.array(raw.resize((256, 256)))/255.
  raw = raw[:,:,0:3]

  #predict the mask
  pred = model.predict(np.expand_dims(raw, 0))

  #mask post-processing
  msk  = pred.squeeze()
  msk = np.stack((msk,)*3, axis=-1)
  msk[msk >= 0.5] = 255
  msk[msk < 0.5] = 0

  msk = np.uint8(msk)

  ## Define the region of interest (ROI) or the area to be cropped
  x, y, width, height = 95, 15, 450, 448  # Example coordinates (x, y, width, height)

  # Crop the image
  image = msk[y:y+height, x:x+width]

  # Convert the image to grayscale
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Apply Canny edge detection
  edges = cv2.Canny(gray, 50, 150)

  # Find contours
  contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Initialize counters
  box_count = 0

  firebrand_information = {}

  # Get the size factor
  raw_image = cv2.imread(image_path)
  height, width = raw_image.shape[:2]
  scale_factor_width = width/256
  scale_factor_height = height/256

  # Open a file to write box information
    # Iterate through contours
  for contour in contours:
    # Compute the minimum bounding box
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # Calculate box parameters
    (x, y), (width, height), angle = rect

    firebrand_information[box_count] = {'width': width*scale_factor_width,\
                                        'height': height*scale_factor_height}

    # Increment box counter
    box_count += 1

    cv2.drawContours(image, [box], 0, (0, 255, 0), 2)
  result[file] = firebrand_information

  # Define the path for the JSON file
  json_file_path = "output./" +file+ ".json"

  # Serialize the dictionary to JSON and save it to a file
  with open(json_file_path, "w") as json_file:
      json.dump(result, json_file)

  raw_image = cv2.imread(image_path)
  height, width = raw_image.shape[:2]
  image_contours = cv2.resize(msk, (width, height))
  overlay = cv2.addWeighted(raw_image, 1, image_contours, 0.3, 1)

  # Define the path for the JSON file
  overlay_file_path = "output_frame./" +file+ ".jpg"
  cv2.imwrite(overlay_file_path,overlay)

  with open('filename.txt', 'a') as file:
    file.write(str(box_count) + '\n')

  index = index + 1

  if index >20000:
    break
  


