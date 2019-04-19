# SOURCED FROM jedwards ANSWER ON STACKOVERFLOW
# The code has been edited in order to suit this application better
# https://stackoverflow.com/questions/29313667/how-do-i-remove-the-background-from-this-kind-of-image

import cv2
import numpy as np

def remove_bg(img):
    # Setting up parameters
    print('Setting up parameters...')
    BLUR = 19
    CANNY_THRESH_1 = 10
    CANNY_THRESH_2 = 200
    MASK_DILATE_ITER = 10
    MASK_ERODE_ITER = 10
    MASK_COLOR = (0.0, 0.0, 0.0) # In BGR format

    # Reading image
    print('Reading image...')
    try:
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    except:
        img = img * 255
        gray = cv2.cvtColor(img.astype('uint8'),cv2.COLOR_BGR2GRAY)
    
    # Detecting edges
    print('Detecting edges...')
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    # Find contours
    print('Creating contours...')
    contour_info = []
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))


    # Creating and filling mask
    print('Setting up mask...')
    mask = np.zeros(edges.shape)
    for i in range(len(contour_info)):
        cv2.fillConvexPoly(mask, contour_info[i][0], (255))

    # Smoothing and blurring mask
    print('Smoothing and blurring mask...')
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

    # Blending mask into background
    print('Blending mask into background...')
    mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
    img         = img.astype('float32') / 255.0                 #  for easy blending

    masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend
    masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit 

    return masked
