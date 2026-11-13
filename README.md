<div align="center">

# ASTRA HEALTH
### Because Every Mission Matters.

**An explainable, rule-based astronaut health-monitoring prototype for space missions**

Built by **VANGUARD POLARIS**  
[Janyar Rakhshanfar](https://github.com/Janyar2016) · Sobhan Rakhshanfar

[![NASA Space Apps Challenge 2026](https://img.shields.io/badge/NASA%20Space%20Apps-Challenge%202026-0B3D91?style=for-the-badge&logo=nasa&logoColor=white)](https://www.spaceappschallenge.org/)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Version](https://img.shields.io/badge/Version-4.0.0-16A34A?style=for-the-badge)

</div>

---

## The mission

Spaceflight creates a demanding environment for human health and performance. Crew members and mission-support teams need clear ways to record health information, review reported symptoms, and understand changes across available records.

**ASTRA HEALTH** is a local software prototype that brings manually entered health indicators, symptom reports, historical trends, and a structured review workflow into one mission-oriented interface.

The prototype focuses on **organizing information and making its software-generated findings explainable**. It is not a medical device and does not make clinical or flight-medical decisions.

## What ASTRA HEALTH includes

| Feature | Current implementation |
|---|---|
| **Mission Dashboard** | Presents the current demonstration health snapshot and rule-based findings. |
| **Interactive Body Map** | Lets a user select a body region as part of symptom reporting. |
| **Health Input** | Records manually entered health indicators and mission context. |
| **Explainable Rule-Based Monitoring** | Applies transparent demonstration rules and shows why a rule was activated. It is not AI or machine learning. |
| **Symptom Report** | Captures structured symptom information, body region, severity, onset, progression, and selected warning indicators. |
| **Mission Intelligence** | Displays available historical measurements and trend charts. |
| **Mission Review Queue** | Stores submitted symptom-review items locally and supports workflow-status updates. |
| **Data Export** | Downloads a JSON snapshot of the available project records. |
| **Space Health Knowledge Base** | Summarizes selected NASA Human Research Program topics and links to NASA and Canadian Space Agency (CSA) reference material. |

## How the application works

1. **Enter information:** The user enters demonstration health measurements or submits a structured symptom report.
2. **Validate and assess:** The application checks inputs and applies its implemented, explainable demonstration rules.
3. **Store locally:** SQLite stores health history, symptom reports, and review-queue items in a local database file.
4. **Review patterns:** The dashboard and trend views present the information available in the local record history.
5. **Track review workflow:** Submitted symptom reports are represented in the local Mission Review Queue, where their workflow status can be updated.
6. **Export:** The user can download a JSON snapshot of the application data.

### Local database

The application creates `astra_health.db` in the same directory as `app.py`. It uses three SQLite tables:

- `health_history` — saved health-input records.
- `symptom_reports` — submitted symptom reports.
- `handover_queue` — local review items and their workflow statuses.

The database is local to the computer running the application. It is not a NASA database, cloud service, or secure clinical record system. The application does not automatically transmit records to a clinician, spacecraft, or mission control.

## NASA and CSA research context

The **Space Health Knowledge Base** introduces five broad human-spaceflight hazard areas described by NASA: space radiation, isolation and confinement, distance from Earth, gravity fields, and hostile or closed environments. It also links to NASA Human Research Program risk and research pages, the NASA Human Research Roadmap, NASA Technical Standards, and selected CSA educational and research resources.

These materials provide **scientific background and context**. The current prototype does **not** download, ingest, or analyze NASA/CSA telemetry or research datasets. Its demonstration thresholds are not NASA or CSA medical limits and are not derived from those websites.

See [Scientific References](docs/scientific_references.md) and [Resources](resources.txt).

## Technology

- **Python** — application logic
- **Streamlit** — interactive web interface
- **Pandas** — data handling and trend preparation
- **Plotly** — interactive charts and body-region selection
- **SQLite** — local persistence
- **JSON** — structured data export

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/Janyar2016/VANGUARD-2026.git
cd VANGUARD-2026
```

### 2. (Optional) Create a virtual environment

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Start the application

```bash
streamlit run app.py
```

The terminal displays a local address for opening ASTRA HEALTH in a browser. On first startup, the application initializes the SQLite tables and creates `astra_health.db` beside `app.py`.

## Repository structure

```text
VANGUARD-2026/
├── app.py
├── requirements.txt
├── README.md
├── AI_USAGE.md
├── resources.txt
├── .gitignore
└── docs/
    ├── project_overview.md
    ├── problem_statement.md
    ├── innovation.md
    ├── system_architecture.md
    ├── methodology.md
    ├── testing_and_validation.md
    ├── limitations.md
    ├── future_work.md
    └── scientific_references.md
```

## Safety, scope, and limitations

ASTRA HEALTH is an **educational software prototype**.

- It does not diagnose conditions, prescribe treatment, or make flight-medical decisions.
- Its thresholds and alert rules are illustrative software settings, not clinically validated reference ranges or official NASA limits.
- It uses manually entered or synthetic demonstration information; it does not connect to live spacecraft sensors or NASA telemetry.
- Its monitoring engine is rule-based. It is not a trained AI or machine-learning model.
- Priority labels are workflow labels for software demonstration, not medical triage.
- The review queue is local and does not send reports to medical personnel or mission control.
- SQLite storage is local and is not presented as encrypted, multi-user, or clinically secure storage.
- Use fictional or synthetic information for demonstrations. Do not enter real personal medical information.

Any real health concern must be handled through the appropriate approved procedures and qualified professionals.

## Project documentation

| Document | Purpose |
|---|---|
| [Project Overview](docs/project_overview.md) | Purpose, scope, users, and implemented features |
| [Problem Statement](docs/problem_statement.md) | The spaceflight health-information challenge |
| [Innovation](docs/innovation.md) | The prototype's integrated workflow and explainability |
| [System Architecture](docs/system_architecture.md) | Application layers, SQLite schema, and data flow |
| [Methodology](docs/methodology.md) | Input, rule assessment, persistence, review, and export |
| [Testing and Validation](docs/testing_and_validation.md) | Test plan, recorded checks, and testing limitations |
| [Limitations](docs/limitations.md) | Current technical and scientific boundaries |
| [Future Work](docs/future_work.md) | Possible next development steps |
| [Scientific References](docs/scientific_references.md) | NASA and CSA background resources |

## Team

**VANGUARD POLARIS**

- Janyar Rakhshanfar
- Sobhan Rakhshanfar

Created for the **NASA Space Apps Challenge 2026**.

---

<div align="center">

**ASTRA HEALTH**  
*Because Every Mission Matters.*

</div>
