import numpy as np
import cv2 as cv

vid_capture = cv.VideoCapture(0, cv.CAP_DSHOW)
if vid_capture.isOpened() == False:
    print("Error opening the video file")
else:
    frame_width = int(vid_capture.get(3))
    frame_height = int(vid_capture.get(4))
    frame_size = (frame_width,frame_height)
    fps = 20
    