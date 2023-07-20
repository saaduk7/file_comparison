from PIL import Image
import numpy as np
import scipy.signal

def calculate_image_shift(im1, im2):
    im1 = np.asarray(im1)
    im2 = np.asarray(im2)
    # get rid of the color channels by performing a grayscale transform
    # the type cast into 'float' is to avoid overflows
    im1_gray = np.sum(im1.astype('float'), axis=2)
    im2_gray = np.sum(im2.astype('float'), axis=2)

    # get rid of the averages, otherwise the results are not good
    im1_gray -= np.mean(im1_gray)
    im2_gray -= np.mean(im2_gray)

    # calculate the correlation image; note the flipping of onw of the images
    img_corr = scipy.signal.convolve(im1_gray, im2_gray[::-1,::-1], mode='same')
    shifted_centre = np.unravel_index(np.argmax(img_corr), img_corr.shape)
    img_center = [295, 512]
    return img_center[1] - shifted_centre[1], img_center[0] - shifted_centre[0]

def resize(img, bw=1024):
    basewidth = bw
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize))
    return img

from os.path import isfile, join, splitext

def read_images_and_resize(image0, image1):
    a = Image.open(image0)
    b = Image.open(image1)
    #a.save(splitext(image0)[0]+".png")
    #b.save(splitext(image1)[0]+".png")
    a = resize(a)
    b = resize(b)
    return a, b

def compare_images(image0, image1):
    image0, image1 = read_images_and_resize(image0, image1)
    image_shift = calculate_image_shift(image0, image1)
    shift_str = ""
    if abs(image_shift[0]) > 0:
        shift_str += f"Image shift on x-axis by {image_shift[0]} pixels  "
    if abs(image_shift[1]) > 0:
        shift_str += f"Image shift on y-axis by {image_shift[1]} pixels"
    
    if shift_str:
        return shift_str
    else:
        return False
