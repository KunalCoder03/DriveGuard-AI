from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import os
from pathlib import Path
import cv2

@dataclass
class FaceResult:
    landmarks: list[tuple[float, float, float]]
    confidence: float = 1.0
    multiple_faces: bool = False

class FaceDetector:
    """MediaPipe Face Mesh adapter. Processing remains entirely local."""
    def __init__(self):
        self.ready, self.error, self.mesh = False, None, None
        try:
            # Avoid a locked per-user Matplotlib cache preventing MediaPipe from loading.
            cache = Path(__file__).resolve().parents[1] / ".mplconfig"
            cache.mkdir(exist_ok=True)
            os.environ.setdefault("MPLCONFIGDIR", str(cache))
            import mediapipe as mp
            self.mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=2,
                refine_landmarks=True, min_detection_confidence=.55, min_tracking_confidence=.55)
            self.ready = True
        except Exception as exc: self.error = f"MediaPipe unavailable: {exc}"
    def process(self, frame) -> FaceResult | None:
        if not self.ready: return None
        result = self.mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if not result.multi_face_landmarks: return None
        h, w = frame.shape[:2]; faces = result.multi_face_landmarks
        # Largest face is normally the driver; caller receives a clear multiple-face warning.
        selected = max(faces, key=lambda f: (max(p.x for p in f.landmark)-min(p.x for p in f.landmark))*(max(p.y for p in f.landmark)-min(p.y for p in f.landmark)))
        return FaceResult([(p.x*w, p.y*h, p.z*w) for p in selected.landmark], multiple_faces=len(faces)>1)
    def close(self):
        if self.mesh: self.mesh.close()

