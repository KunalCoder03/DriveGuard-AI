from __future__ import annotations
import threading, time
from .risk_engine import AlertLevel
class AlertManager:
    """One reusable alarm thread; safely degrades to terminal bell when pygame is absent."""
    def __init__(self, volume=.8): self.volume=volume; self.active=False; self._stop=threading.Event(); self._thread=None
    def set_level(self, level: AlertLevel) -> None:
        should_alarm=level >= AlertLevel.DROWSINESS
        if should_alarm and not self.active: self.active=True; self._stop.clear(); self._thread=threading.Thread(target=self._beep,daemon=True); self._thread.start()
        elif not should_alarm: self.stop()
    def _beep(self):
        while not self._stop.is_set():
            try:
                import winsound; winsound.Beep(1200,350)
            except Exception: print('\a', end='', flush=True)
            self._stop.wait(.35)
    def stop(self): self.active=False; self._stop.set()

