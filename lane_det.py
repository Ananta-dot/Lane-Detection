import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from os.path import isfile, join
import re
import time

def load_images_from_folder(folder):
	i_name = 0
	images = []
	for filename in os.listdir(folder):
		img = cv2.imread(os.path.join(folder,str(i_name)+".png"))
		if img is not None:
			images.append(img)
		i_name += 1
	return images

images = load_images_from_folder("frames")

#shape of "list" images = (1108,270)

i_no = 1100

arr_zero = np.zeros_like(images[i_no][:,:,0])
lane_shape = np.array([[50,270], [220,160], [360,160], [480,270]])

cv2.fillConvexPoly(arr_zero,lane_shape,1)

img = cv2.bitwise_and(images[i_no][:,:,0],images[i_no][:,:,0], mask=arr_zero)

ret,thresh1 = cv2.threshold(img,130,255,cv2.THRESH_BINARY)

lines = cv2.HoughLinesP(thresh1, rho = 1, theta=np.pi/180, threshold=30, maxLineGap=200)

img2 = images[i_no][:,:,0].copy()

for line in lines:
	x1, y1, x2, y2 = line[0]
	cv2.line(img2, (x1, y1), (x2, y2), (255, 0, 0), 3)

detected = 0

for img in images:
	covered = cv2.bitwise_and(img[:,:,0],img[:,:,0], mask=arr_zero)
	ret,thresh1 = cv2.threshold(covered,130,255,cv2.THRESH_BINARY)
	lines = cv2.HoughLinesP(thresh1, rho = 1, theta=np.pi/180, threshold=30, maxLineGap=200)
	img2 = img.copy()

	try:
		for line in lines:
			x1, y1, x2, y2 = line[0]
			cv2.line(img2, (x1, y1), (x2, y2), (255, 0, 0), 3)

		cv2.imwrite('detected/'+str(detected)+'.png',img2)
	except TypeError:
		cv2.imwrite('detected/'+str(detected)+'.png',img)
	
	detected+= 1


pathIn= 'detected/'
pathOut = 'video.avi'
fps = 20

frame_array = []
files_num = []
files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
files.remove(".DS_Store")
for i in files:
	i = i.replace('.png','')
	files_num.append(int(str(i)))

files_num.sort()
files_final = []
for i in files_num:
	files_final.append(str(i)+".png")

print(files_final)

for i in range(len(files_final)):
	filename = pathIn + files_final[i]
	img = cv2.imread(filename)
	height, width, layers = img.shape
	size = (width,height)
	frame_array.append(img)

out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'MPEG'), fps, size)

for i in range(len(frame_array)):
	out.write(frame_array[i])

out.release()