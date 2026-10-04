from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from config import Settings
from .utils import TimedHistory
class AlertLevel(IntEnum): NORMAL=0; WATCH=1; WARNING=2; DROWSINESS=3; CRITICAL=4
@dataclass
class RiskAssessment: score: float; level: AlertLevel; reason: str; perclos: float
class RiskEngine:
    def __init__(self, settings: Settings): self.s=settings; self.closed=TimedHistory(settings.perclos_window_seconds)
    def update(self, *, eye, mouth, pose, attention, timestamp: float) -> RiskAssessment:
        self.closed.add(1. if eye.closed else 0., timestamp); perclos=self.closed.mean()
        c=min(1., eye.closure_seconds/self.s.eye_alert_seconds); p=min(1., perclos/max(self.s.perclos_critical,.01))
        y=min(1., (mouth.yawn_count*.12)+(mouth.yawn_seconds/self.s.yawn_seconds*.3)); head=1. if pose.state=="HEAD DOWN" else 0.; blink=min(1., max(0., eye.blink_rate-25)/25); att=1. if attention.distracted else 0.
        raw=sum(self.s.weights[k]*v for k,v in {"closure":c,"perclos":p,"yawn":y,"head":head,"blink":blink,"attention":att}.items())*100
        reasons=[]
        if eye.closure_seconds >= self.s.eye_alert_seconds: reasons.append(f"eyes closed {eye.closure_seconds:.1f}s")
        if perclos >= self.s.perclos_warning: reasons.append(f"PERCLOS {perclos*100:.0f}%")
        if mouth.yawn_count: reasons.append(f"{mouth.yawn_count} yawn(s)")
        if pose.state=="HEAD DOWN": reasons.append("head down")
        if attention.distracted: reasons.append(f"looking {attention.direction.lower()} {attention.away_seconds:.1f}s")
        # Prolonged closure is an immediate safety override but needs temporal evidence from EyeTracker.
        if eye.closure_seconds >= self.s.eye_alert_seconds*1.5: raw=max(raw, 85)
        level=AlertLevel.CRITICAL if raw>=81 else AlertLevel.DROWSINESS if raw>=61 else AlertLevel.WARNING if raw>=41 else AlertLevel.WATCH if raw>=21 else AlertLevel.NORMAL
        return RiskAssessment(min(100,raw),level, "; ".join(reasons) or "No elevated indicators",perclos)

