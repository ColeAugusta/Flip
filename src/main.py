from mediapipe.tasks.python import vision
from GestureLogger import GestureLogger
from mediapipe.tasks import python
from tkinter import *
from PIL import Image, ImageTk
import pyautogui as pgui
import mediapipe as mp
import time
import math
import cv2

def runFlip():

    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open/find camera. Please ensure that a camera is connected and accessible.")
        # Optionally, display an error message in the GUI
        error_window = Tk()
        error_window.title("Error")
        Label(error_window, text="Could not open/find camera.\nPlease ensure that a camera is connected.", font=('Ubuntu', 14)).pack(pady=20)
        Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)
        error_window.mainloop()
        return
    
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(static_image_mode=False,
                        max_num_hands=2,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)
    mpDraw = mp.solutions.drawing_utils
    pTime = 0
    cTime = 0

    # get size of screen for pyautogui
    # and move cursor to bottom center
    pguiSize = pgui.size()
    pgui.moveTo(math.floor(.50 * pguiSize[0]), math.floor(.80 * pguiSize[1]))
    status = ""
    scrollAmt = 0
    
    while True:
        #reads the image
        success, img = cap.read()
        #change color to RGB for detection using mediapipe
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #processes each image
        results = hands.process(imgRGB)

        #processes RGB image with gesture logger model
        logger = GestureLogger(video_mode=False)
        logger.detect(imgRGB) 


        h, w, c = img.shape

        #if there are results, if they find some sort of hand.
        if results.multi_hand_landmarks:
            cordlist = []
            #for every "point" of the hand in the results
            for handLms in results.multi_hand_landmarks:
                #for every point, there is an id and a location of the point of the hand. this loops through all of them. 
                for id, lm in enumerate(handLms.landmark):
                    
                    if id == 8:
                        cx, cy = int(lm.x *w), int(lm.y*h)

                        # store circle cords
                        cords = (cx, cy)
                        cordlist.append(cords)

                        #if id ==0:
                        #makes a small circle at each "point" of the hand
                        cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)
                #actually draws the circle on the image.
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # for all lm cords, determine status of
            # hand and scroll accordingly
            status = "wait"
            for i in range(len(cordlist)):
                # print(f"x: {cordlist[i][0]} y: {cordlist[i][1]}")

                # hand is in the upper 1/3 (ish) of the screen scroll
                # up, if continuously holding in one direction 
                # scroll speeds up
                if cordlist[i][1] < 200:
                    status = "scrolling up"
                    if scrollAmt < 0:
                        scrollAmt = 0
                    pgui.scroll(scrollAmt)
                    scrollAmt += 10
                    status = "wait"
                # hand is in the lower 1/3 (ish) of the screen scroll
                # down
                if cordlist[i][1] > 400:
                    status = "scrolling down"
                    if scrollAmt > 0:
                        scrollAmt = 0
                    pgui.scroll(scrollAmt)
                    scrollAmt -= 10
                    status = "wait"


        #gets FPS
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        #puts FPS in image
        cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        #shows image
        cv2.imshow("Image", img)
        #lets user press "q" button to exit program
        if cv2.waitKey(1) & 0xFF == ord('q'):#close using q
            break

    # end capture and destroy window
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":


    # create window to start Flip app
    window = Tk()
    window.title("Flip")
    window.iconbitmap("logo.ico")
    window.geometry("600x600")

    # fill window with widgets
    frame = Frame(window)
    frame.pack()
    label = Label(frame, text = "Welcome to Flip!", font = ('Ubuntu', 24))
    label.pack()
    label = Label(frame, text = "swipe up/down to scroll up/down, q to quit", font = ('Ubuntu', 16))
    label.pack()
    img = Image.open("flip.png")
    img = img.resize((100, 100))
    image = PhotoImage(file="flip.png")
    label = Label(frame, image = image)
    label.pack()
    button = Button(frame, text = "Run", command = runFlip)
    button.pack()

    window.mainloop()