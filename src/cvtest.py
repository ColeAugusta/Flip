import cv2
import mediapipe as mp
import time



cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    #reads the image
    success, img = cap.read()
    #change color to RGB for detection using mediapipe
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #processes each image
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    #if there are results, if they find some sort of hand.
    if results.multi_hand_landmarks:
        #for every "point" of the hand in the results
        for handLms in results.multi_hand_landmarks:
            #for every point, there is an id and a location of the point of the hand. this loops through all of them. 
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                #if id ==0:
                #makes a small circle at each "point" of the hand
                cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)
            #actually draws the circle on the image.
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

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

cap.release()
cv2.destroyAllWindows()