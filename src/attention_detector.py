from __future__ import annotations
from dataclasses import dataclass
@dataclass
class Attention: direction: str = "FORWARD"; distracted: bool = False; away_seconds: float = 0.
class AttentionDetector:
    def __init__(self, yaw_threshold: float, duration: float): self.yaw_threshold,self.duration,self.away_since=yaw_threshold,duration,None
    def update(self, yaw: float, pitch: float, timestamp: float) -> Attention:
        direction = "LEFT" if yaw < -self.yaw_threshold else "RIGHT" if yaw > self.yaw_threshold else "DOWN" if pitch > 18 else "FORWARD"
        if direction != "FORWARD" and self.away_since is None: self.away_since=timestamp
        if direction == "FORWARD": self.away_since=None
        seconds=timestamp-self.away_since if self.away_since else 0
        return Attention(direction, seconds >= self.duration, seconds)

