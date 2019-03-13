from PIL import Image, ImageDraw
import cv2
import numpy as np


img_width = 500
img_height = 500

img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 255))
img = np.asarray(img)

cv2.circle(img, (int(img_width/2), int(img_height/2)), int(img_width/4), (100, 100, 100), 10)
cv2.imwrite('test-img.png', img)

image = cv2.imread('./test-img.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
img[np.all(img == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]
cv2.imwrite('test-img.png', img)



# image = Image.new('RGBA', (200, 200))
# draw = ImageDraw.Draw(image)
# draw.ellipse((20, 20, 180, 180), fill = 'blue', outline ='blue')
# draw.point((100, 100), 'red')
# image.save('test.png')
# img = np.zeros((img_width, img_height, 3), np.uint8)
# cv2.line(img,(0,0),(511,511),(255,0,0),10) 