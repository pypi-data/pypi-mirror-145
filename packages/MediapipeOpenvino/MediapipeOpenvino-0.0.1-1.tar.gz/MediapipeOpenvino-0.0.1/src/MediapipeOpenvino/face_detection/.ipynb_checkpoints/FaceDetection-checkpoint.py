import collections
import enum
import os
from typing import Any, Iterable, List, Mapping, NamedTuple, Optional, Union
import numpy as np
import cv2
from openvino.runtime import Core
from MediapipeOpenvino.calculator import SsdAnchorsCalculator, ImageToTensor, TensorsToDetections, NonMaximumSuppression, ImageConvertOpencv
 #  RIGHT_EYE = 0
 #  LEFT_EYE = 1
 #  NOSE_TIP = 2
 #  MOUTH_CENTER = 3
 #  RIGHT_EAR_TRAGION = 4
 #  LEFT_EAR_TRAGION = 5
class FaceDetectionResult:
    indexNames = ['ymin','xmin','ymax','xmax', 'right_eye_x', 'right_eye_y', 'left_eye_x','left_eye_y',
                  'nose_tip_x','nose_tip_y','mouth_center_x','mouth_center_y','right_ear_tragion_x','right_ear_tragion_y',
                  'left_ear_tragion_x','left_ear_tragion_y','score']
    
    def __init__(self, predict_data):
        assert len(self.indexNames) == len(predict_data)
        
        for i in range(len(self.indexNames)):
            setattr(self, self.indexNames[i], predict_data[i])
        self.data_ = predict_data
        
    def __str__(self):
        return """This is FaceDetectionResult. xmin:{},ymin:{},xmax:{},ymax:{}""".format(self.xmin, self.ymin, self.xmax, self.ymax)

class FaceDetection:
    
    expected_width = 128
    expected_height = 128
    
    def __init__(self, 
                 binary_openvino_name: str = "face_detection.xml", 
                 device: str = "CPU") -> None:
        root_path = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])

        
        self.ie = Core()
        self.model = self.ie.read_model(model="{}".format(os.sep.join((root_path, binary_openvino_name))))
        self.compiled_model = self.ie.compile_model(model=self.model, device_name=device)
        self.anchors = SsdAnchorsCalculator.SsdAnchorsCalculator(4, 0.1484375, 0.75, 128, 128, 0.5, 0.5, [8, 16, 16, 16], [1.0], True, 1.0) 
        self.anchors = np.array(self.anchors)
        
    def __call__(self,
                input_image):
        
   
        h, w, c = input_image.shape
   
        roi = ImageToTensor.GetRoi(w, h)
        padding = ImageToTensor.PadRoi(self.expected_width, self.expected_height, True, roi)
        img, transform_matrix = ImageConvertOpencv.convert(input_image, roi, self.expected_width,self.expected_height)
        
        # print(transform_matrix)
        input_image = np.expand_dims( np.transpose(cv2.cvtColor(img,cv2.COLOR_BGR2RGB), (2,0,1)), 0)
        input_image = input_image/127.5 - 1.0
        
        
        re = self.compiled_model([input_image])
        output_layer_ir_0 = self.compiled_model.outputs[0]
        output_layer_ir_1= self.compiled_model.outputs[1]
        raw_box = self.compiled_model([input_image])[output_layer_ir_0]
        raw_score = self.compiled_model([input_image])[output_layer_ir_1]
 
    
        ### decode boxes 

        detection_boxes = TensorsToDetections._decode_boxes(raw_box, self.anchors, 128, 128, 128, 128, 4, 6, 2)
       
        ### score clipping
        score_clipping_thresh = 100
        raw_score = np.clip(raw_score, -score_clipping_thresh, score_clipping_thresh)
        raw_score = 1 / (1 + np.exp(-raw_score)) ## sigmoid 
        detection_scores = np.squeeze(raw_score, axis=-1)

        ### filtered boxes
        min_score_thresh = 0.5
        mask = detection_scores >= min_score_thresh
        output_detections = []
        for i in range(raw_score.shape[0]):
            boxes = detection_boxes[i, mask[i]]
            scores = np.expand_dims( detection_scores[i, mask[i]], axis=-1 )
            output_detections.append(np.concatenate((boxes, scores), axis=-1))

        ## WNMS
        filtered_detections = []
        for i in range(len(output_detections)):
            faces = NonMaximumSuppression._weighted_non_max_suppression(output_detections[i], 16, 16)
            faces = np.stack(faces) if len(faces) > 0 else np.zeros((0, 17))
            filtered_detections.append(faces)
        filtered_detections = np.array(filtered_detections)

        ### project detections to original image
         # return {p.x() * project_mat[0] + p.y() * project_mat[1] + project_mat[3],
         #        p.x() * project_mat[4] + p.y() * project_mat[5] + project_mat[7]};
        def project_fn(a):
            key_points = a[4:].copy()
            key_points[0:-1:2] = key_points[0:-1:2]*transform_matrix[0][0] +  key_points[1:-1:2]*transform_matrix[0][1] + transform_matrix[0][3] 
            key_points[1:-1:2] = key_points[0:-1:2]*transform_matrix[1][0] +  key_points[1:-1:2]*transform_matrix[1][1] + transform_matrix[1][3] 
            
            tmp_b = a[:4].copy() # ymin xmin ymax xmax
            tmp_b[[0,2]] = tmp_b[[2,0]]
            tmp_b[1::2] = tmp_b[1::2]*transform_matrix[0][0] +  tmp_b[0::2]*transform_matrix[0][1] + transform_matrix[0][3] 
            # print(a[1:-1:2])
            tmp_b[0::2] = tmp_b[1::2]*transform_matrix[1][0] + tmp_b[0::2]*transform_matrix[1][1] + transform_matrix[1][3] 
            
            a[1:4:2] = a[1:4:2]*transform_matrix[0][0] +  a[0:4:2]*transform_matrix[0][1] + transform_matrix[0][3] 
            a[0:4:2] = a[1:4:2]*transform_matrix[1][0] +  a[0:4:2]*transform_matrix[1][1] + transform_matrix[1][3] 
            nymin= min(tmp_b[0],tmp_b[2],a[0],a[2])
            nxmin = min(tmp_b[1],tmp_b[3],a[1],a[3])
            nymax = max(tmp_b[0],tmp_b[2],a[0],a[2])
            nxmax = max(tmp_b[1],tmp_b[3],a[1],a[3])
            a[:4] = nymin,nxmin,nymax,nxmax
            a[4:] = key_points
            return a
        # print( np.apply_along_axis(project_fn, 2,filtered_detections))
        final_detections = np.apply_along_axis(project_fn, 2,filtered_detections)
        print(final_detections)
        batch_detections = []
        for bi in range(final_detections.shape[0]):
            cur_det = []
            for idx in range(final_detections.shape[1]):
                cur_det.append(FaceDetectionResult(final_detections[bi][idx]))
            batch_detections.append(cur_det)
        return batch_detections
        
        
                 