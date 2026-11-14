"""ASTRA HEALTH - crew health monitoring prototype.

A local Streamlit application for recording crew health measurements,
filing structured symptom reports and tracking a review (handover) queue.

All alert rules in this module are demonstration rules. They are not
clinically validated and must not be used for diagnosis, treatment or
flight-medical decisions.
"""

from __future__ import annotations

import html
import json
import math
import sqlite3
import uuid
from contextlib import closing
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional, Sequence

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from nasa_osdr import page_nasa_osdr

st.set_page_config(
    page_title="ASTRA HEALTH",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

APP_NAME = "ASTRA HEALTH"
VERSION = "4.2.0"
DB_PATH = Path(__file__).with_name("astra_health.db")

DISCLAIMER = (
    "Demonstration prototype only. Not clinically validated. "
    "Not for diagnosis, treatment, or flight medical decisions."
)

DEFAULT_HEALTH: dict[str, Any] = {
    "heart_rate": 72,
    "systolic_bp": 118,
    "diastolic_bp": 78,
    "temperature": 36.8,
    "glucose": 95,
    "sleep_hours": 7.5,
    "mood": "Good",
    "hydration": "Normal",
    "fatigue": 2,
    "mission_day": 12,
    "microgravity_days": 10,
    "notes": "",
}

DEMO_RULES = {
    "heart_rate_low": 45,
    "heart_rate_high": 110,
    "systolic_low": 85,
    "systolic_high": 150,
    "temperature_low": 35.5,
    "temperature_high": 38.0,
    "glucose_low": 65,
    "glucose_high": 180,
    "sleep_low": 5.0,
    "fatigue_high": 7,
}

# field, low-limit key, high-limit key, finding title, value format, action
RANGE_RULES = (
    (
        "heart_rate", "heart_rate_low", "heart_rate_high",
        "Heart-rate rule activated", "{:g} bpm",
        "Verify the measurement and follow the mission's approved procedure.",
    ),
    (
        "systolic_bp", "systolic_low", "systolic_high",
        "Systolic pressure rule activated", "{:g} mmHg",
        "Verify the measurement and request authorized review.",
    ),
    (
        "temperature", "temperature_low", "temperature_high",
        "Temperature rule activated", "{:.1f} °C",
        "Verify the measurement and follow the approved mission procedure.",
    ),
    (
        "glucose", "glucose_low", "glucose_high",
        "Glucose rule activated", "{:g} mg/dL",
        "Check the entry and refer it to the authorized workflow.",
    ),
)

MOOD_OPTIONS = ["Very good", "Good", "Neutral", "Low", "Very low"]
HYDRATION_OPTIONS = ["Normal", "Needs attention", "Not recorded"]
HANDOVER_STATUSES = ["Pending review", "Reviewed", "Follow-up scheduled", "Closed"]

BODY_REGIONS = [
    "Head", "Neck", "Chest", "Abdomen", "Upper back", "Lower back", "Pelvis",
    "Left shoulder", "Right shoulder", "Left arm", "Right arm",
    "Left hand", "Right hand", "Left thigh", "Right thigh",
    "Left knee", "Right knee", "Left lower leg", "Right lower leg",
    "Left foot", "Right foot",
]

URGENT_FLAGS = [
    "Severe breathing difficulty",
    "Chest pressure or pain",
    "Fainting or loss of consciousness",
    "Sudden confusion",
    "Severe allergic-type reaction",
    "Major injury",
]

SYMPTOM_CATEGORIES = [
    "Pain or discomfort", "Breathing", "Digestive", "Vision",
    "Skin", "Sleep", "Mood / stress", "Other",
]
ONSET_OPTIONS = ["Just now", "Within the last few hours", "Today", "Earlier"]
TREND_OPTIONS = ["Improving", "Staying the same", "Getting worse", "Unsure"]

# Streamlit 1.50 replaced ``use_container_width`` with ``width="stretch"``.
_STREAMLIT_VERSION = tuple(int(p) for p in st.__version__.split(".")[:2] if p.isdigit())
STRETCH: dict[str, Any] = (
    {"width": "stretch"} if _STREAMLIT_VERSION >= (1, 50) else {"use_container_width": True}
)

# --------------------------------------------------------------------------
# Small utilities
# --------------------------------------------------------------------------


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10].upper()}"


def to_float(value: Any) -> Optional[float]:
    """Return ``value`` as a finite float, or ``None`` if it is not numeric."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def clamp_int(value: Any, low: int, high: int, fallback: int) -> int:
    number = to_float(value)
    return fallback if number is None else int(min(max(number, low), high))


def clamp_float(value: Any, low: float, high: float, fallback: float) -> float:
    number = to_float(value)
    return fallback if number is None else float(min(max(number, low), high))


def option_index(options: Sequence[str], value: Any, default: int = 0) -> int:
    return options.index(value) if value in options else default


def esc(value: Any) -> str:
    return html.escape(str(value))


# --------------------------------------------------------------------------
# Persistence (SQLite)
# --------------------------------------------------------------------------


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@st.cache_resource
def init_database() -> bool:
    with closing(_connect()) as conn, conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS health_history (
                id TEXT PRIMARY KEY,
                recorded_at TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS symptom_reports (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS handover_queue (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                status TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """
        )
    return True


def _encode(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, default=str)


def save_health_record(record: dict[str, Any]) -> None:
    with closing(_connect()) as conn, conn:
        conn.execute(
            "INSERT INTO health_history (id, recorded_at, payload) VALUES (?, ?, ?)",
            (record["id"], record["timestamp"], _encode(record)),
        )


def save_report_with_handover(report: dict[str, Any], handover: dict[str, Any]) -> None:
    """Store a symptom report and its handover item in one transaction."""
    with closing(_connect()) as conn, conn:
        conn.execute(
            "INSERT INTO symptom_reports (id, created_at, payload) VALUES (?, ?, ?)",
            (report["id"], report["timestamp"], _encode(report)),
        )
        conn.execute(
            "INSERT INTO handover_queue (id, created_at, status, payload) "
            "VALUES (?, ?, ?, ?)",
            (handover["id"], handover["timestamp"], handover["status"], _encode(handover)),
        )


def update_handover_status(item_id: str, status: str) -> None:
    with closing(_connect()) as conn, conn:
        conn.execute(
            "UPDATE handover_queue SET status = ? WHERE id = ?", (status, item_id)
        )


_LOAD_QUERIES = {
    "health_history": (
        "SELECT id, recorded_at AS timestamp, NULL AS status, payload "
        "FROM health_history ORDER BY recorded_at"
    ),
    "symptom_reports": (
        "SELECT id, created_at AS timestamp, NULL AS status, payload "
        "FROM symptom_reports ORDER BY created_at"
    ),
    "handover_queue": (
        "SELECT id, created_at AS timestamp, status, payload "
        "FROM handover_queue ORDER BY created_at DESC"
    ),
}


def load_table(table: str) -> list[dict[str, Any]]:
    with closing(_connect()) as conn:
        rows = conn.execute(_LOAD_QUERIES[table]).fetchall()

    items: list[dict[str, Any]] = []
    for row in rows:
        try:
            item = json.loads(row["payload"])
        except (TypeError, json.JSONDecodeError):
            item = {}
        if not isinstance(item, dict):
            item = {}
        item["id"] = row["id"]
        item["timestamp"] = row["timestamp"]
        if row["status"] is not None:
            item["status"] = row["status"]
        items.append(item)
    return items


# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------


def initialize_state() -> None:
    state = st.session_state

    if "health_history" not in state:
        state.health_history = load_table("health_history")
    if "symptom_reports" not in state:
        state.symptom_reports = load_table("symptom_reports")
    if "handover_queue" not in state:
        state.handover_queue = load_table("handover_queue")

    if "health" not in state:
        health = DEFAULT_HEALTH.copy()
        if state.health_history:
            latest = state.health_history[-1]
            health.update({k: v for k, v in latest.items() if k in DEFAULT_HEALTH})
        state.health = health

    defaults = {
        "selected_region": "Chest",
        "body_view": "Front",
        "mission_name": "Demo Mission",
        "crew_member": "Crew Member 01",
        "navigation": "Mission Dashboard",
        "_last_map_pick": None,
    }
    for key, value in defaults.items():
        state.setdefault(key, value)


def add_health_record(data: dict[str, Any]) -> None:
    record = {**data, "id": new_id("HLT"), "timestamp": now_iso()}
    save_health_record(record)
    st.session_state.health_history.append(record)
    st.session_state.health = dict(data)


def add_symptom_report(report: dict[str, Any]) -> dict[str, Any]:
    timestamp = now_iso()
    report = {**report, "id": new_id("SYM"), "timestamp": timestamp}
    handover = {
        "id": new_id("HDO"),
        "timestamp": timestamp,
        "symptom_report_id": report["id"],
        "priority": report["priority"],
        "title": f"Symptom report — {report['region']}",
        "summary": report["summary"],
        "region": report["region"],
        "status": HANDOVER_STATUSES[0],
    }
    save_report_with_handover(report, handover)
    st.session_state.symptom_reports.append(report)
    st.session_state.handover_queue.insert(0, handover)
    return report


# --------------------------------------------------------------------------
# Rule engine
# --------------------------------------------------------------------------


def evaluate_health(
    data: dict[str, Any], history: Optional[Sequence[dict[str, Any]]] = None
) -> dict[str, Any]:
    """Apply the demonstration rules to one set of measurements.

    ``history`` must contain earlier records only, excluding ``data`` itself.
    """
    findings: list[dict[str, str]] = []

    def add(level: str, title: str, reason: str, action: str) -> None:
        findings.append(
            {"level": level, "title": title, "reason": reason, "action": action}
        )

    for field, low_key, high_key, title, fmt, action in RANGE_RULES:
        value = to_float(data.get(field))
        if value is None:
            continue
        if value < DEMO_RULES[low_key] or value > DEMO_RULES[high_key]:
            add("Review", title, f"Recorded value: {fmt.format(value)}.", action)

    heart_rate = to_float(data.get("heart_rate"))
    sleep = to_float(data.get("sleep_hours"))
    fatigue = to_float(data.get("fatigue"))

    if sleep is not None and sleep < DEMO_RULES["sleep_low"]:
        add(
            "Monitor",
            "Sleep-duration pattern",
            f"Recorded sleep: {sleep:.1f} hours.",
            "Review the record in the context of the crew's schedule.",
        )

    if fatigue is not None and fatigue >= DEMO_RULES["fatigue_high"]:
        add(
            "Monitor",
            "High fatigue self-rating",
            f"Self-reported fatigue: {fatigue:g}/10.",
            "Consider a scheduled crew-support check-in.",
        )

    if data.get("mood") in ("Low", "Very low"):
        add(
            "Monitor",
            "Mood check-in",
            f"Self-reported mood: {data.get('mood')}.",
            "Offer a private, supportive crew check-in.",
        )

    if data.get("hydration") == "Needs attention":
        add(
            "Monitor",
            "Hydration self-check",
            "The crew member marked hydration as needing attention.",
            "Review the entry in the context of the mission's approved hydration plan.",
        )

    if (
        sleep is not None and heart_rate is not None
        and sleep < DEMO_RULES["sleep_low"] and heart_rate > 90
    ):
        add(
            "Pattern",
            "Combined sleep and heart-rate pattern",
            "Short sleep and a higher recorded heart rate appear together.",
            "Review both records together. This is not a diagnosis.",
        )

    previous = [
        value
        for value in (to_float(item.get("heart_rate")) for item in (history or []))
        if value is not None
    ]
    if heart_rate is not None and len(previous) >= 3:
        recent = previous[-7:]
        baseline = sum(recent) / len(recent)
        difference = heart_rate - baseline
        if abs(difference) >= 20:
            add(
                "Baseline",
                "Change from personal reference",
                f"Current value differs by {difference:+.1f} bpm from the recent "
                f"average ({baseline:.1f}).",
                "Check measurement quality and review the trend.",
            )

    if not findings:
        add(
            "Info",
            "No demonstration rules activated",
            "No configured demonstration rule was triggered.",
            "Continue routine recording. This does not confirm medical wellness.",
        )

    levels = {item["level"] for item in findings}
    if "Review" in levels:
        status = "Review requested"
    elif levels & {"Monitor", "Pattern", "Baseline"}:
        status = "Monitoring note"
    else:
        status = "No demo rule triggered"

    return {
        "status": status,
        "findings": findings,
        "engine": "ASTRA Explainable Engine",
        "clinical_validation": False,
        "timestamp": now_iso(),
    }


def classify_symptom_report(
    intensity: int, trend: str, urgent_flags: Sequence[str]
) -> tuple[str, str]:
    if urgent_flags:
        return (
            "Urgent protocol review",
            "Selected flag(s) require attention under the mission's established "
            "emergency procedure.",
        )
    if intensity >= 8 or trend == "Getting worse":
        return (
            "Priority review requested",
            "High self-rated intensity or worsening trend was reported.",
        )
    return "Routine follow-up", "Report saved for normal authorized review."


# --------------------------------------------------------------------------
# Presentation helpers
# --------------------------------------------------------------------------

STYLES = """
<style>
html, body, .stApp {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                 "Helvetica Neue", Arial, sans-serif;
}
.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(28,111,190,.20), transparent 28%),
        radial-gradient(circle at 95% 12%, rgba(20,184,166,.12), transparent 25%),
        #07111f;
    color: #edf5ff;
}
[data-testid="stSidebar"] { background: #0b192a; border-right: 1px solid #20334b; }
h1, h2, h3 { color: #f3f8ff !important; }
p, label, li { color: #d3dfed; }
.hero {
    padding: 26px; border-radius: 22px; margin-bottom: 20px;
    background: linear-gradient(120deg, rgba(17,83,139,.55), rgba(11,35,57,.88));
    border: 1px solid rgba(98,174,226,.25);
}
.hero-kicker { color: #6ee7d5; font-size: .8rem; font-weight: 800; letter-spacing: 2px; }
.hero-title { color: #fff; font-size: 2rem; font-weight: 800; margin: 7px 0; }
.hero-sub { color: #c4d7e9; }
.metric-card {
    padding: 18px; border-radius: 17px; min-height: 110px;
    background: linear-gradient(145deg, #122941, #0d1d30);
    border: 1px solid #24415e;
}
.metric-label { color: #9eb5ca; font-size: .82rem; }
.metric-value { color: #f7fbff; font-size: 1.8rem; font-weight: 800; margin-top: 5px; }
.metric-note { color: #6ee7d5; font-size: .75rem; }
.section-card {
    background: rgba(15,34,54,.82); border: 1px solid #203c58;
    padding: 18px; border-radius: 17px; margin: 8px 0 14px;
}
.notice {
    border-left: 4px solid #eabf57; background: rgba(130,93,20,.15);
    border-radius: 10px; padding: 14px; color: #f7e7bc; margin: 10px 0 16px;
}
.muted { color: #8fa7bd; font-size: .8rem; }
div.stButton > button {
    border-radius: 11px; border: 1px solid #2d759d; color: #fff; font-weight: 700;
    background: linear-gradient(90deg, #12618b, #0f8c89);
}
div.stButton > button:hover { border-color: #65d9d0; color: #fff; }
[data-testid="stMetric"] {
    background: #10263b; border: 1px solid #25425c; padding: 14px; border-radius: 14px;
}
</style>
"""

FINDING_COLORS = {
    "Review": "#ff7373",
    "Monitor": "#f5c66b",
    "Pattern": "#8bb9ff",
    "Baseline": "#c4a7ff",
    "Info": "#69dbc7",
}


def hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-kicker">ASTRA HEALTH / MISSION INTELLIGENCE</div>
            <div class="hero-title">{esc(title)}</div>
            <div class="hero-sub">{esc(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def notice(text: str) -> None:
    st.markdown(f'<div class="notice">{text}</div>', unsafe_allow_html=True)


def metric_card(label: str, value: str, note: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{esc(label)}</div>
            <div class="metric-value">{esc(value)}</div>
            <div class="metric-note">{esc(note)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_finding(item: dict[str, str]) -> None:
    color = FINDING_COLORS.get(item["level"], "#9eb5ca")
    st.markdown(
        f"""
        <div class="section-card" style="border-left:4px solid {color}">
            <b style="color:{color}">{esc(item['level'])} · {esc(item['title'])}</b>
            <p>{esc(item['reason'])}</p>
            <p style="color:#8ee6d7"><b>Suggested workflow:</b> {esc(item['action'])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------
# Body map
# --------------------------------------------------------------------------

BODY_FILL = "#183c56"
BODY_OUTLINE = "#75b8d5"
GUIDE_COLOR = "#5a91ae"

BODY_POLYGONS = (
    # neck
    [(4.55, 8.65), (5.45, 8.65), (5.38, 8.15), (4.62, 8.15)],
    # torso
    [(4.62, 8.2), (3.85, 8.15), (3.25, 7.75), (3.55, 6.85), (4.15, 6.65),
     (4.25, 5.15), (4.65, 4.85), (5.35, 4.85), (5.75, 5.15), (5.85, 6.65),
     (6.45, 6.85), (6.75, 7.75), (6.15, 8.15), (5.38, 8.2)],
    # arms
    [(3.85, 8.05), (3.25, 7.8), (2.95, 6.85), (2.55, 5.55), (2.35, 4.95),
     (2.75, 4.75), (3.15, 5.3), (3.65, 6.25), (4.15, 7.25)],
    [(6.15, 8.05), (6.75, 7.8), (7.05, 6.85), (7.45, 5.55), (7.65, 4.95),
     (7.25, 4.75), (6.85, 5.3), (6.35, 6.25), (5.85, 7.25)],
    # hands
    [(2.35, 4.95), (2.75, 4.75), (2.95, 4.35), (2.65, 4.05), (2.25, 4.2), (2.15, 4.6)],
    [(7.65, 4.95), (7.25, 4.75), (7.05, 4.35), (7.35, 4.05), (7.75, 4.2), (7.85, 4.6)],
    # pelvis
    [(4.25, 5.2), (5.75, 5.2), (5.9, 4.45), (5.55, 3.95), (4.45, 3.95), (4.1, 4.45)],
    # legs
    [(4.35, 4.2), (4.95, 4.05), (4.8, 2.65), (4.75, 1.3), (4.55, 1.05),
     (3.95, 1.05), (3.85, 1.3), (4.0, 2.65)],
    [(5.05, 4.05), (5.65, 4.2), (6.0, 2.65), (6.15, 1.3), (6.05, 1.05),
     (5.45, 1.05), (5.25, 1.3), (5.2, 2.65)],
    # feet
    [(4.55, 1.15), (3.95, 1.15), (3.7, 0.85), (3.75, 0.65), (4.8, 0.65), (4.85, 0.85)],
    [(5.45, 1.15), (6.05, 1.15), (6.3, 0.85), (6.25, 0.65), (5.2, 0.65), (5.15, 0.85)],
)

FRONT_GUIDES = (
    [(5, 7.7), (5, 5.3)],
    [(4.25, 7.35), (5, 7.15), (5.75, 7.35)],
    [(4.45, 5.0), (5, 4.85), (5.55, 5.0)],
    [(4.45, 4.0), (4.5, 3.3), (4.35, 2.3)],
    [(5.55, 4.0), (5.5, 3.3), (5.65, 2.3)],
)

BACK_GUIDES = (
    [(4.3, 7.65), (5, 7.85), (5.7, 7.65)],
    [(4.25, 6.65), (5, 6.45), (5.75, 6.65)],
    [(4.25, 5.2), (5, 5.0), (5.75, 5.2)],
    [(4.35, 4.0), (4.5, 3.3), (4.35, 2.3)],
    [(5.65, 4.0), (5.5, 3.3), (5.65, 2.3)],
)

_SHARED_MARKERS = {
    "Head": (5, 9.25),
    "Neck": (5, 8.35),
    "Pelvis": (5, 4.55),
    "Left shoulder": (3.95, 7.85),
    "Right shoulder": (6.05, 7.85),
    "Left arm": (3.05, 6.15),
    "Right arm": (6.95, 6.15),
    "Left hand": (2.55, 4.45),
    "Right hand": (7.45, 4.45),
    "Left thigh": (4.35, 3.65),
    "Right thigh": (5.65, 3.65),
    "Left knee": (4.35, 2.65),
    "Right knee": (5.65, 2.65),
    "Left lower leg": (4.3, 1.75),
    "Right lower leg": (5.7, 1.75),
    "Left foot": (4.25, 0.85),
    "Right foot": (5.75, 0.85),
}
FRONT_MARKERS = {"Chest": (5, 7.15), "Abdomen": (5, 5.85), **_SHARED_MARKERS}
BACK_MARKERS = {"Upper back": (5, 7.15), "Lower back": (5, 5.85), **_SHARED_MARKERS}


def _closed_path(points: Sequence[tuple[float, float]]) -> tuple[list[float], list[float]]:
    ring = list(points) + [points[0]]
    return [p[0] for p in ring], [p[1] for p in ring]


def build_body_figure(view: str, selected: str) -> go.Figure:
    fig = go.Figure()

    fig.add_shape(
        type="circle", x0=4.35, x1=5.65, y0=8.65, y1=9.95,
        fillcolor=BODY_FILL, line=dict(color=BODY_OUTLINE, width=2.5),
    )

    for polygon in BODY_POLYGONS:
        xs, ys = _closed_path(polygon)
        fig.add_trace(go.Scatter(
            x=xs, y=ys, mode="lines", fill="toself", fillcolor=BODY_FILL,
            line=dict(color=BODY_OUTLINE, width=2), hoverinfo="skip", showlegend=False,
        ))

    is_front = view == "Front"
    for guide in FRONT_GUIDES if is_front else BACK_GUIDES:
        fig.add_trace(go.Scatter(
            x=[p[0] for p in guide], y=[p[1] for p in guide], mode="lines",
            line=dict(color=GUIDE_COLOR, width=2), hoverinfo="skip", showlegend=False,
        ))

    markers = FRONT_MARKERS if is_front else BACK_MARKERS
    names = list(markers)
    fig.add_trace(go.Scatter(
        x=[markers[n][0] for n in names],
        y=[markers[n][1] for n in names],
        mode="markers",
        customdata=names,
        marker=dict(
            size=[22 if n == selected else 12 for n in names],
            color=["#ffbd59" if n == selected else "#5ee5d5" for n in names],
            line=dict(color="#eafaff", width=1.2),
            opacity=0.95,
        ),
        hovertemplate="<b>%{customdata}</b><extra></extra>",
        showlegend=False,
    ))

    fig.update_layout(
        height=650,
        margin=dict(l=5, r=5, t=15, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        clickmode="event+select",
        xaxis=dict(range=(1.5, 8.5), visible=False, fixedrange=True),
        yaxis=dict(range=(0.3, 10.1), visible=False, fixedrange=True, scaleanchor="x"),
    )
    return fig


def selected_region_from_event(event: Any) -> Optional[str]:
    """Extract the clicked region name from a Plotly selection event."""
    try:
        points = event["selection"]["points"]
    except (KeyError, TypeError):
        return None
    if not points:
        return None
    label = points[0].get("customdata")
    if isinstance(label, (list, tuple)):
        label = label[0] if label else None
    return label if label in BODY_REGIONS else None


# --------------------------------------------------------------------------
# Callbacks
# --------------------------------------------------------------------------


def on_region_picked() -> None:
    st.session_state.selected_region = st.session_state.region_picker


def open_symptom_report() -> None:
    st.session_state.navigation = "Symptom Report"


def on_status_changed(item_id: str) -> None:
    status = st.session_state[f"status_{item_id}"]
    update_handover_status(item_id, status)
    for item in st.session_state.handover_queue:
        if item["id"] == item_id:
            item["status"] = status
            break


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------


def page_dashboard() -> None:
    health = st.session_state.health
    history = st.session_state.health_history

    hero(
        "Mission Dashboard",
        "A unified view of crew records, monitoring patterns, and review workflow.",
    )
    notice(
        "<b>Prototype notice:</b> this dashboard uses manually entered or "
        "synthetic data. All rule thresholds are illustrative software settings, "
        "not NASA limits or clinically validated medical thresholds."
    )

    cards = [
        ("Heart rate", f"{health['heart_rate']} bpm", "Latest entered value"),
        (
            "Blood pressure",
            f"{health['systolic_bp']}/{health['diastolic_bp']}",
            "Systolic / diastolic",
        ),
        ("Sleep", f"{float(health['sleep_hours']):.1f} h", "Latest entered value"),
        ("Health records", str(len(history)), "Saved locally"),
    ]
    for column, card in zip(st.columns(4), cards):
        with column:
            metric_card(*card)

    # The current snapshot is the newest record, so compare it with the earlier ones.
    result = evaluate_health(health, history[:-1])

    st.subheader("Explainable monitoring result")
    st.info(f"**{result['status']}** · {len(result['findings'])} finding(s)")
    for finding in result["findings"]:
        render_finding(finding)

    left, right = st.columns(2)

    with left:
        st.subheader("Mission context")
        st.write(f"**Mission:** {st.session_state.mission_name}")
        st.write(f"**Crew profile:** {st.session_state.crew_member}")
        st.write(f"**Mission day:** {health['mission_day']}")
        st.write(f"**Microgravity days:** {health['microgravity_days']}")
        st.caption("Mission context is displayed for reference only.")

    with right:
        st.subheader("Workflow overview")
        pending = sum(
            1 for item in st.session_state.handover_queue
            if item.get("status") == HANDOVER_STATUSES[0]
        )
        st.metric("Pending review items", pending)
        st.metric("Symptom reports", len(st.session_state.symptom_reports))


def page_body_map() -> None:
    hero("Interactive Body Map", "Select a region to connect it with a symptom report.")

    left, right = st.columns([1.05, 1])

    with left:
        view = st.radio("Body view", ["Front", "Back"], horizontal=True, key="body_view")
        figure = build_body_figure(view, st.session_state.selected_region)

        try:
            event = st.plotly_chart(
                figure,
                key=f"body_map_{view}",
                on_select="rerun",
                selection_mode="points",
                **STRETCH,
            )
        except TypeError:
            st.plotly_chart(figure, **STRETCH)
            st.caption("Point selection requires a newer Streamlit release. Use the selector.")
        else:
            picked = selected_region_from_event(event)
            if picked is None:
                st.session_state._last_map_pick = None
            elif picked != st.session_state._last_map_pick:
                # The chart keeps its selection across reruns, so react only to new clicks.
                st.session_state._last_map_pick = picked
                st.session_state.selected_region = picked
                st.rerun()

    with right:
        st.subheader("Selected region")

        st.session_state.region_picker = st.session_state.selected_region
        st.selectbox(
            "Body region", BODY_REGIONS, key="region_picker", on_change=on_region_picked
        )

        st.markdown(
            f"""
            <div class="section-card">
                <div class="muted">CURRENT SELECTION</div>
                <div style="font-size:1.7rem;font-weight:800;color:#6ee7d5">
                    {esc(st.session_state.selected_region)}
                </div>
                <p>This region will be attached to the next symptom report.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.button("Create symptom report", on_click=open_symptom_report, **STRETCH)

    st.caption("The body map is a schematic interface and is not an anatomical reference.")


def page_health_input() -> None:
    hero("Health Input", "Record a new set of manually entered demonstration measurements.")
    notice(
        "Use fictional or synthetic values for demonstrations. "
        "Do not enter real personal medical information."
    )

    current = st.session_state.health
    defaults = DEFAULT_HEALTH

    with st.form("health_form"):
        left, right = st.columns(2)

        with left:
            heart_rate = st.number_input(
                "Heart rate (bpm)", 20, 240,
                clamp_int(current.get("heart_rate"), 20, 240, defaults["heart_rate"]),
            )
            systolic = st.number_input(
                "Systolic blood pressure", 40, 260,
                clamp_int(current.get("systolic_bp"), 40, 260, defaults["systolic_bp"]),
            )
            diastolic = st.number_input(
                "Diastolic blood pressure", 20, 180,
                clamp_int(current.get("diastolic_bp"), 20, 180, defaults["diastolic_bp"]),
            )
            temperature = st.number_input(
                "Temperature (°C)", 30.0, 43.0,
                clamp_float(current.get("temperature"), 30.0, 43.0, defaults["temperature"]),
                step=0.1,
            )
            glucose = st.number_input(
                "Glucose demo value (mg/dL)", 20, 600,
                clamp_int(current.get("glucose"), 20, 600, defaults["glucose"]),
            )

        with right:
            sleep = st.number_input(
                "Sleep hours", 0.0, 24.0,
                clamp_float(current.get("sleep_hours"), 0.0, 24.0, defaults["sleep_hours"]),
                step=0.5,
            )
            mood = st.selectbox(
                "Mood self-check", MOOD_OPTIONS,
                index=option_index(MOOD_OPTIONS, current.get("mood"), 1),
            )
            hydration = st.selectbox(
                "Hydration self-check", HYDRATION_OPTIONS,
                index=option_index(HYDRATION_OPTIONS, current.get("hydration")),
            )
            fatigue = st.slider(
                "Fatigue self-rating", 0, 10,
                clamp_int(current.get("fatigue"), 0, 10, defaults["fatigue"]),
            )
            mission_day = st.number_input(
                "Mission day", 0, 5000,
                clamp_int(current.get("mission_day"), 0, 5000, defaults["mission_day"]),
            )
            microgravity_days = st.number_input(
                "Microgravity days", 0, 5000,
                clamp_int(
                    current.get("microgravity_days"), 0, 5000, defaults["microgravity_days"]
                ),
            )

        notes = st.text_area(
            "Optional context note", value=str(current.get("notes", "") or "")
        )
        submitted = st.form_submit_button("Save health record", **STRETCH)

    if not submitted:
        return

    if systolic <= diastolic:
        st.error(
            "Please check the blood-pressure entry: systolic must be greater than diastolic."
        )
    elif microgravity_days > mission_day:
        st.error("Microgravity days cannot exceed the mission day.")
    else:
        add_health_record({
            "heart_rate": heart_rate,
            "systolic_bp": systolic,
            "diastolic_bp": diastolic,
            "temperature": round(temperature, 1),
            "glucose": glucose,
            "sleep_hours": round(sleep, 1),
            "mood": mood,
            "hydration": hydration,
            "fatigue": fatigue,
            "mission_day": mission_day,
            "microgravity_days": microgravity_days,
            "notes": notes.strip(),
        })
        st.success("Health record saved locally.")


def page_symptom_report() -> None:
    hero("Symptom Report", "Create a structured report and add it to the local review queue.")

    with st.form("symptom_form", clear_on_submit=True):
        region = st.selectbox(
            "Body region", BODY_REGIONS,
            index=option_index(BODY_REGIONS, st.session_state.selected_region),
        )
        category = st.selectbox("Report category", SYMPTOM_CATEGORIES)
        intensity = st.slider("Self-rated intensity", 0, 10, 3)
        onset = st.selectbox("When did it begin?", ONSET_OPTIONS)
        trend = st.selectbox("Recent trend", TREND_OPTIONS)
        urgent_flags = st.multiselect("Urgent-sign checklist", URGENT_FLAGS)
        summary = st.text_area(
            "Description", placeholder="Describe what was noticed and when."
        )
        submitted = st.form_submit_button("Submit symptom report", **STRETCH)

    if submitted:
        if not summary.strip():
            st.error("Please enter a short description.")
        else:
            priority, routing_note = classify_symptom_report(intensity, trend, urgent_flags)
            report = add_symptom_report({
                "region": region,
                "category": category,
                "intensity": intensity,
                "onset": onset,
                "trend": trend,
                "urgent_flags": urgent_flags,
                "summary": summary.strip(),
                "priority": priority,
                "routing_note": routing_note,
            })
            st.success(f"Report {report['id']} saved and added to the local handover queue.")
            if urgent_flags:
                st.warning(
                    "Follow the mission's established emergency procedure. "
                    "This application does not assess or manage emergencies."
                )

    st.caption("Priority labels are administrative workflow labels, not medical triage.")


TREND_METRICS = {
    "heart_rate": "Heart rate (bpm)",
    "sleep_hours": "Sleep (hours)",
    "temperature": "Temperature (°C)",
    "systolic_bp": "Systolic pressure",
    "diastolic_bp": "Diastolic pressure",
    "fatigue": "Fatigue self-rating",
}


def page_intelligence() -> None:
    hero("Mission Intelligence", "Explore recorded trends and compare recent values.")

    records = st.session_state.health_history
    if len(records) < 2:
        st.info("At least two saved health records are required for a trend.")
        return

    frame = pd.DataFrame(records)
    if "timestamp" not in frame.columns:
        st.warning("Timestamps are unavailable.")
        return

    frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="coerce", utc=True)
    frame = frame.dropna(subset=["timestamp"]).sort_values("timestamp")

    metric = st.selectbox(
        "Choose a trend", list(TREND_METRICS), format_func=TREND_METRICS.__getitem__
    )
    if metric not in frame.columns:
        st.warning("This field is unavailable.")
        return

    frame[metric] = pd.to_numeric(frame[metric], errors="coerce")
    frame = frame.dropna(subset=[metric])
    if frame.empty:
        st.info("No numeric records are available.")
        return

    figure = go.Figure(go.Scatter(
        x=frame["timestamp"], y=frame[metric], mode="lines+markers",
        line=dict(color="#54d6ca", width=3), marker=dict(size=8),
        name=TREND_METRICS[metric],
    ))
    figure.update_layout(
        height=390,
        margin=dict(l=10, r=10, t=25, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#d5e2ef"),
        xaxis_title="Recorded time",
        yaxis_title=TREND_METRICS[metric],
    )
    figure.update_xaxes(gridcolor="#20364c")
    figure.update_yaxes(gridcolor="#20364c")
    st.plotly_chart(figure, **STRETCH)

    first, second, third = st.columns(3)
    first.metric("Latest", f"{frame[metric].iloc[-1]:.2f}")
    second.metric("Record average", f"{frame[metric].mean():.2f}")
    third.metric("Records", len(frame))

    st.caption(
        "These statistics describe recorded data only. They are not a prediction or diagnosis."
    )

    st.subheader("Recent records")
    st.dataframe(
        frame[["timestamp", metric]].tail(10).sort_values("timestamp", ascending=False),
        hide_index=True,
        **STRETCH,
    )


def page_handover() -> None:
    hero("Mission Review Queue", "A local queue for structured review reports.")

    queue = st.session_state.handover_queue
    if not queue:
        st.info("No review items yet. Submit a symptom report first.")
        return

    for item in queue:
        with st.container(border=True):
            st.markdown(f"### {item.get('title', 'Review item')}")
            st.caption(f"{item.get('id')} · {item.get('timestamp', '')}")
            st.write(item.get("summary", ""))
            st.write(f"**Priority:** {item.get('priority', 'Not specified')}")
            st.write(f"**Region:** {item.get('region', 'Not specified')}")
            st.selectbox(
                "Workflow status",
                HANDOVER_STATUSES,
                index=option_index(HANDOVER_STATUSES, item.get("status")),
                key=f"status_{item['id']}",
                on_change=on_status_changed,
                args=(item["id"],),
            )

    st.caption("No report is transmitted to a clinician, spacecraft, or mission control.")


def build_export() -> bytes:
    payload = {
        "project": APP_NAME,
        "version": VERSION,
        "exported_at": now_iso(),
        "mission": {
            "name": st.session_state.mission_name,
            "crew_profile": st.session_state.crew_member,
        },
        "current_health_snapshot": st.session_state.health,
        "health_history": st.session_state.health_history,
        "symptom_reports": st.session_state.symptom_reports,
        "review_queue": st.session_state.handover_queue,
        "disclaimer": DISCLAIMER,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2, default=str).encode("utf-8")


def page_export() -> None:
    hero("Data Export", "Download a complete snapshot of the local project data.")
    st.write(
        "The export includes mission labels, current health data, historical records, "
        "symptom reports, and the review queue."
    )
    st.download_button(
        "Download complete JSON snapshot",
        data=build_export(),
        file_name=f"astra_health_{date.today().isoformat()}.json",
        mime="application/json",
        **STRETCH,
    )
    st.caption("Use synthetic data. Store exported files carefully.")


def page_resources() -> None:
    hero(
        "Space Health Knowledge Base",
        "A guided overview of the official NASA and Canadian Space Agency resources referenced by this prototype.",
    )

    st.subheader("NASA Human Research Program: five hazards")
    st.write(
        "NASA groups major human-spaceflight challenges into five connected hazard areas. "
        "These are mission-level research topics, not individual diagnoses."
    )

    hazard_cards = [
        (
            "Space radiation",
            "Radiation exposure is an important consideration for crew health, especially on missions beyond Earth's protective environment.",
        ),
        (
            "Isolation and confinement",
            "Long periods in a confined, remote environment can affect sleep, behavior, well-being, and team performance.",
        ),
        (
            "Distance from Earth",
            "Communication delays and limited access to supplies or medical support increase the need for reliable onboard information and planning.",
        ),
        (
            "Gravity fields",
            "Microgravity and transitions between gravity environments require the human body to adapt; NASA studies effects on multiple body systems.",
        ),
        (
            "Hostile and closed environments",
            "Spacecraft conditions such as temperature, pressure, lighting, noise, water, and microbial environments are important to crew health and performance.",
        ),
    ]
    for index, (title, description) in enumerate(hazard_cards, start=1):
        with st.container(border=True):
            st.markdown(f"**{index}. {title}**")
            st.write(description)

    st.markdown(
        "[NASA — Five Hazards of Human Spaceflight](https://www.nasa.gov/hrp/hazards/)"
    )

    st.subheader("NASA: human-spaceflight risks and ongoing research")
    st.markdown(
        """- [Risks of Human Spaceflight](https://www.nasa.gov/hrp/risks/) — an overview of identified human-health and performance risks.
- [Ongoing HRP Research in Space](https://www.nasa.gov/hrp/ongoing-hrp-research/) — articles about current Human Research Program work.
- [NASA Human Research Roadmap](https://humanresearchroadmap.nasa.gov/) — research gaps and risk information.
- [NASA Technical Standards](https://standards.nasa.gov/) — technical standards and reference material."""
    )

    st.subheader("Canadian Space Agency (CSA) partner resources")
    st.markdown(
        """- [Monitoring Radiation for Astronaut Health](https://www.asc-csa.gc.ca/eng/news/articles/2026/2026-02-26-monitoring-radiation-astronaut-health.asp) — an overview of radiation monitoring technologies and research.
- [Why Do We Conduct Science Experiments in Space?](https://www.asc-csa.gc.ca/eng/iss/science/why-do-we-conduct-science-experiments-in-space.asp) — background on the value of research in the space environment."""
    )

    notice(
        "<b>Source and data-use note:</b> This knowledge base provides NASA/CSA scientific context. "
        "ASTRA HEALTH also retrieves and retrospectively analyzes the public NASA OSDR OSD-575 "
        "Inspiration4 serum dataset in the separate NASA OSDR analytics page. Those descriptive "
        "comparisons do not set the prototype's demonstration alert thresholds and are not clinical "
        "decision support. Follow the terms of each external source. NASA does not endorse non-U.S. "
        "Government entities and is not responsible for information on non-U.S. Government websites."
    )

    st.subheader("What ASTRA HEALTH currently does")
    st.markdown(
        """- Manual entry of demonstration health indicators and mission context
- Local SQLite storage on the computer running the app
- Schematic body-region selection and structured symptom reports
- Transparent, rule-based demonstration checks with an explanation for each finding
- Comparison with a recent personal heart-rate reference when enough earlier records exist
- Historical trend charts, a local review queue, and JSON export
- A separate NASA OSDR analytics module that compares Inspiration4 serum biomarkers with each crew code's own pre-flight mean and displays source-provided ranges"""
    )

    st.subheader("Current system boundaries")
    st.markdown(
        """- No live spacecraft sensors or live NASA telemetry; the OSD-575 connection is retrospective public research data only
- No machine-learning model or automated prediction
- No clinically validated thresholds, diagnosis, treatment advice, or medical triage
- No secure multi-user authentication or encrypted clinical database
- No automatic communication with a flight surgeon or mission control
- No radiation dosimeter integration or environmental sensor fusion"""
    )

    notice(
        "<b>Scientific integrity:</b> ASTRA HEALTH is an educational challenge prototype. "
        "Its demonstration rules are software examples only and require assessment by qualified "
        "aerospace-medicine professionals before any real-world use."
    )


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

PAGES = {
    "Mission Dashboard": page_dashboard,
    "Interactive Body Map": page_body_map,
    "Health Input": page_health_input,
    "Symptom Report": page_symptom_report,
    "Mission Intelligence": page_intelligence,
    "Mission Review Queue": page_handover,
    "Data Export": page_export,
    "Space Health Knowledge Base": page_resources,
    "NASA OSDR Research Data": page_nasa_osdr,
}


def main() -> None:
    init_database()
    initialize_state()
    st.markdown(STYLES, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(f"# 🛰️ {APP_NAME}")
        st.caption(f"Explainable Crew Health Prototype · v{VERSION}")
        st.divider()

        page = st.radio("Navigation", list(PAGES), key="navigation")

        st.divider()
        st.markdown("### Mission configuration")
        st.text_input("Mission label", key="mission_name")
        st.text_input("Crew profile label", key="crew_member")

        st.divider()
        st.markdown(
            '<div class="muted">LOCAL PROTOTYPE<br>Manual / synthetic + historical NASA research<br>'
            "No external transmission</div>",
            unsafe_allow_html=True,
        )

    PAGES[page]()

    st.divider()
    st.markdown(
        '<div class="muted" style="text-align:center;padding:10px">'
        f"{APP_NAME} · VANGUARD POLARIS<br>NASA Space Apps Challenge 2026<br>"
        "Prototype only — not a medical device or flight-certified system.</div>",
        unsafe_allow_html=True,
    )


main()
