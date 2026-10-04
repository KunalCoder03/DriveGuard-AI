from src.utils import aspect_ratio
from src.eye_tracker import EyeTracker
from src.mouth_tracker import MouthTracker

def test_aspect_ratio_square_eye():
    points=[(0,0),(1,1),(3,1),(4,0),(3,-1),(1,-1)]
    assert round(aspect_ratio(points),3) == .5

def test_eye_closure_timer_and_blink():
    tracker=EyeTracker(.2); lm=[(0.,0.,0.)]*400
    # Patch canonical points into a deliberately low-EAR contour
    for ids in ([33,160,158,133,153,144],[362,385,387,263,373,380]):
        for i,p in zip(ids,[(0,0,0),(1,.1,0),(3,.1,0),(4,0,0),(3,-.1,0),(1,-.1,0)]): lm[i]=p
    a=tracker.update(lm,10); b=tracker.update(lm,11.2)
    assert a.closed and b.closure_seconds > 1

