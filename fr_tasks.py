import os
from pathlib import Path
import logging

from celery import Celery, Task
from celery import Task
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis


redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', '6379')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"{redis_host = }, {redis_port = }")


celery = Celery('tasks', backend=f"redis://{redis_host}", 
                broker=f"redis://{redis_host}:{redis_port}/0")


class InsightFaceTask(Task):
    def __init__(self):
        # 'CUDAExecutionProvider'
        self._app = FaceAnalysis(providers=['CPUExecutionProvider'], 
                                allowed_modules=['detection', 'recognition'])
        self._app.prepare(ctx_id=0, det_size=(640, 640))

        random_im = np.random.rand(640, 640, 3)
        random_im = (random_im*255.).astype(np.uint8)
        # cv2.imwrite('random.jpg', random_im)

        cv2_img = random_im # = cv2.imread('random.jpg')
        faces = self._app.get(cv2_img)
        logger.info(f"warmup: {faces}")
                

@celery.task(base=InsightFaceTask)
def detect_template(im_path: str):

    cv2_img = cv2.imread(str(im_path))
    faces = detect_template._app.get(cv2_img)

    if len(faces) > 0:
        return {"face": faces[0].kps.tolist()}
    else:
        return {"face": None}
