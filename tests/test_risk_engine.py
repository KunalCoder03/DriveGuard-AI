from config import Settings
from src.risk_engine import RiskEngine, AlertLevel
from src.eye_tracker import EyeMetrics
from src.mouth_tracker import MouthMetrics
from src.head_pose import HeadPose
from src.attention_detector import Attention

def test_prolonged_closure_is_high_risk():
    engine=RiskEngine(Settings())
    risk=engine.update(eye=EyeMetrics(ear=.1,closed=True,closure_seconds=3.1),mouth=MouthMetrics(),pose=HeadPose(),attention=Attention(),timestamp=10)
    assert risk.level >= AlertLevel.DROWSINESS
    assert "eyes closed" in risk.reason

def test_normal_is_normal():
    engine=RiskEngine(Settings())
    risk=engine.update(eye=EyeMetrics(ear=.3),mouth=MouthMetrics(),pose=HeadPose(),attention=Attention(),timestamp=10)
    assert risk.level == AlertLevel.NORMAL

