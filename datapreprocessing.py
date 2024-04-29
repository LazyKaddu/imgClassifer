import skimage as ski
from skimage.transform import resize
import os
import numpy as np

DATAIMG = os.listdir("dataImg")

def retLen(dirct):
  return len(os.listdir(f'dataImg\\{dirct}'))

def resizer(img):
  return resize(img, (512, 512),anti_aliasing=True)

def preProcess(name,ind):
  imgArr = np.empty([ind,512,512,3])
  for i in range(ind):
    print(i)
    imgArr = np.append(imgArr,resizer(ski.io.imread(f"dataImg\\{name}\\{name}_{i+1}.jpg")))
  return imgArr


for i in DATAIMG:
  print(i)
  DATAFRAME = np.array(preProcess(i,retLen(i)), dtype=object)
  np.save(f"data{i}",DATAFRAME)
  DATAFRAME = None

print("resize done")

print(DATAFRAME)