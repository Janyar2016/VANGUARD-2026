# ASTRA HEALTH
## Project Overview

**Team:** VANGUARD POLARIS  
**Challenge:** Create Health Monitoring Software for Astronauts on Space Missions  
**Platform:** Python, Streamlit, SQLite  
**Application version:** 4.0.0

### 1. Introduction

ASTRA HEALTH is an educational software prototype exploring how astronaut health information can be recorded, organized, reviewed, and communicated during space missions.

Spaceflight introduces health and performance challenges associated with radiation, isolation and confinement, distance from Earth, changing gravity environments, and the spacecraft's closed and demanding environment. Health information can also be distributed across measurements, self-reports, and records collected at different times.

ASTRA HEALTH brings manually entered demonstration health indicators, structured symptom reports, historical trends, and a local review workflow into one interface.

### 2. Project Goal

The goal is to demonstrate an explainable software workflow for organizing health-related information in a mission-oriented setting. The application is intended to support information review, not to make medical decisions.

### 3. Implemented Features

- **Mission Dashboard:** presents the current demonstration health snapshot and findings produced by implemented rules.
- **Interactive Body Map:** supports selection of a body region during symptom reporting.
- **Health Input:** accepts manually entered health indicators and mission context.
- **Explainable Rule-Based Monitoring:** evaluates selected values and combinations using visible demonstration rules.
- **Symptom Report:** stores structured symptom details, including body region, description, severity, onset, progression, and selected warning indicators.
- **Mission Intelligence:** displays available historical records and trend charts.
- **Mission Review Queue:** lists local review items created from submitted symptom reports and allows workflow-status changes.
- **Data Export:** downloads a JSON snapshot containing the available project records.
- **Space Health Knowledge Base:** introduces selected NASA human-spaceflight hazard and research topics and links to selected NASA and CSA resources.

### 4. Local Data Storage

The application uses SQLite through Python's `sqlite3` module. On startup it initializes three tables in `astra_health.db`, located beside `app.py`:

| Table | Purpose |
|---|---|
| `health_history` | Stores submitted health-input records |
| `symptom_reports` | Stores submitted symptom reports |
| `handover_queue` | Stores local review items and workflow status |

This is local persistence on the computer running the app. It is not a cloud database, operational NASA system, or secure clinical records platform.

### 5. Intended Context

The prototype is designed around the information-management challenges of human spaceflight and may be useful as an educational demonstration for people exploring astronaut health monitoring software concepts. It has not been evaluated for operational use by astronauts or medical teams.

### 6. Technology

- Python — application logic
- Streamlit — interactive interface
- Pandas — data organization and trend preparation
- Plotly — charts and interactive body-region selection
- SQLite — local database
- JSON — data export

### 7. Scope and Safety

ASTRA HEALTH is not a certified medical device. It does not diagnose conditions, prescribe treatment, or make flight-medical decisions. Its rule thresholds are illustrative demonstration settings, not clinically validated reference ranges or official NASA/CSA limits.

The application uses manually entered or synthetic data. It does not connect to real astronaut sensors, spacecraft telemetry, or NASA/CSA research datasets. It does not transmit reports to a clinician, flight surgeon, spacecraft, or mission control.
