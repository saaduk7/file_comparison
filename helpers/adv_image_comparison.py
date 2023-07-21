import cv2
import numpy as np
import sys
from PIL import Image
import pyemf3
from scipy.linalg import norm


"""
A list of a numbers that represent different elements present in emf file according to pyemf library.
90: POLYPOLYLINE16
95: EXTCREATEPEN
36: MODIFYWORLDTRANSFORM
37: SELECTOBJECT
40: DELETEOBJECT
86: POLYGON16: all the boxes mainly
81: STRETCHEDBITS : images

22: SETTEXTALIGN
24: SETTEXTCOLOR
82: EXTCREATEFONTDIRECTW
84: EXTTEXTOUTW
38: CREATEPEN
87: POLYLINE16: with cptl = 501 are graphs
14: EOF
""" 


def text_comparison(img0, img1):
    """
    compares the text part of images to see if they have different color or text value.
    returns the difference as list.
    """
    diff_list = list()
    for key, value in img0["text"].items():
        if key in img1["text"].keys():
            if value["text"] == img1["text"][key]["text"]:
                if value["color"] != img1["text"][key]["color"]:
                    diff_list.append(f"Different Color for Text {value['text']}")
            else:
                diff_list.append(f"Different Text value Image1: {value['text']}, Image2: {img1['text'][key]['text']}")
                
    return diff_list

def extract_logos_text_and_graphs(img):
    """
    extract logos, texts, and graphs from the emf image and returns their respective information like text, color,
    or their rectangular bounds.
    """
    info_list = {"logo": {}, "text": {}, "graphs": []}
    for rec in img.records:
        if rec.iType == 24:
            current_color = rec.crColor
        elif rec.iType in [83, 84]:
            info_list["text"][rec.ptlReference_x, rec.ptlReference_y] =  {"text": rec.string, "rcl":rec.rclBounds, "color": current_color}
        elif rec.iType in [81]:
            info_list["logo"][rec.xDest, rec.yDest]={"rcl":rec.rclBounds}
        elif rec.iType in [87] and rec.cptl == 501:
            info_list["graphs"].append({"rcl":rec.rclBounds, "cptl": rec.cptl, "aptl": rec.aptl})
    return info_list

def fixed_resize(img, bw=7680, hsize=5336):
    img = img.resize((bw,hsize))
    return img

def compare_images(img1, img2):
    """
    compare images to check if the curves present in the graph are same or not.
    """
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    (_, img1) = cv2.threshold(img1, 0, 255, cv2.THRESH_BINARY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    (_, img2) = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY)
    # calculate the difference and its norms
    diff = img1 - img2  # elementwise for scipy arrays
    m_norm = np.sum(abs(diff))  # Manhattan norm
    z_norm = norm(diff.ravel(), 0)  # Zero norm
    return (m_norm, z_norm)

def get_image_from_rcl(img, rcl):
    return img[rcl[0][1]:rcl[1][1] , rcl[0][0]:rcl[1][0]]

def compare_graphs(img1_info, img1, img2):
    diff_threshold = 10
    for graph in img1_info["graphs"]:   
        (m_norm, z_norm) =compare_images( get_image_from_rcl(img1, graph['rcl']),  get_image_from_rcl(img2, graph['rcl'])  )
        if z_norm > diff_threshold:
            return "Difference in curves"
        

def compare_image_files(img1, img2):
    """
    reads the emf files and extract elements like logo, cruves, text etc and compare them to their counterparts.
    return difference list.
    """
    diff_list = list()
    # Load the emf version via pyemf3 library
    options = {'verbose': False, 'save': False, 'outputfile': None}  
    emf_a= pyemf3.EMF(verbose=False)
    emf_a.load(img1)
    emf_b= pyemf3.EMF(verbose=False)
    emf_b.load(img2)
    
    # load via PIL library for opencv processing
    a = fixed_resize(Image.open(img1))
    b = fixed_resize(Image.open(img1))
    image_1 = np.array(a) 
    image_2 = np.array(b)
    # extract information from emf images.
    a_info = extract_logos_text_and_graphs(emf_a)
    b_info = extract_logos_text_and_graphs(emf_b)
    
    # find difference between text and their color
    text_diff = text_comparison(a_info, b_info)
    if text_diff:
        diff_list.extend(text_diff)
    
    # compare curves/graphs
    graph_diff = compare_graphs(a_info, image_1, image_2)
    if graph_diff:
        diff_list.append(graph_diff)
        
    # compare images like logo etc.
    for logo in a_info["logo"]:
        logo_thresh = 10
        _, z_norm = compare_images(get_image_from_rcl(image_1, a_info["logo"][logo]['rcl']), get_image_from_rcl(image_2, b_info["logo"][logo]['rcl']) )
        if z_norm > logo_thresh:
            return diff_list.append(f"Difference in images/logos")
    return diff_list
