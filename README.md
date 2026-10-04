# AI DriverGuard

**Real-Time AI Driver Drowsiness, Fatigue & Attention Monitoring** — a local, educational computer-vision project built with Python, OpenCV, MediaPipe, Streamlit and SQLite.

> Safety disclaimer: this is a college demonstration, not a certified automotive safety device. It estimates risk and must never replace attentive driving, safe stops, or professional systems. It does not diagnose sleep, mood, mental health, or medical conditions.

## What it does

- Local webcam facial-landmark tracking with independent left/right EAR.
- Temporal eye-closure timer, blink statistics, rolling PERCLOS, MAR/yawning, head pose and looking-away duration.
- Explainable 0–100 multi-signal risk score with NORMAL → WATCH → WARNING → DROWSINESS → CRITICAL levels.
- Repeating alert that starts once at drowsiness/critical levels and stops on recovery.
- Configurable settings, personal eye-baseline calibration, camera/mirror controls, mesh debugging, demo scenarios, live signal chart, local SQLite events and CSV export.
- Explicit no-face/multiple-face handling. Facial expression is intentionally an optional integration point: the project does **not** invent emotion predictions.

## Install and run

Requires Python 3.10–3.11 (MediaPipe compatibility is platform/version dependent).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL Streamlit displays. Allow webcam permission, select its index if necessary, click **Start monitoring**, then use **Stop monitoring** to release it. If no camera is available, use **Demo / test mode** to demonstrate the same temporal risk and audio state logic. Demo mode is clearly marked and must not be used while driving.

## Calibration

Sit normally, look at the camera with eyes open, blink naturally, and use **Save current calibration** after roughly 100 frames. It stores an EAR baseline locally in `calibration.json`; you may then apply its suggested threshold in Settings. Individual calibration is important because eye geometry differs between people.

## Architecture

`camera → FaceDetector → eye/mouth/head/attention trackers → RiskEngine → AlertManager + Streamlit + EventLogger`

See [docs/architecture.md](docs/architecture.md) for data flow and formulas. EAR measures relative eyelid opening; MAR measures mouth opening; PERCLOS is the fraction of recent observed time in which eyes were closed. Thresholds are configurable project heuristics, not validated clinical cut-offs.

## Privacy

Processing happens on the computer. The app neither uploads frames nor records raw video by default. It logs only event metadata (time, type, severity, explanation, scalar metrics) to `data/driverguard.db`; **Clear logs** and **Export CSV** are available in the dashboard. Profiles are optional and should remain local.

## Validation and manual checklist

Run core tests:

```powershell
python -m pytest -q
```

Manual checks: normal alert face; a single blink; a 2+ second eye closure; repeated blinking; yawn; head down; looking away; face lost; multiple faces; low light/glasses; recovery after an alert; audio availability. Test while parked — never while driving.

## Limitations and extension points

Landmark tracking can fail with low light, occlusion, camera movement, glasses, or uncommon angles. The app reports uncertainty/no face rather than claiming a driver is asleep. Phone detection and facial-expression estimation are intentionally optional because they need separately evaluated models; no placeholder results are shown as AI predictions. Future work: calibrated gaze, a consented recording workflow, model evaluation against labeled data, and hardware-integrated safety validation.

