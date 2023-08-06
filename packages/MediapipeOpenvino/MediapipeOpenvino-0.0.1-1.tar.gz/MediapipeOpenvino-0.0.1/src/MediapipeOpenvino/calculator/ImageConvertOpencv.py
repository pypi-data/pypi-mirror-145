from . import ImageToTensor
import cv2
import numpy as np
def convert(frame,
            roi, 
            ouput_width,
            output_height):
    h, w, c = frame.shape

    transform_matrix = ImageToTensor.GetRotatedSubRectToRectTransformMatrix(roi, w, h)


    src = cv2.boxPoints(roi.getBoxPointsInput())
    print(src)
    dst = np.array([[0., output_height*1.], [0., 0.], [ouput_width*1., 0.], [ouput_width*1.,output_height*1.]], np.float32)

    M = cv2.getPerspectiveTransform(src, dst)

    img = cv2.warpPerspective(frame, M, (ouput_width, output_height),cv2.INTER_LINEAR,borderValue=0)
    return img, transform_matrix