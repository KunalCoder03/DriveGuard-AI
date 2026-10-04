You are a senior AI/Computer Vision engineer and software architect.

I want you to build a complete, polished, working college-level AI project called:

"AI DriverGuard – Real-Time Driver Drowsiness, Fatigue & Attention Detection System"

The project should be built as a real working application, NOT as a mockup or a collection of disconnected code snippets.

The main goal is:

Use a computer/laptop webcam continuously to monitor a driver's face in real time and detect signs of:

1. Drowsiness
2. Prolonged eye closure
3. Yawning
4. Excessive blinking
5. Head nodding / abnormal head pose
6. Driver distraction / looking away
7. Reduced alertness
8. General facial state / apparent emotion estimation
9. Overall fatigue/risk level

When dangerous drowsiness is detected, the application must immediately produce a loud audible warning and continue the warning until the driver becomes alert again.

IMPORTANT:
This is a college/educational AI project and NOT a certified automotive safety device. Clearly mention this inside the application documentation and README.

==================================================
1. CORE CONCEPT
==================================================

The webcam continuously captures frames.

The AI/computer vision pipeline detects the driver's face and facial landmarks.

The system should continuously analyze:

- Eyes
- Eye aspect ratio (EAR)
- Eye closure duration
- PERCLOS
- Blink frequency
- Mouth opening / Mouth Aspect Ratio (MAR)
- Yawning
- Head pose
- Head tilt
- Head nodding
- Looking direction / gaze where practical
- Face presence
- Facial expression / apparent emotional state
- Overall fatigue indicators

The system combines multiple signals instead of depending on only one metric.

Example:

If the driver's eyes remain closed for more than approximately 2 seconds:

→ DROWSINESS ALERT
→ Start loud warning beep
→ Show RED warning UI
→ Continue warning while eyes remain closed
→ Stop/reduce alert when eyes are detected open again and the driver appears attentive.

The 2-second threshold must be configurable from the UI/settings.

Do NOT simply detect "eyes closed in one frame".

The system must use temporal information across multiple frames.

==================================================
2. TECHNOLOGY STACK
==================================================

Preferred stack:

Python 3.x

Computer Vision:
- OpenCV

Face/Landmark Detection:
- MediaPipe Face Mesh / Face Landmarker or another reliable lightweight facial landmark solution

Optional object detection:
- YOLO if needed for advanced features such as phone detection

Audio:
- pygame or another reliable Python audio library

Dashboard/UI:
- Streamlit

Data:
- SQLite or lightweight local JSON/CSV logging

Visualization:
- Plotly / Matplotlib if useful

Configuration:
- .env only if necessary
- config.py or YAML/JSON configuration for thresholds

Do NOT unnecessarily introduce a huge number of dependencies.

Prioritize:
- Real-time performance
- Stability
- Easy installation
- CPU compatibility
- Clean architecture

The application should ideally work without requiring a powerful NVIDIA GPU.

If a GPU is available, the architecture may optionally take advantage of it.

==================================================
3. PROJECT ARCHITECTURE
==================================================

Create a professional modular project structure similar to:

driverguard/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── config.py
│
├── src/
│   ├── __init__.py
│   ├── camera.py
│   ├── face_detector.py
│   ├── eye_tracker.py
│   ├── mouth_tracker.py
│   ├── head_pose.py
│   ├── fatigue_detector.py
│   ├── attention_detector.py
│   ├── emotion_detector.py
│   ├── risk_engine.py
│   ├── alert_manager.py
│   ├── calibration.py
│   ├── logger.py
│   └── utils.py
│
├── models/
│
├── assets/
│   ├── sounds/
│   └── icons/
│
├── data/
│
├── tests/
│   ├── test_eye_detection.py
│   ├── test_fatigue.py
│   └── test_risk_engine.py
│
└── docs/
    └── architecture.md

You may modify this structure if there is a technically better architecture, but keep the project modular and understandable for a college student.

Do NOT put the entire project into one giant Python file.

==================================================
4. CAMERA MODULE
==================================================

Implement webcam capture using OpenCV.

Requirements:

- Detect available camera
- Allow camera selection if multiple cameras exist
- Configurable resolution
- Real-time FPS calculation
- Graceful handling when camera is unavailable
- Graceful handling when camera permissions are denied
- Ability to start/stop monitoring
- Avoid crashing when frames are temporarily unavailable

Display:

- Live webcam feed
- FPS
- Camera status

Allow the user to mirror the camera preview if desired.

==================================================
5. FACE DETECTION
==================================================

Detect the driver's face in real time.

For every frame:

- Detect face
- Extract facial landmarks
- Draw optional face bounding box
- Draw optional landmark mesh
- Track face consistently between frames

The application should support:

FACE DETECTED

and

NO FACE DETECTED

states.

If no face is detected for a short period:

Display:

"DRIVER NOT DETECTED"

Do NOT immediately trigger a drowsiness alarm simply because the face disappears.

Log this as a separate event.

==================================================
6. EYE DETECTION
==================================================

Implement Eye Aspect Ratio (EAR).

Calculate EAR separately for:

- Left eye
- Right eye

Then calculate:

average_EAR

Use a configurable eye closure threshold.

For example:

EAR < threshold = potentially closed

But do NOT hard-code assumptions without calibration.

Create a calibration stage.

During calibration:

Ask the user to:

1. Look normally with eyes open
2. Blink naturally
3. Keep eyes closed briefly
4. Look straight at camera

Estimate a baseline.

Allow thresholds to be configured.

==================================================
7. EYE CLOSURE TIMER
==================================================

This is one of the MOST IMPORTANT features.

Track the continuous duration for which the driver's eyes remain closed.

Example:

0.2 sec → normal
0.8 sec → warning state
1.5 sec → fatigue suspicion
2.0+ sec → DROWSINESS ALERT

The exact values must be configurable.

IMPORTANT:

Do not trigger the alert because of a single frame.

Use temporal smoothing.

If eyes reopen:

Reset the continuous eye closure timer.

However, maintain historical fatigue statistics.

==================================================
8. DROWSINESS ALERT
==================================================

When prolonged eye closure is detected:

Display a large RED banner:

"DROWSINESS DETECTED – WAKE UP!"

or:

"⚠ DRIVER DROWSINESS ALERT"

Play a loud repeating beep/alarm.

The alarm should continue while dangerous drowsiness persists.

The alarm should stop when:

- Eyes reopen
- Face becomes stable
- Driver is no longer classified as severely drowsy

Do not rely only on one frame.

Implement an alert state machine such as:

NORMAL
↓
WARNING
↓
DROWSY
↓
CRITICAL
↓
RECOVERY
↓
NORMAL

Prevent alert spam.

Do not start a new audio process on every frame.

==================================================
9. PERCLOS
==================================================

Implement PERCLOS.

PERCLOS = percentage of time that the driver's eyes are considered closed during a selected time window.

For example:

Analyze the last 30–60 seconds.

Calculate:

closed_time / total_observation_time

Display:

PERCLOS: XX%

Use a rolling window.

Classify risk based on configurable thresholds.

Example:

Low PERCLOS
→ Normal

Moderate PERCLOS
→ Warning

High PERCLOS
→ Critical fatigue

Do not claim that the thresholds are medically or scientifically certified.

Clearly state they are project-level thresholds.

==================================================
10. BLINK DETECTION
==================================================

Detect:

- Normal blink
- Blink frequency
- Abnormally long blink
- Excessive blinking

Display:

Blink Count
Blink Rate
Average Blink Duration

Do not count one blink as drowsiness.

Combine blinking behavior with other indicators.

==================================================
11. YAWNING DETECTION
==================================================

Calculate Mouth Aspect Ratio (MAR).

Detect prolonged mouth opening.

Possible states:

MOUTH CLOSED
MOUTH OPEN
YAWNING SUSPECTED
YAWNING DETECTED

If the mouth remains open beyond a configurable duration:

Count as a yawn.

Display:

Yawns: X

Keep a rolling count.

Repeated yawning should contribute to the fatigue/risk score.

==================================================
12. HEAD POSE DETECTION
==================================================

Estimate head pose:

- Pitch
- Yaw
- Roll

Display values in the dashboard.

Detect:

- Head nodding
- Head tilted down
- Looking far left
- Looking far right
- Abnormal head angle

If the driver's head repeatedly drops forward/down for a significant duration:

Increase fatigue score.

Example:

HEAD DOWN
↓
Potential nodding
↓
Fatigue warning

Do not classify a normal temporary head movement as dangerous.

Use temporal smoothing.

==================================================
13. DRIVER ATTENTION / DISTRACTION
==================================================

Add an attention monitoring module.

Estimate whether the driver is:

- Looking forward
- Looking left
- Looking right
- Looking down
- Possibly distracted

If the driver's face/head is turned away from the forward direction for a configurable duration:

Display:

"ATTENTION WARNING"

This should be separate from the drowsiness alarm.

Example:

Eyes open + head turned right for 5 seconds
→ distraction warning

Eyes closed for 2+ seconds
→ drowsiness warning

==================================================
14. FACIAL STATE / EMOTION ESTIMATION
==================================================

I originally wanted a "mood tracker".

Implement this carefully.

DO NOT claim that the AI can know the driver's true internal mood.

Instead call the feature:

"Facial State / Emotion Estimation"

Possible categories:

- Neutral
- Happy
- Sad
- Angry
- Surprised
- Tired-looking
- Stressed-looking
- Drowsy-looking

If a reliable emotion model is not available, create this module as an optional component.

Do not fake emotion predictions.

The UI should clearly label this as:

"Estimated facial expression"

not:

"Actual mood"

The system should never make medical or psychological diagnoses.

==================================================
15. FATIGUE SCORE
==================================================

Create a dynamic fatigue score from 0–100.

Example inputs:

Eye closure duration
PERCLOS
Blink behavior
Yawning
Head nodding
Head pose
Attention/distraction
Face stability

Example conceptual weighting:

Eye closure: 30%
PERCLOS: 25%
Yawning: 15%
Head nodding: 15%
Blink behavior: 5%
Attention: 10%

These weights should be configurable.

Do NOT blindly use these exact weights if testing shows a better approach.

Display:

FATIGUE SCORE: 0–100

Risk categories:

0–20:
SAFE / ALERT

21–40:
LOW FATIGUE

41–60:
MODERATE FATIGUE

61–80:
HIGH FATIGUE

81–100:
CRITICAL

Use clear visual indicators.

==================================================
16. RISK ENGINE
==================================================

Create a dedicated risk engine.

It should combine multiple signals.

Example:

EAR
PERCLOS
MAR
Yawning
Head Pose
Eye Closure Duration
Blink Rate
Attention
Face Detection

Output:

risk_score
risk_level
dominant_reason

Example:

Risk Score: 87
Risk Level: CRITICAL
Reason:
"Prolonged eye closure + high PERCLOS + head nodding"

This is much better than simply:

"Eyes closed"

==================================================
17. ALERT LEVELS
==================================================

Implement multiple alert levels.

LEVEL 0:
NORMAL

LEVEL 1:
WATCH

LEVEL 2:
WARNING

LEVEL 3:
DROWSINESS

LEVEL 4:
CRITICAL

Example:

NORMAL:
Green UI

WATCH:
Yellow UI

WARNING:
Orange UI

DROWSINESS:
Red UI + beep

CRITICAL:
Red flashing UI + stronger repeating alarm

Avoid excessive flashing that could itself become annoying.

Make the alert system configurable.

==================================================
18. AUDIO ALERT MANAGER
==================================================

Create a proper AlertManager.

Requirements:

- Start alarm
- Stop alarm
- Prevent duplicate audio processes
- Adjustable volume
- Different sounds for different alert levels
- Repeat alarm while dangerous state continues
- Automatically stop when recovery is detected

Possible sounds:

warning.wav
drowsiness.wav
critical.wav

If sound files are unavailable, provide a fallback using a simple generated beep.

==================================================
19. DRIVER CALIBRATION
==================================================

Create a calibration screen.

Before monitoring:

Show:

"Calibration"

Ask driver to sit normally.

Steps:

STEP 1:
Look directly at camera with eyes open.

STEP 2:
Blink normally.

STEP 3:
Close eyes briefly.

STEP 4:
Look straight ahead.

STEP 5:
Turn head slightly left/right.

Use these observations to estimate personal baseline.

Store calibration values locally.

Allow:

"Recalibrate"

button.

This is important because different people have different eye shapes and EAR values.

==================================================
20. REAL-TIME DASHBOARD
==================================================

Create a polished Streamlit dashboard.

The dashboard should look like a modern AI safety monitoring system.

Layout:

--------------------------------------------------
AI DRIVERGUARD
Real-Time Driver Safety Monitoring
--------------------------------------------------

CAMERA FEED

[Live video]

STATUS:
● DRIVER DETECTED

FATIGUE SCORE:
34 / 100

RISK:
LOW

--------------------------------------------------

EYE ANALYTICS

Left EAR: 0.31
Right EAR: 0.30
Average EAR: 0.305

Eye Status:
OPEN

Eye Closure:
0.4 sec

PERCLOS:
8.2%

Blink Count:
17

Blink Rate:
12/min

--------------------------------------------------

MOUTH ANALYTICS

MAR:
0.21

Mouth:
CLOSED

Yawns:
2

--------------------------------------------------

HEAD ANALYTICS

Pitch:
-3°

Yaw:
+2°

Roll:
+1°

Head State:
NORMAL

--------------------------------------------------

ATTENTION

Forward:
YES

Looking Left:
NO

Looking Right:
NO

Looking Down:
NO

--------------------------------------------------

FACIAL STATE

Estimated Expression:
NEUTRAL

Confidence:
XX%

--------------------------------------------------

RISK ENGINE

Risk Score:
34

Risk Level:
LOW

Primary Factors:
- Normal eye closure
- Low PERCLOS
- No prolonged yawning
--------------------------------------------------

EVENT LOG

19:05:21 — Driver detected
19:06:12 — Normal blink
19:07:34 — Short yawn detected
19:08:42 — Attention warning
19:09:13 — Recovered
--------------------------------------------------

Use clean cards, graphs, status indicators and modern typography.

Do NOT make the UI look like a beginner Python project.

==================================================
21. LIVE GRAPH
==================================================

Display real-time graphs for:

- Fatigue score
- EAR
- PERCLOS
- MAR
- Risk score
- Head pose

Allow the user to select which metric to view.

Use a rolling time window.

Do not store unlimited data in RAM.

==================================================
22. EVENT LOG
==================================================

Log important events.

Example:

timestamp
event_type
severity
description
metrics

Possible events:

FACE_DETECTED
FACE_LOST
BLINK
LONG_EYE_CLOSURE
YAWN
HEAD_NOD
DISTRACTION
DROWSINESS
CRITICAL_DROWSINESS
RECOVERY

Store logs locally.

Provide:

Clear Logs
Export CSV

buttons.

==================================================
23. SESSION REPORT
==================================================

At the end of a monitoring session show:

Session Duration
Average Fatigue Score
Maximum Fatigue Score
Maximum Risk
Total Blinks
Total Yawns
Longest Eye Closure
Total Drowsiness Alerts
Total Attention Warnings
Total Critical Events

Also provide a simple session summary:

"Overall Session Risk: LOW / MODERATE / HIGH"

==================================================
24. DRIVER PROFILE
==================================================

Allow optional local driver profile.

Fields:

Name
Age (optional)
Calibration profile

Do NOT require sensitive personal information.

Profiles should remain local.

Do not upload camera frames or personal information to the cloud.

==================================================
25. PRIVACY
==================================================

Privacy is important.

Default behavior:

Process webcam frames locally.

Do not upload images/videos anywhere.

Do not store raw webcam footage unless the user explicitly enables recording.

Add a visible privacy statement:

"All computer vision processing is performed locally. Camera frames are not uploaded by default."

If screenshots or recording are implemented, make them optional.

==================================================
26. PERFORMANCE OPTIMIZATION
==================================================

The application must run in real time.

Target:

15–30 FPS depending on hardware.

Use:

- Frame skipping if necessary
- Efficient landmark processing
- Temporal smoothing
- Limited graph history
- Avoid expensive processing every frame
- Separate high-frequency and low-frequency calculations

Example:

Face landmarks:
every frame

Emotion estimation:
every 5–10 frames

Heavy object detection:
every 5–10 frames

Charts:
update periodically

Do not unnecessarily run expensive models on every frame.

==================================================
27. OPTIONAL PHONE DETECTION
==================================================

If feasible, add an optional module using YOLO or another lightweight object detector.

Detect:

cell phone

If a phone is detected near the driver's visible region for a sustained period:

Display:

"PHONE DISTRACTION DETECTED"

Add it to risk score.

IMPORTANT:

Do not make the entire application dependent on YOLO.

The core project must work without phone detection.

If the required model cannot be downloaded automatically, provide a clean optional integration and instructions.

==================================================
28. LOW LIGHT / GLASSES ROBUSTNESS
==================================================

Handle common problems:

- Low light
- Glasses
- Slight head rotation
- Different face shapes
- Different skin tones
- Temporary face occlusion
- Camera angle changes

Do not claim perfect accuracy.

Show:

"Detection confidence"

where appropriate.

If detection becomes unreliable:

"Tracking confidence low"

instead of making a dangerous assumption.

==================================================
29. FALSE POSITIVE REDUCTION
==================================================

This is extremely important.

The system must NOT trigger drowsiness because:

- User blinked
- User looked down for a moment
- User scratched their face
- User moved their head
- Camera temporarily lost face
- One frame incorrectly detected closed eyes

Use:

Temporal smoothing
Debouncing
Moving averages
State machines
Minimum duration thresholds
Multi-signal confirmation

A dangerous system with constant false alarms is useless.

Prioritize stability.

==================================================
30. SAFETY LOGIC
==================================================

Important:

Never automatically claim:

"Driver is definitely asleep."

Instead use:

"High drowsiness risk detected."

The system should communicate uncertainty.

Example:

BAD:
"Driver is asleep."

GOOD:
"High drowsiness risk – prolonged eye closure detected."

==================================================
31. SETTINGS PANEL
==================================================

Create a Settings section.

Allow configuration of:

Eye closure threshold
Eye closure alert duration
PERCLOS window
PERCLOS warning threshold
Yawning duration
Head-down threshold
Distraction duration
Risk weights
Alert volume
Camera index
Camera resolution
Mirror camera
Show face mesh
Show landmarks
Enable emotion estimation
Enable phone detection
Enable event logging

Provide:

"Reset to Defaults"

==================================================
32. DEBUG MODE
==================================================

Add a debug mode.

When enabled show:

EAR
MAR
PERCLOS
FPS
Head pose
Eye closure timer
Risk score
Detection confidence
Current state
Alert state

This is useful for development and college demonstration.

==================================================
33. DEMO MODE
==================================================

Create a Demo/Test Mode.

This allows the developer to test:

Eyes closed
Yawning
Head down
Distraction
Recovery

without needing actual driving.

The system should clearly label:

"DEMO MODE – DO NOT USE WHILE DRIVING"

Never encourage testing this while actually driving.

==================================================
34. ERROR HANDLING
==================================================

The application should gracefully handle:

- Missing dependencies
- Missing model files
- Camera unavailable
- Camera permission denied
- No face
- Multiple faces
- Audio failure
- Invalid configuration
- Corrupted log files

Never allow a simple webcam or audio error to crash the entire application.

Show useful error messages.

==================================================
35. MULTIPLE FACE HANDLING
==================================================

This is important.

Normally there should be one driver.

If multiple faces are detected:

Display:

"Multiple faces detected"

Do not blindly use the wrong person's face.

Prefer the largest/central face but clearly warn the user.

==================================================
36. DOCUMENTATION
==================================================

Create a professional README.md.

Include:

Project title
Project overview
Problem statement
Motivation
Features
AI/Computer Vision concepts
Architecture
Technology stack
Algorithms
EAR explanation
MAR explanation
PERCLOS explanation
Head pose explanation
Risk engine explanation
Installation
Requirements
How to run
Calibration
Dashboard explanation
Screenshots section
Testing
Limitations
Privacy
Future improvements
Disclaimer

Explain technical concepts in simple language because this is a college project.

==================================================
37. COLLEGE PROJECT DOCUMENTATION
==================================================

Also create:

docs/architecture.md

Include:

System architecture

Camera
↓
Frame preprocessing
↓
Face detection
↓
Facial landmarks
↓
Feature extraction
↓
Temporal analysis
↓
Risk engine
↓
Alert manager
↓
Dashboard + Event Logger

Also include a detailed data flow.

==================================================
38. ALGORITHM EXPLANATION
==================================================

Document the formulas.

EAR:

EAR = (||p2-p6|| + ||p3-p5||) / (2||p1-p4||)

Explain what it means.

MAR:

MAR = vertical mouth distances / horizontal mouth distance

Explain.

PERCLOS:

PERCLOS = closed-eye duration / total observation duration × 100

Explain.

Risk score:

Explain how individual signals contribute.

Do not claim the formulas are medical diagnostic standards.

==================================================
39. TESTING
==================================================

Create automated tests for core mathematical logic.

Test:

EAR calculation
MAR calculation
PERCLOS calculation
Risk score
Alert state transitions
Eye closure timer
Yawning timer

Also create a manual test checklist:

1. Normal alert driver
2. Blink
3. Long eye closure
4. Repeated blinking
5. Yawn
6. Head nod
7. Looking away
8. Face lost
9. Multiple faces
10. Low light
11. Glasses
12. Recovery after alert

==================================================
40. PROJECT QUALITY
==================================================

Write clean Python.

Use:

- Type hints
- Docstrings
- Meaningful variable names
- Classes where appropriate
- Modular functions
- Logging
- Exception handling

Avoid:

- Giant functions
- Duplicate code
- Hardcoded paths
- Magic numbers
- Global state everywhere
- Fake AI predictions
- Placeholder functionality presented as complete

==================================================
41. IMPORTANT DEVELOPMENT RULE
==================================================

Before writing the implementation:

1. Inspect the current workspace.
2. Determine whether a Python environment already exists.
3. Inspect existing files.
4. Reuse useful existing components if present.
5. Do not destroy unrelated files.
6. Create the project incrementally.

Then implement the project.

After implementation:

1. Install required dependencies if possible.
2. Run syntax checks.
3. Run automated tests.
4. Fix errors.
5. Run the application.
6. Verify webcam initialization.
7. Verify dashboard.
8. Verify alert state logic.
9. Verify audio logic.
10. Verify logging.
11. Verify export functionality.

If webcam access cannot be tested automatically, create a test/mock mode and explain exactly what remains to be manually tested.

==================================================
42. DO NOT STOP AT CODE GENERATION
==================================================

I want you to actually build the project.

Do NOT simply tell me:

"Here is how you can implement it."

Instead:

- Create the files
- Write the code
- Connect the modules
- Install dependencies when possible
- Test the project
- Fix errors
- Leave the workspace in a runnable state

If something is technically impossible in the current environment, implement the best working fallback instead of abandoning the feature.

==================================================
43. FINAL COMMANDS
==================================================

The final project should ideally run with:

pip install -r requirements.txt

and:

streamlit run app.py

or another clearly documented command.

Make sure README explains the exact command.

==================================================
44. PROJECT BRANDING
==================================================

Project name:

AI DriverGuard

Subtitle:

"Real-Time AI Driver Drowsiness, Fatigue & Attention Monitoring"

Use a professional visual identity.

The dashboard should feel like an actual AI safety monitoring product rather than a basic college assignment.

==================================================
45. FINAL FEATURE CHECKLIST
==================================================

Before considering the project complete, verify:

[ ] Webcam works
[ ] Face detection works
[ ] Face landmarks work
[ ] Eye tracking works
[ ] EAR works
[ ] Eye closure timer works
[ ] 2+ second drowsiness alert works
[ ] Alarm continues during dangerous state
[ ] Alarm stops after recovery
[ ] PERCLOS works
[ ] Blink detection works
[ ] Yawn detection works
[ ] MAR works
[ ] Head pose works
[ ] Head nod detection works
[ ] Attention detection works
[ ] Fatigue score works
[ ] Risk engine works
[ ] Alert state machine works
[ ] Facial state/emotion module works or is cleanly optional
[ ] Calibration works
[ ] Dashboard works
[ ] Live charts work
[ ] Event logging works
[ ] CSV export works
[ ] Session summary works
[ ] Settings work
[ ] Debug mode works
[ ] Demo mode works
[ ] Multiple-face handling works
[ ] No-face handling works
[ ] Error handling works
[ ] README exists
[ ] Architecture documentation exists
[ ] Tests exist and pass
[ ] requirements.txt works
[ ] No fake functionality is presented as working
[ ] Privacy disclaimer exists
[ ] Safety disclaimer exists

==================================================
46. MOST IMPORTANT DESIGN PRINCIPLE
==================================================

Build this as a real Computer Vision + AI project.

The system should not merely say:

"Eyes closed = beep."

It should reason from multiple signals:

Eye closure
+
PERCLOS
+
Blink pattern
+
Yawning
+
Head pose
+
Head nodding
+
Attention
+
Optional facial state
+
Temporal behavior

Then calculate an overall fatigue/risk score.

The result should be explainable.

Example:

"CRITICAL DROWSINESS RISK
Risk Score: 91/100

Reasons:
• Eyes closed for 2.7 seconds
• PERCLOS: 38%
• Head nod detected
• 3 yawns in the last 2 minutes

Action:
⚠ TAKE A BREAK / STOP DRIVING SAFELY"

Do not encourage the driver to continue driving after a critical alert.

==================================================
FINAL OBJECTIVE
==================================================

Build a polished, technically impressive, explainable AI/Computer Vision college project that demonstrates:

Python
Computer Vision
Facial Landmark Detection
Machine Learning/AI concepts
Real-time processing
Signal processing
Risk scoring
State machines
Audio alerts
Data visualization
Dashboard development
Logging
Software architecture
Testing

The project should be impressive enough to demonstrate during a college project presentation and strong enough to showcase on GitHub/LinkedIn.

Start by inspecting the workspace and then build the project.