# DriverGuard architecture

```text
Camera / demo input
       ↓
Frame preprocessing → MediaPipe Face Mesh (local)
       ↓
EAR / MAR / head pose / face status
       ↓
Temporal trackers: closure duration, blink rate, yawn duration, PERCLOS, attention duration
       ↓
Explainable risk engine → alert state → dashboard, sound, SQLite event log
```

`FaceDetector` selects the largest face when more than one is present and marks that condition for the UI. `EyeTracker` measures each eye independently; its continuous closure clock is reset only after reopening. `RiskEngine` has a rolling time window for PERCLOS, configurable weights, and a deliberately conservative immediate override for sustained closure.

## Data flow and limits

No frames leave the device. The application retains scalar metrics in a bounded dashboard history and stores event metadata locally in SQLite. It does not store video. Face landmarks can be unreliable in low light, with occlusion, extreme rotation, or glasses; a lost face is reported rather than interpreted as closed eyes.

## Formulas

For six ordered eye points, `EAR = (||p2-p6|| + ||p3-p5||) / (2||p1-p4||)`. Lower values can indicate a closed eye. MAR is the mean vertical mouth opening divided by mouth width. `PERCLOS = closed samples / observed samples × 100` within a rolling window. These are project-level heuristics, not medical or automotive safety standards.

