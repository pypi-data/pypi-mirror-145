from typing import Tuple, Type
import numpy as np
import math

M_PI = 3.14159265358979323846  

class RotatedRect:
    center_x = 0
    center_y = 0
    width = 0
    height = 0
    rotation = 0
    
    def __init__(self, 
                 cx: float, 
                 cy: float, 
                 width: float, 
                 height: float, 
                 rot: float = 0) -> None:
        self.center_x = cx
        self.center_y = cy
        self.width = width
        self.height = height
        self.rotation = rot
    def getBoxPointsInput(self):
        return ((self.center_x,self.center_y), (self.width,self.height),self.rotation * 180. / M_PI)
    def __str__(self):
        return """This is RotateRect. cx:{},cy:{},width:{},height:{},rotation:{}.""".format(self.center_x, self.center_y, self.width, self.height, self.rotation)
        

def GetRoi(width: int,
           height: int,
           roi: Type[RotatedRect] = None ) -> Type[RotatedRect]:
    if roi:
        return RotatedRect( roi.center_x*width, roi.center_y*height, roi.width*width, roi.height*height, roi.rotation)
    return RotatedRect( 0.5*width, 0.5*height, width, height)

def PadRoi(input_tensor_width: int,
           input_tensor_height: int,
           keep_aspect_ratio: bool,
           roi: Type[RotatedRect]) -> Tuple[float, float, float, float] :
    
    if not keep_aspect_ratio:
        return (0., 0., 0., 0.)
    
    assert input_tensor_width > 0 and input_tensor_height > 0, "Input tensor width and height must be > 0." 
    assert roi.width > 0 and roi.height > 0, "ROI width and height must be > 0."
    print("input",roi)
    tensor_aspect_ratio = 1.*input_tensor_height / input_tensor_width
    
    roi_aspect_ratio = roi.height / roi.width
    
    vertical_padding, horizontal_padding = 0., 0.
    if tensor_aspect_ratio > roi_aspect_ratio:
        new_width = roi.width
        new_height = roi.width * tensor_aspect_ratio
        vertical_padding = (1.0 - roi_aspect_ratio / tensor_aspect_ratio) / 2.0;
    else:
        new_width = roi.height / tensor_aspect_ratio
        new_height = roi.height
        horizontal_padding = (1.0 - tensor_aspect_ratio / roi_aspect_ratio) / 2.0;
    roi.width = new_width
    roi.height = new_height

    return (horizontal_padding, vertical_padding, horizontal_padding, vertical_padding)

def GetRotatedSubRectToRectTransformMatrix(sub_rect: Type[RotatedRect],
                                           rect_width: int,
                                           rect_height: int,
                                           flip_horizontaly: bool = False) -> np.ndarray:
    a = sub_rect.width
    b = sub_rect.height
    flip = -1 if flip_horizontaly else 1
    c = math.cos(sub_rect.rotation)
    d = math.sin(sub_rect.rotation)
    e = sub_rect.center_x
    f = sub_rect.center_y
    g = 1. / rect_width
    h = 1. / rect_height
    
    matrix = np.zeros((4,4), dtype = np.float32)
    
    matrix[0][0] = a * c * flip * g
    matrix[0][1] = -b * d * g
    matrix[0][2] = 0.0
    matrix[0][3] = (-0.5 * a * c * flip + 0.5 * b * d + e) * g

    matrix[1][0] = a * d * flip * h
    matrix[1][1] = b * c * h
    matrix[1][2] = 0.0
    matrix[1][3] = (-0.5 * b * c - 0.5 * a * d * flip + f) * h

    matrix[2][0] = 0.0
    matrix[2][1] = 0.0
    matrix[2][2] = a * g
    matrix[2][3] = 0.0

    matrix[3][0] = 0.0
    matrix[3][1] = 0.0
    matrix[3][2] = 0.0
    matrix[3][3] = 1.0

    
    return matrix