from __future__ import annotations
import os
import cv2
from config import Settings

class Camera:
    def __init__(self, settings: Settings): self.settings, self.cap = settings, None
    def start(self) -> tuple[bool, str]:
        # Do not pass an explicit backend here. Some partial/minimal OpenCV builds
        # expose VideoCapture but omit CAP_DSHOW/CAP_ANY constants; auto-selection
        # is compatible with those builds and with Windows laptop webcams.
        self.cap = cv2.VideoCapture(self.settings.camera_index)
        if not self.cap.isOpened(): return False, "Camera unavailable or permission denied. Check camera index/permissions."
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.settings.width); self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.settings.height)
        # Warm up auto-exposure and reject a device that opens but yields no frames.
        for _ in range(8):
            ok, _ = self.cap.read()
            if ok: return True, "Camera ready"
        self.stop()
        return False, "Camera opened but returned no frames. Close other camera apps and try another index."
    def read(self):
        if not self.cap: return None
        ok, frame = self.cap.read()
        if not ok: return None
        return cv2.flip(frame, 1) if self.settings.mirror else frame
    def stop(self):
        if self.cap: self.cap.release(); self.cap = None

