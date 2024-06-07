import numpy as np
import cv2 as cv

vid_capture = cv.VideoCapture(0, cv.CAP_DSHOW)

if vid_capture.isOpened() == False:
    print("Error opening the video file")
    exit()

frame_width = int(vid_capture.get(3))
frame_height = int(vid_capture.get(4))
frame_size = (frame_width,frame_height)
fps = 20

while True:
    ret, frame = vid_capture.read()
    if not ret:
        print("Not receiving frame, exiting\n")
        break

    image = cv.cvtColor(frame, cv.COLOR_BGR2RGB);
    cv.imshow('frame', image)

vid_capture.release()
cv.destroyAllWindows()
