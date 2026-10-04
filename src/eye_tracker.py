from __future__ import annotations
from dataclasses import dataclass
from collections import deque
from .utils import aspect_ratio

# MediaPipe canonical six-point eye contours.
LEFT = [33, 160, 158, 133, 153, 144]; RIGHT = [362, 385, 387, 263, 373, 380]
@dataclass
class EyeMetrics:
    left_ear: float = 0.; right_ear: float = 0.; ear: float = 0.; closed: bool = False
    closure_seconds: float = 0.; blink_count: int = 0; blink_rate: float = 0.; average_blink_seconds: float = 0.

class EyeTracker:
    def __init__(self, threshold: float):
        self.threshold, self.closed_since, self.was_closed = threshold, None, False
        self.blinks, self.durations = deque(), deque(maxlen=100)
    def update(self, lm, timestamp: float) -> EyeMetrics:
        left, right = aspect_ratio([lm[i] for i in LEFT]), aspect_ratio([lm[i] for i in RIGHT]); ear = (left+right)/2
        closed = ear < self.threshold
        if closed and not self.was_closed: self.closed_since = timestamp
        closure = timestamp-self.closed_since if closed and self.closed_since is not None else 0.
        if not closed and self.was_closed and self.closed_since is not None:
            duration = timestamp-self.closed_since
            if .05 <= duration <= 1.0: self.blinks.append(timestamp); self.durations.append(duration)
            self.closed_since = None
        self.was_closed = closed
        while self.blinks and self.blinks[0] < timestamp-60: self.blinks.popleft()
        return EyeMetrics(left, right, ear, closed, closure, len(self.blinks), len(self.blinks), sum(self.durations)/len(self.durations) if self.durations else 0.)

