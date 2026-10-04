from __future__ import annotations
from dataclasses import dataclass
import cv2, numpy as np
@dataclass
class HeadPose: pitch: float = 0.; yaw: float = 0.; roll: float = 0.; state: str = "NORMAL"
class HeadPoseEstimator:
    def __init__(self, down: float): self.down = down
    def update(self, lm, shape) -> HeadPose:
        # Standard 2D/3D landmark correspondence, solved per frame then smoothed by risk engine durations.
        h,w = shape[:2]; ids=[1,152,33,263,61,291]; image=np.array([[lm[i][0],lm[i][1]] for i in ids], dtype=np.float64)
        model=np.array([[0,0,0],[0,-63,-12],[-43,32,-26],[43,32,-26],[-28,-28,-24],[28,-28,-24]], dtype=np.float64)
        camera=np.array([[w,0,w/2],[0,w,h/2],[0,0,1]], dtype=np.float64)
        ok, rvec, _ = cv2.solvePnP(model,image,camera,np.zeros((4,1)),flags=cv2.SOLVEPNP_ITERATIVE)
        if not ok: return HeadPose()
        rotation,_=cv2.Rodrigues(rvec); angles=cv2.RQDecomp3x3(rotation)[0]; pitch,yaw,roll=map(float,angles)
        state = "HEAD DOWN" if pitch > self.down else ("LOOKING AWAY" if abs(yaw)>28 else "NORMAL")
        return HeadPose(pitch,yaw,roll,state)

