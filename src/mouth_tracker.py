from __future__ import annotations
from dataclasses import dataclass
from .utils import distance
MOUTH_H = (61, 291); MOUTH_V = [(13, 14), (82, 87), (312, 317)]
@dataclass
class MouthMetrics: mar: float = 0.; open: bool = False; yawn_count: int = 0; yawn_seconds: float = 0.
class MouthTracker:
    def __init__(self, threshold: float, duration: float): self.threshold, self.duration, self.opened_since, self.was_open, self.yawns = threshold, duration, None, False, 0
    def update(self, lm, timestamp: float) -> MouthMetrics:
        width = distance(lm[MOUTH_H[0]], lm[MOUTH_H[1]]); mar = sum(distance(lm[a], lm[b]) for a,b in MOUTH_V)/3/width if width else 0
        opened = mar >= self.threshold
        if opened and not self.was_open: self.opened_since = timestamp
        secs = timestamp-self.opened_since if opened and self.opened_since else 0
        if not opened and self.was_open and self.opened_since and timestamp-self.opened_since >= self.duration: self.yawns += 1
        if not opened: self.opened_since = None
        self.was_open = opened
        return MouthMetrics(mar, opened, self.yawns, secs)

