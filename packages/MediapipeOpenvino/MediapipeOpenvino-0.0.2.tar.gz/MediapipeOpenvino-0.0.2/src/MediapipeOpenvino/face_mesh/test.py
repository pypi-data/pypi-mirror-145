import sys
from pathlib import Path
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-3]))


import cv2
import numpy as np
from openvino.runtime import Core
from MediapipeOpenvino.face_mesh import FaceMesh

import mediapipe as mp

if __name__ == "__main__":

    capture = cv2.VideoCapture("video3.mp4")
    if capture.isOpened():
        hasFrame, frame = capture.read()
    capture.release()
    
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=2,
        refine_landmarks=False,
        min_detection_confidence=0.5) as face_mesh:
  
       
        # Convert the BGR image to RGB before processing.
        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Print and draw face mesh landmarks on the image.
        if not results.multi_face_landmarks:
            exit(-1)
        annotated_image = frame.copy()
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
              image=annotated_image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_TESSELATION,
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles
              .get_default_face_mesh_tesselation_style())


    h, w, c = frame.shape
    fm = FaceMesh()
    
    batch_re = fm( frame )
    for batch in batch_re:
        for face_ in batch:
            for idx, face_point in enumerate(face_.points):
                print(face_point, results.multi_face_landmarks[idx//468].landmark[idx % 468])
                cv2.circle(annotated_image, (int(face_point.x*w), int(face_point.y*h)), 1, (0, 255, 0), thickness=1)
    
    cv2.imwrite("mesh.jpg",annotated_image)
    
    


    
    
