from PIL import Image, ImageDraw
import cv2
import numpy as np



def create_portrait(image, directory, index):

    img = Image.open(image).convert("RGB")

    npImage=np.array(img)
    h,w=img.size
    print(img.size)
    x = min(img.size)

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,x,x],0,360,fill=255)

    # Convert alpha Image to numpy array
    npAlpha=np.array(alpha)

    # Add alpha layer to RGB
    npImage=np.dstack((npImage,npAlpha))

    # Save with alpha
    npImage = npImage[0:x, 0:x]
    img = Image.fromarray(npImage)

    new_img_size = int(0.1*x)
    img = img.resize((new_img_size, new_img_size))

    save_loc = "{0}/result_{1}.png".format(directory, index)
    img.save(save_loc)

    return save_loc
