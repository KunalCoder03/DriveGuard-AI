"""AI DriverGuard Streamlit dashboard. Run: streamlit run app.py"""
from __future__ import annotations
import time
from pathlib import Path
import cv2
import pandas as pd
import plotly.express as px
import streamlit as st
from config import Settings
from src.camera import Camera
from src.face_detector import FaceDetector
from src.eye_tracker import EyeTracker
from src.mouth_tracker import MouthTracker
from src.head_pose import HeadPoseEstimator
from src.attention_detector import AttentionDetector
from src.risk_engine import RiskEngine, AlertLevel
from src.alert_manager import AlertManager
from src.logger import EventLogger
from src.calibration import Calibration

st.set_page_config(page_title="AI DriverGuard", page_icon="🛡️", layout="wide")
st.markdown("""<style>.stApp{background:#07111f;color:#e6effa}.metric-card{padding:1rem;border-radius:12px;background:#0d2038;border:1px solid #1d4064}.risk{padding:16px;border-radius:12px;text-align:center;font-size:1.45rem;font-weight:700}</style>""", unsafe_allow_html=True)

def defaults():
    if "settings" not in st.session_state:
        st.session_state.settings=Settings(); st.session_state.history=[]; st.session_state.events=[]; st.session_state.monitoring=False; st.session_state.demo="Normal"
    if "logger" not in st.session_state: st.session_state.logger=EventLogger()
defaults()

def reset_camera_session() -> None:
    """Release any old capture and force a clean pipeline on every new Start."""
    if "camera" in st.session_state:
        st.session_state.camera.stop()
    if "alert" in st.session_state:
        st.session_state.alert.stop()
    for key in ("camera", "detector", "eye", "mouth", "pose", "attention", "risk", "alert", "face_missing"):
        st.session_state.pop(key, None)

def level_style(level):
    return {AlertLevel.NORMAL:"#138a58",AlertLevel.WATCH:"#b98b11",AlertLevel.WARNING:"#db7912",AlertLevel.DROWSINESS:"#d3363d",AlertLevel.CRITICAL:"#920d22"}[level]

def setup_pipeline(settings):
    return (FaceDetector(), EyeTracker(settings.eye_threshold), MouthTracker(settings.yawn_threshold,settings.yawn_seconds), HeadPoseEstimator(settings.head_down_pitch_degrees), AttentionDetector(settings.distraction_yaw_degrees,settings.distraction_seconds), RiskEngine(settings), AlertManager(settings.alert_volume))

@st.cache_resource
def create_pipeline(settings_key): return setup_pipeline(Settings())

st.title("AI DRIVERGUARD")
st.caption("Real-Time AI Driver Drowsiness, Fatigue & Attention Monitoring")
st.warning("Educational prototype — not a certified automotive safety device. Never rely on this system as your only safety measure.")

with st.sidebar:
    st.header("Monitoring controls")
    mode=st.radio("Input",["Webcam", "Demo / test mode"], index=1 if st.session_state.demo != "Normal" else 0)
    st.session_state.settings.camera_index=st.number_input("Camera index",0,10,st.session_state.settings.camera_index)
    st.session_state.settings.mirror=st.toggle("Mirror preview",st.session_state.settings.mirror)
    st.session_state.settings.show_mesh=st.toggle("Show landmark points",st.session_state.settings.show_mesh)
    st.session_state.settings.eye_threshold=st.slider("Eye-closure EAR threshold",.10,.40,st.session_state.settings.eye_threshold,.01)
    st.session_state.settings.eye_alert_seconds=st.slider("Drowsiness duration (s)",.5,5.,st.session_state.settings.eye_alert_seconds,.1)
    st.session_state.settings.distraction_seconds=st.slider("Distraction duration (s)",1.,10.,st.session_state.settings.distraction_seconds,.5)
    st.session_state.settings.alert_volume=st.slider("Alert volume",0.,1.,st.session_state.settings.alert_volume,.1)
    if mode == "Demo / test mode": st.session_state.demo=st.selectbox("Scenario",["Normal","Eyes closed","Yawn","Head down","Looking away","Recovery"])
    else: st.session_state.demo="Normal"
    if st.button("Reset defaults"): st.session_state.settings=Settings(); st.rerun()
    if st.button("Clear logs"): st.session_state.logger.clear(); st.success("Logs cleared")

start, stop, calibrate = st.columns(3)
if start.button("▶ Start monitoring",use_container_width=True):
    reset_camera_session()
    st.session_state.monitoring=True
if stop.button("■ Stop monitoring",use_container_width=True):
    st.session_state.monitoring=False
    if "alert" in st.session_state: st.session_state.alert.stop()
    if "camera" in st.session_state: st.session_state.camera.stop()
if calibrate.button("Save current calibration",use_container_width=True):
    ears=[x["ear"] for x in st.session_state.history[-100:] if x.get("ear",0)>0]
    result=Calibration().save_eye_baseline(ears); st.info(f"Saved personal EAR threshold: {result:.3f}" if result else "Need a few frames with a detected face first.")

feed_col, status_col=st.columns([1.45,1])
frame_slot=feed_col.empty(); status_slot=status_col.empty()
metrics_slot=st.empty(); chart_slot=st.empty(); events_slot=st.empty()

def render(eye,mouth,pose,attention,risk,fps,face=True):
    status_slot.markdown(f'<div class="risk" style="background:{level_style(risk.level)}">{risk.level.name} · {risk.score:.0f}/100<br><small>{risk.reason}</small></div>',unsafe_allow_html=True)
    a,b,c,d,e=metrics_slot.columns(5)
    a.metric("Driver", "DETECTED" if face else "NOT DETECTED"); b.metric("Average EAR",f"{eye.ear:.3f}"); c.metric("PERCLOS",f"{risk.perclos*100:.1f}%"); d.metric("Yawns",mouth.yawn_count); e.metric("Head",pose.state)
    if st.session_state.history:
        df=pd.DataFrame(st.session_state.history[-180:]); chart_slot.plotly_chart(px.line(df,x="time",y=["score","ear","perclos"],template="plotly_dark",title="Live safety signals"),use_container_width=True)
    rows=st.session_state.logger.recent(12)
    if rows: events_slot.dataframe(pd.DataFrame(rows,columns=["Time","Event","Severity","Description"]),hide_index=True,use_container_width=True)

if st.session_state.monitoring:
    # A finite refresh batch keeps Streamlit responsive and lets the Stop control take effect on the next run.
    s=st.session_state.settings
    if "detector" not in st.session_state:
        st.session_state.detector,st.session_state.eye,st.session_state.mouth,st.session_state.pose,st.session_state.attention,st.session_state.risk,st.session_state.alert=setup_pipeline(s)
        st.session_state.camera=Camera(s); ok,message=st.session_state.camera.start()
        if not ok and mode=="Webcam":
            st.error(message)
            st.session_state.monitoring=False
            st.stop()
    detector,eye_t,mouth_t,pose_t,att_t,engine,alert=(st.session_state.detector,st.session_state.eye,st.session_state.mouth,st.session_state.pose,st.session_state.attention,st.session_state.risk,st.session_state.alert)
    frame=st.session_state.camera.read() if mode=="Webcam" else None
    ts=time.monotonic(); eye=eye_t.update([],ts) if False else None
    if frame is not None:
        found=detector.process(frame)
        if found:
            st.session_state.face_missing=False
            eye=eye_t.update(found.landmarks,ts); mouth=mouth_t.update(found.landmarks,ts); pose=pose_t.update(found.landmarks,frame.shape); attention=att_t.update(pose.yaw,pose.pitch,ts)
            if s.show_mesh:
                for x,y,_ in found.landmarks[::8]: cv2.circle(frame,(int(x),int(y)),1,(80,220,160),-1)
            frame_slot.image(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB),channels="RGB",use_container_width=True)
        else:
            # The camera image stays visible even while tracking fails. A missing face
            # never becomes an eye-closure alert and monitoring keeps trying.
            if not st.session_state.get("face_missing", False):
                st.session_state.logger.log("FACE_LOST","INFO","Driver not detected")
                st.session_state.face_missing=True
            cv2.putText(frame,"DRIVER NOT DETECTED - ADJUST LIGHT / CAMERA",(18,36),cv2.FONT_HERSHEY_SIMPLEX,.62,(30,40,255),2)
            frame_slot.image(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB),channels="RGB",use_container_width=True)
            status_slot.warning("Camera is live, but face landmarks are not available yet. Improve lighting and face the camera.")
    else:
        # Clearly labelled deterministic demo injection, never presented as computer-vision output.
        scenario=st.session_state.demo; e=.31; mar=.25; yaw=pitch=0
        if scenario=="Eyes closed": e=.12
        if scenario=="Yawn": mar=.75
        if scenario=="Head down": pitch=25
        if scenario=="Looking away": yaw=38
        class L: pass
        lm=[(0.,0.,0.)]*400
        # Demo metrics bypass geometric landmarks but use the exact same temporal/risk pipeline.
        eye=L(); eye.ear=e; eye.left_ear=e; eye.right_ear=e; eye.closed=e<s.eye_threshold; eye.closure_seconds=(ts-getattr(st.session_state,"demo_closed",ts)) if eye.closed else 0; eye.blink_count=0; eye.blink_rate=0; eye.average_blink_seconds=0
        if eye.closed and not hasattr(st.session_state,"demo_closed"): st.session_state.demo_closed=ts
        if not eye.closed: st.session_state.pop("demo_closed",None)
        mouth=L(); mouth.mar=mar; mouth.open=mar>s.yawn_threshold; mouth.yawn_seconds=2 if mouth.open else 0; mouth.yawn_count=1 if mouth.open else 0
        pose=L(); pose.pitch=pitch; pose.yaw=yaw; pose.roll=0; pose.state="HEAD DOWN" if pitch>18 else ("LOOKING AWAY" if abs(yaw)>28 else "NORMAL")
        attention=att_t.update(yaw,pitch,ts); frame_slot.info(f"DEMO MODE — {scenario}. Do not use while driving.")
    if eye is not None:
        risk=engine.update(eye=eye,mouth=mouth,pose=pose,attention=attention,timestamp=ts); alert.set_level(risk.level)
        st.session_state.history.append({"time":time.strftime("%H:%M:%S"),"score":risk.score,"ear":eye.ear,"perclos":risk.perclos*100})
        if risk.level>=AlertLevel.DROWSINESS: st.session_state.logger.log("DROWSINESS","CRITICAL",risk.reason,{"score":risk.score})
        render(eye,mouth,pose,attention,risk,0,True)
    # Refresh whether or not a face was found, so a temporary tracking loss does not
    # freeze the preview or require opening the camera again.
    time.sleep(.10); st.rerun()
else:
    st.info("Ready. All camera processing is local; frames are not uploaded or recorded by default.")
    st.subheader("Session / event log")
    rows=st.session_state.logger.recent(20)
    if rows: st.dataframe(pd.DataFrame(rows,columns=["Time","Event","Severity","Description"]),hide_index=True,use_container_width=True)
    if st.button("Export CSV"): st.success(f"Exported {st.session_state.logger.export_csv()}")

