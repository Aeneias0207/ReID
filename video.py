import cv2
import numpy as np
from glob import glob
  
  
images = sorted(glob("images/*.jpg"), key = lambda img:int(img.split("/")[-1].split(".")[0]))
print(images[:5])
  # choose codec according to format needed
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
video = cv2.VideoWriter('video.mp4', fourcc, 3, (324,244))

for imagepath in images:
    img = cv2.imread(imagepath)
    video.write(img)
print(len(images))
video.release()