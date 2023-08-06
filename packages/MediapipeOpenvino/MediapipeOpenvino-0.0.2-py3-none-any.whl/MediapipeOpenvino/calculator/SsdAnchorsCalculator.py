import numpy as np
import math
import cv2
from typing import List, Tuple



def CalculateScale(min_scale: float,
                   max_scale: float,
                   stride_index: int,
                   num_strides: int) -> float :
    if (num_strides == 1):
        return (min_scale + max_scale) * 0.5
    else:
        return min_scale + (max_scale - min_scale) * 1.0 * stride_index / (num_strides - 1.0)
    
def SsdAnchorsCalculator(num_layers: int,
                         min_scale: float,
                         max_scale: float,
                         input_size_height: int,
                         input_size_width: int,
                         anchor_offset_x: float,
                         anchor_offset_y: float,
                         strides: List[int],
                         aspect_ratios: List[float],
                         fixed_anchor_size: bool,
                         interpolated_scale_aspect_ratio: float,
                         reduce_boxes_in_lowest_layer: bool = False) -> List[Tuple[int, int,int,int]] :
    assert num_layers == len(strides), "numpy_layers must be equal to strides"
    anchors = []
    layer_id = 0
    while layer_id < num_layers:
        anchor_height, anchor_width, aspect_ratios_, scales = [], [], [], []
        
        # For same strides, we merge the anchors in the same order.
        last_same_stride_layer = layer_id
        while last_same_stride_layer < len(strides) and strides[last_same_stride_layer] == strides[layer_id]:
            scale = CalculateScale(min_scale, max_scale, last_same_stride_layer, len(strides) )
            
            # For first layer, it can be specified to use predefined anchors.
            if (last_same_stride_layer == 0) and reduce_boxes_in_lowest_layer:
                aspect_ratios_.append(1.0)
                aspect_ratios_.append(2.0)
                aspect_ratios_.append(0.5)
                scales.append(0.1)
                scales.append(scale)
                scales.append(scale)
            else:
                for ar in aspect_ratios:
                    aspect_ratios_.append(ar)
                    scales.append(scale)
            
            if interpolated_scale_aspect_ratio > 0.:
                scale_next  = 1.0 if last_same_stride_layer == (len(strides) - 1) else CalculateScale(min_scale, max_scale, last_same_stride_layer+1, len(strides))
                aspect_ratios_.append(interpolated_scale_aspect_ratio)
                scales.append(math.sqrt(scale*scale_next))
            last_same_stride_layer += 1
        for i in range(len(aspect_ratios_)):
            ratio_sqrts = math.sqrt(aspect_ratios_[i])
            anchor_height.append(scales[i] / ratio_sqrts)
            anchor_width.append(scales[i] * ratio_sqrts)

        cur_stride  = strides[layer_id]
        feature_map_height =math.ceil(1.0 * input_size_height / cur_stride)
        feature_map_width =math.ceil(1.0 * input_size_width / cur_stride)
        
        for y in range(feature_map_height):
            for x in range(feature_map_width):
                for anchor_id in range(len(anchor_height)):
                    x_center = (x + anchor_offset_x) * 1.0 / feature_map_width
                    y_center = (y + anchor_offset_y) * 1.0 / feature_map_height
                    if fixed_anchor_size:
                        anchors.append((x_center, y_center, 1.0, 1.0))
                    else:
                        anchors.append((x_center, y_center, anchor_width[anchor_id], anchor_height[anchor_id]))
        layer_id = last_same_stride_layer
    return anchors