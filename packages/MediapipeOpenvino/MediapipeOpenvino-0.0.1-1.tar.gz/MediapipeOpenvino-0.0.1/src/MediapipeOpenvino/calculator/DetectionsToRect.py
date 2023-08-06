import math
from . import ImageToTensor, RectTransformation
M_PI = 3.1415926
def NormalizeRadians(angle):
    return angle - 2 * M_PI * math.floor((angle - (-M_PI)) / (2 * M_PI));

def ComputeRotation(location_data, input_image_width, input_image_height, target_angle_ = 0.):
    batch_rot = []
    for batch in location_data: 
        cur_rect = []
        for dec in batch:
            
            x1 = dec.left_eye_x * input_image_width
            y1 = dec.left_eye_y * input_image_height
            x0 = dec.right_eye_x * input_image_width
            y0 = dec.right_eye_y * input_image_height
            # print( dec.left_eye_x, dec.left_eye_y, dec.right_eye_x, dec.right_eye_y, input_image_width, input_image_height)
            rot = NormalizeRadians(target_angle_ - math.atan2(-(y1 - y0), x1 - x0))
            rect = ImageToTensor.RotatedRect((dec.xmax + dec.xmin)*.5,
                                                      (dec.ymax + dec.ymin)*.5,
                                                      (dec.xmax - dec.xmin),
                                                      (dec.ymax - dec.ymin),
                                                      rot=rot)
            print(rect)
            RectTransformation.TransformNormalizedRect(rect, input_image_width, input_image_height)
            print("square rect: ", rect)
            cur_rect.append(rect )
        batch_rot.append( cur_rect )
    return batch_rot