"""Central, deliberately conservative project-level thresholds."""
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Settings:
    camera_index: int = 0
    width: int = 640
    height: int = 480
    mirror: bool = True
    show_mesh: bool = False
    eye_threshold: float = 0.21
    eye_alert_seconds: float = 2.0
    perclos_window_seconds: float = 60.0
    perclos_warning: float = 0.20
    perclos_critical: float = 0.35
    yawn_threshold: float = 0.55
    yawn_seconds: float = 1.2
    distraction_yaw_degrees: float = 28.0
    distraction_seconds: float = 4.0
    head_down_pitch_degrees: float = 18.0
    alert_volume: float = 0.8
    weights: Dict[str, float] = field(default_factory=lambda: {
        "closure": .30, "perclos": .25, "yawn": .15, "head": .15,
        "blink": .05, "attention": .10,
    })

