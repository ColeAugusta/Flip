import numpy as np
import cv2 as cv

capture = cv.VideoCapture(0);
if not capture.isOpened():
    print("ERROR: camera not opened")
    exit()