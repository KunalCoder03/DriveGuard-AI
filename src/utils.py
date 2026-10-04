from __future__ import annotations
from collections import deque
from math import hypot
from typing import Iterable, Sequence
import time

def now() -> float: return time.monotonic()
def distance(a: Sequence[float], b: Sequence[float]) -> float: return hypot(a[0]-b[0], a[1]-b[1])
def aspect_ratio(points: Sequence[Sequence[float]]) -> float:
    """Six-point EAR/MAR-style ratio: (p2-p6 + p3-p5)/(2*(p1-p4))."""
    if len(points) != 6: return 0.0
    horizontal = 2 * distance(points[0], points[3])
    return (distance(points[1], points[5]) + distance(points[2], points[4])) / horizontal if horizontal else 0.0

class TimedHistory:
    def __init__(self, seconds: float): self.seconds, self.items = seconds, deque()
    def add(self, value: float, timestamp: float | None = None) -> None:
        timestamp = now() if timestamp is None else timestamp; self.items.append((timestamp, value)); self.trim(timestamp)
    def trim(self, timestamp: float | None = None) -> None:
        timestamp = now() if timestamp is None else timestamp
        while self.items and self.items[0][0] < timestamp-self.seconds: self.items.popleft()
    def mean(self) -> float: return sum(v for _, v in self.items) / len(self.items) if self.items else 0.0

