from mediapipe.tasks.python import vision
from mediapipe.tasks import python
import mediapipe as mp
import numpy as np

# GestureLogger class to handle using the mediapipe
# gesture recognition data and its related functions
class GestureLogger:

    # init GestureLogger obj and recognizer w/ options
    def __init__(self, video_mode: bool = False):
        #init video mode
        self.video_mode = video_mode

        #init options for gesture recognizer obj
        base_options = python.BaseOptions(
            model_asset_path = 'gesture_recognizer.task'
        )
        options = vision.GestureRecognizerOptions(
            base_options = base_options,
            running_mode = mp.tasks.vision.RunningMode.VIDEO
        )
        #init recognizer obj
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    
    def detect(self, image: np.ndarray[np.uint8]) -> None:
        #creates image in mp format, calls recognizer
        image = mp.Image(
            image_format = mp.ImageFormat.SRGB,
            data = image
        )
        recognizer_result = self.recognizer.recognize(image)

        #print top result from recognizer obj
        for i, gesture in enumerate(recognizer_result.gestures):
            print("Gesture result: ", gesture[0].category_name)
        
        #get hand landmarks if hand found
        if recognizer_result.hand_landmarks:
            hand_lms = recognizer_result.hand_landmarks
            print("landmark: ", str(hand_lms))