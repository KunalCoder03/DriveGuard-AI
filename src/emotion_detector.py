from dataclasses import dataclass
@dataclass
class FacialState: label: str = "Not enabled"; confidence: float = 0.
class EmotionDetector:
    """Honest optional integration point; no emotion is fabricated from landmarks."""
    def estimate(self, _frame) -> FacialState: return FacialState()

