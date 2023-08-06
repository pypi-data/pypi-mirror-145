from dataclasses import Field
from typing import List
from pydantic import BaseModel, Field, root_validator, validator

def labels_validator(v: List[int]) -> List[int]:
    if not isinstance(v, List):
        raise TypeError(v)
    
    if len(v) < 1:
        raise ValueError('There must be at least one id')

    return v

def boxes_validator(v: List[List[int]]) -> List[List[int]]:
    if not isinstance(v, List):
        raise TypeError(v)
    
    if len(v) < 1:
        raise ValueError('There must be at least one id')

    return v

def detection_scores_validator(v: List[float]) -> List[float]:
    if not isinstance(v, List):
        raise TypeError(v)
    
    if len(v) < 1:
        raise ValueError('There must be at least one score')

    return v

def masks_validator(v: List[List[int]]) -> List[List[int]]:
    if not isinstance(v, List):
        raise TypeError(v)
    
    if len(v) < 1:
        raise ValueError('There must be at least one id')

    return v
    


class PredictionFormat(BaseModel):
    pass

class ClassificationPredictionFormat(PredictionFormat):
    labels: List[int] = Field(alias="label_id")
    detection_scores: List[float] = Field(alias="score")

    @validator('labels', pre=True)
    def to_label_ids(cls, v):
        if isinstance(v, int):
            return [v]
        elif isinstance(v, List):
            return v
        raise TypeError(v)

    @validator('detection_scores', pre=True)
    def to_score_list(cls, v):
        if isinstance(v, float) or isinstance(v, int):
            return [float(v)]
        elif isinstance(v, List):
            return v
        raise TypeError(v)

    _validate_labels = validator('labels', allow_reuse=True)(labels_validator)
    _validate_scores = validator('detection_scores', allow_reuse=True)(detection_scores_validator)
    
class DetectionPredictionFormat(PredictionFormat):
    labels: List[int] = Field(alias='label_ids')
    boxes: List[List[int]] = Field(alias='boxes')
    detection_scores: List[float] = Field(alias='detection_scores')

    _validate_labels = validator('labels', allow_reuse=True)(labels_validator)
    _validate_scores = validator('detection_scores', allow_reuse=True)(detection_scores_validator)
    _validate_boxes = validator('boxes', allow_reuse=True)(boxes_validator)

    @root_validator
    def check_sizes(cls, values):
        labels, detection_scores, boxes = values.get('labels'), values.get('detection_scores'), values.get('boxes')
        
        if labels is None or detection_scores is None or boxes is None is None or len(labels) != len(detection_scores) or len(boxes) != len(labels):
            raise ValueError('incoherent lists')

        return values


class SegmentationPredictionFormat(PredictionFormat):
    labels: List[int] = Field(alias='label_ids')
    boxes: List[List[int]] = Field(alias='boxes')
    detection_scores: List[float] = Field(alias='detection_scores')
    masks: List[List[int]] = Field(alias="masks")

    _validate_labels = validator('labels', allow_reuse=True)(labels_validator)
    _validate_scores = validator('detection_scores', allow_reuse=True)(detection_scores_validator)
    _validate_boxes = validator('boxes', allow_reuse=True)(boxes_validator)
    _validate_masks = validator('masks', allow_reuse=True)(masks_validator)

    @root_validator
    def check_sizes(cls, values):
        labels, detection_scores, boxes, masks = values.get('labels'), values.get('detection_scores'), values.get('boxes'), values.get('masks')
        
        if labels is None or detection_scores is None or boxes is None or masks is None or len(labels) != len(detection_scores) or len(boxes) != len(labels) or len(masks) != len(labels):
            raise ValueError('incoherent lists')

        return values
