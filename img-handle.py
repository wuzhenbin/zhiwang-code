
'''
单张图片二值化 灰度处理demo
'''
import tesserocr 
from PIL import Image 
import os

path = os.getcwd() + '\\imgs'
file_lis = os.listdir(path)

for item in file_lis:
	image = Image.open('./imgs/{}'.format(item)) 
	image = image.convert('L') 
	threshold = 165 
	table = [] 
	for i in range(256): 
		if i < threshold: 
			table.append(0)

		else: 
			table.append(1)

	image = image.point(table,'1') 
	print(tesserocr.image_to_text(image)) 