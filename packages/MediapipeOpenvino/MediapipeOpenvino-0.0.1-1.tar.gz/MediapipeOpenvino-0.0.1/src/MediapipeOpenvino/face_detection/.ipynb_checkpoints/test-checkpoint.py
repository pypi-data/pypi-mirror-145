import sys
from pathlib import Path
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3]))

from MediapipeOpenvino.calculator import ImageToTensor, SsdAnchorsCalculator, TensorsToDetections, NonMaximumSuppression, ImageConvertOpencv
import cv2
import numpy as np
from openvino.runtime import Core
from MediapipeOpenvino.face_detection import FaceDetection

import mediapipe as mp

if __name__ == "__main__":
    target_width, target_height = 128, 128
    capture = cv2.VideoCapture("video2.mp4")
    if capture.isOpened():
        hasFrame, frame = capture.read()
    capture.release()
    
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils

    # For static images:

    with mp_face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.5) as face_detection:
       

        # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
        results = face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Draw face detections of each face.
        if  results.detections:
            annotated_image = frame.copy()
            for detection in results.detections:
                print('Nose tip:')
                print(mp_face_detection.get_key_point(
                  detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
                mp_drawing.draw_detection(annotated_image, detection)
          

    
    h, w, c = frame.shape
    fd = FaceDetection()

    re = fd(frame)
    
    # print(h,w)
    for batch in re: ## this test we only have one image
        for dec in batch:
            print(dec)
            img = cv2.rectangle(annotated_image, (int(dec.xmin*w),int(dec.ymin*h)), (int(dec.xmax*w),int(dec.ymax*h)), (255, 0, 0), 1)
    cv2.imwrite("test.jpg",img)
    
    
    
    


    
    
