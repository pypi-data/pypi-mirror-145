import numpy as np

def intersect(box_a, box_b):
    """ We resize both tensors to [A,B,2] without new malloc:
    [A,2] -> [A,1,2] -> [A,B,2]
    [B,2] -> [1,B,2] -> [A,B,2]
    Then we compute the area of intersect between box_a and box_b.
    Args:
      box_a: (tensor) bounding boxes, Shape: [A,4].
      box_b: (tensor) bounding boxes, Shape: [B,4].
    Return:
      (tensor) intersection area, Shape: [A,B].
    """

    A = box_a.shape[0]
    B = box_b.shape[0]
    max_xy = np.minimum(np.broadcast_to(np.expand_dims(box_a[:, 2:], 1),(A, B, 2)),
                    np.broadcast_to(np.expand_dims(box_b[:, 2:], 0),(A, B, 2)))
    min_xy = np.maximum(np.broadcast_to(np.expand_dims(box_a[:, :2], 1),(A, B, 2)),
                    np.broadcast_to(np.expand_dims(box_b[:, :2], 0),(A, B, 2)))
    inter = np.clip((max_xy - min_xy), a_min=0, a_max=100000)
    return inter[:, :, 0] * inter[:, :, 1]


def jaccard(box_a, box_b):
    """Compute the jaccard overlap of two sets of boxes.  The jaccard overlap
    is simply the intersection over union of two boxes.  Here we operate on
    ground truth boxes and default boxes.
    E.g.:
        A ∩ B / A ∪ B = A ∩ B / (area(A) + area(B) - A ∩ B)
    Args:
        box_a: (tensor) Ground truth bounding boxes, Shape: [num_objects,4]
        box_b: (tensor) Prior boxes from priorbox layers, Shape: [num_priors,4]
    Return:
        jaccard overlap: (tensor) Shape: [box_a.size(0), box_b.size(0)]
    """
    inter = intersect(box_a, box_b)
    area_a = np.broadcast_to(np.expand_dims(((box_a[:, 2]-box_a[:, 0]) *
              (box_a[:, 3]-box_a[:, 1])),axis=1), inter.shape)  # [A,B]
    area_b = np.broadcast_to(np.expand_dims(((box_b[:, 2]-box_b[:, 0]) *
              (box_b[:, 3]-box_b[:, 1])),0), inter.shape)  # [A,B]
    union = area_a + area_b - inter
    return inter / union  # [A,B]


def overlap_similarity(box, other_boxes):
    """Computes the IOU between a bounding box and set of other boxes."""
    return jaccard(np.expand_dims(box,0), other_boxes).squeeze(0)


def _weighted_non_max_suppression(detections, num_coords, score_idx,min_suppression_threshold=0.3):
       
    if len(detections) == 0: return []

    output_detections = []

    # Sort the detections from highest to lowest score.
    remaining = np.argsort( -detections[:, score_idx])

    while len(remaining) > 0:
        detection = detections[remaining[0]]

        # Compute the overlap between the first box and the other 
        # remaining boxes. (Note that the other_boxes also include
        # the first_box.)
        first_box = detection[:4]
        other_boxes = detections[remaining, :4]
        ious = overlap_similarity(first_box, other_boxes)

        # If two detections don't overlap enough, they are considered
        # to be from different faces.
        mask = ious > min_suppression_threshold
        overlapping = remaining[mask]
        remaining = remaining[~mask]

        # Take an average of the coordinates from the overlapping
        # detections, weighted by their confidence scores.
        weighted_detection = detection.copy()
        if len(overlapping) > 1:
            coordinates = detections[overlapping, :num_coords]
            scores = detections[overlapping, score_idx:score_idx+1]
            total_score = scores.sum()
            # total_score = scores.sum()

            weighted = (coordinates * scores).sum(axis=0) / total_score
            weighted_detection[:num_coords] = weighted
            # weighted_detection[self.num_coords] = total_score / len(overlapping)

            weighted_detection[score_idx] = scores.max()


        output_detections.append(weighted_detection)

    return output_detections    