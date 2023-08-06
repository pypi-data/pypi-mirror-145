import collections
import enum
import os
from typing import Any, Iterable, List, Mapping, NamedTuple, Optional, Union
import numpy as np
from openvino.runtime import Core
from MediapipeOpenvino.face_detection.FaceDetection import FaceDetection
from MediapipeOpenvino.calculator import DetectionsToRect, ImageToTensor, ImageConvertOpencv
import cv2
import math
class Point3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __str__(self):
        return """This is Point3. x:{},y:{},z:{}""".format(self.x, self.y, self.z)
class FaceMeshPoint3:
    points = []
    
    def __init__(self,
                 xyz,
                 score,
                 roi):

        for x,y,z in xyz:
            # print("ss",x,y,z)
            x = x - 0.5
            y = y - 0.5
            new_x = math.cos(roi.rotation) * x - math.sin(roi.rotation) * y;
            new_y = math.sin(roi.rotation) * x + math.cos(roi.rotation) * y;
            new_x = new_x * roi.width + roi.center_x
            new_y = new_y * roi.height + roi.center_y
            new_z = z * roi.width
            self.points.append( Point3(new_x,new_y,new_z))
            self.score = score

class FaceMesh:
    
    expected_width = 192
    expected_height = 192
    
    def __init__(self, 
                 binary_openvino_name: str = "face_mesh.xml", 
                 device: str = "CPU") -> None:
        root_path = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])

        
        self.ie = Core()
        self.model = self.ie.read_model(model="{}".format(os.sep.join((root_path, binary_openvino_name))))
        self.compiled_model = self.ie.compile_model(model=self.model, device_name=device)
        
        self.fd = FaceDetection()
        
    def __call__(self,
                input_image):
        
        h, w, c = input_image.shape
        batch_det = self.fd(input_image)
        batch_rot = DetectionsToRect.ComputeRotation(batch_det, w, h)
        batch_ = []
        for batch in batch_rot:
            cur_ = []
            for dec_roi in batch:
                new_roi = ImageToTensor.GetRoi(w, h, dec_roi)
                crop_img, _= ImageConvertOpencv.convert(input_image, new_roi, self.expected_width, self.expected_height)
                crop_img = np.transpose(cv2.cvtColor(crop_img,cv2.COLOR_BGR2RGB), (2,0,1))
                crop_img = crop_img/255.0
                
                cur_.append( crop_img )
            batch_.append(cur_)
        output_layer_ir_0 = self.compiled_model.outputs[0]
        output_layer_ir_1= self.compiled_model.outputs[1]
        batch_mesh = []
        batch_score = []
        for i, batch in enumerate(batch_):
            cur_re = []
            re = self.compiled_model([np.array(batch)])
            for idx in range(re[output_layer_ir_1].shape[0]):
                cur_re.append( FaceMeshPoint3(re[output_layer_ir_0][idx], re[output_layer_ir_1][idx], batch_rot[i][idx]) )
          
            batch_mesh.append(cur_re)
               
        

      
     
        return batch_mesh
        
        
                 