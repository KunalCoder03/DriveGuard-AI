from __future__ import annotations
import json
from pathlib import Path
class Calibration:
    def __init__(self,path="calibration.json"): self.path=Path(path)
    def save_eye_baseline(self, ears):
        if not ears: return None
        baseline=sum(ears)/len(ears); threshold=baseline*.72
        self.path.write_text(json.dumps({"open_eye_ear":baseline,"eye_threshold":threshold},indent=2)); return threshold
    def load(self):
        try: return json.loads(self.path.read_text())
        except (OSError,json.JSONDecodeError): return {}

