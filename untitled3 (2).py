# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mUNhR7IUQT3rBpStEAyB5AOtciUDyyTY
"""

!pip install roboflow

import os
HOME = os.getcwd()
print(HOME)

!pip install ultralytics
from IPython import display
display.clear_output()
from IPython.display import display, Image



import ultralytics
ultralytics.checks()
from ultralytics import YOLO

# Commented out IPython magic to ensure Python compatibility.
!mkdir {HOME}/datasets
# %cd {HOME}/datasets

from roboflow import Roboflow
rf = Roboflow(api_key="hDQlcoxO6BUFllYD2guE")
project = rf.workspace("makestuff").project("human-detection-n1ovn")
version = project.version(4)
dataset = version.download("yolov5-obb")

class_names=['fire','person']
class_indices={name:index for index, name in enumerate(class_names)}

img_width,img_height= 640, 640

folder_path ='/content/datasets/human-detection-4/valid/labels'

def normalize_coordinates(coord, max_value):
  return float(coord) / max_value

for filename in os.listdir(folder_path):
  if filename.endswith(".txt"):
    file_path=os.path.join(folder_path, filename)
    with open(file_path,'r') as file:
      lines = file.readlines()

    new_lines=[]
    for line in lines:
      parts = line.strip().split(' ')
      if len(parts) == 10:
        label = parts[-2]
        coords = parts[:8]

        class_index = class_indices.get(label, -1)
        if class_index != -1:
          normalized_coords = [normalize_coordinates(coords[i], img_width if i % 2 == 0 else img_height) for i in range(8)]
          # Convert to the desired format and add to new lines
          new_line = f"{class_index} " + " ".join(map(str, normalized_coords))
          new_lines.append(new_line)

     # Write the converted lines to a new file or overwrite the existing file
    with open(file_path, 'w') as file:
       file.write('\n'.join(new_lines))

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}

!yolo task=obb mode=train model=yolov8s-obb.pt data={dataset.location}/data.yaml epochs=6 imgsz=954 batch=10



# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
!yolo task=obb mode=predict model={HOME}/runs/obb/train/weights/best.pt conf=0.02 source={dataset.location}/test/images save=true



import glob
from IPython.display import Image, display

for image_path in glob.glob(f'{HOME}/runs/obb/predict/*.jpg'):
      display(Image(filename=image_path, height=600))
      print("\n")

!zip -r datasets2.zip human-detection-4/

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/datasets/

from google.colab import files
files.download('datasets2.zip')

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
!yolo task=obb mode=train model=yolov8s-obb.pt data={dataset.location}/data.yaml epochs=12 imgsz=954 batch=10

# Commented out IPython magic to ensure Python compatibility.
# %cd {HOME}
!yolo task=obb mode=predict model={HOME}/runs/obb/train/weights/best.pt conf=0.25 source={dataset.location}/test/images save=true

import glob
from IPython.display import Image, display

for image_path in glob.glob(f'{HOME}/runs/obb/predict4/*.jpg'):
      display(Image(filename=image_path, height=600))
      print("\n")

!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="hDQlcoxO6BUFllYD2guE")
project = rf.workspace("makestuff").project("human-detection-n1ovn")
version = project.version(5)
dataset = version.download("yolov5-obb")

project.version(dataset.version).deploy(model_type='ultralytics/yolov8', model_path=f'{HOME}/runs/obb/train/')

!pip install ultralytics==8.0.196

import os
HOME = os.getcwd()
print(HOME)