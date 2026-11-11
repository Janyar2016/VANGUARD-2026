<div align="center">

# ASTRA HEALTH
### Because Every Mission Matters.

**An explainable astronaut health-monitoring prototype for space missions**

Built by **VANGUARD POLARIS**  
[Janyar Rakhshanfar](https://github.com/Janyar2016) · Sobhan Rakhshanfar

[![NASA Space Apps Challenge 2026](https://img.shields.io/badge/NASA%20Space%20Apps-Challenge%202026-0B3D91?style=for-the-badge&logo=nasa&logoColor=white)](https://www.spaceappschallenge.org/)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Project status](https://img.shields.io/badge/Status-Prototype-16A34A?style=for-the-badge)

</div>

---

## 🌌 The mission

Space missions place unusual demands on the human body. Health measurements, symptoms, and changes over time can be difficult for a crew or mission-support team to review when the information is scattered across separate records.

**ASTRA HEALTH** is a software prototype that brings manually entered health information, symptom reports, visual trends, and structured handover records into one mission-oriented interface.

Its purpose is to make demonstration health information easier to record, organize, understand, and prepare for human review.

> **Every mission matters. Every health record deserves careful review.**

## ✨ Main features

| Feature | Description |
|---|---|
| **Mission Dashboard** | Displays the current demonstration health snapshot, monitoring results, mission context, and workflow overview. |
| **Interactive Body Map** | Allows the user to select a body region and connect it to a symptom report. |
| **Health Input** | Records manually entered health indicators and mission-related context. |
| **Explainable Monitoring** | Uses visible, rule-based demonstration checks and displays the reasons behind its findings. |
| **Symptom Reports** | Organizes a reported body region, category, intensity, onset, trend, and selected warning signs. |
| **Mission Intelligence** | Shows charts and summary statistics for previously recorded measurements. |
| **Medical Handover** | Keeps structured reports in a local review queue with workflow statuses. |
| **Data Export** | Exports the current project records as a JSON snapshot. |
| **Resources & Limitations** | Explains implemented capabilities, project boundaries, and relevant NASA reference resources. |

## 🧭 How it works

1. **Record:** Enter fictional or synthetic demonstration measurements and mission context.
2. **Store:** Save records locally in an SQLite database.
3. **Check:** Apply transparent, rule-based demonstration checks to the entered values and available history.
4. **Explore:** Review the dashboard, selected body region, reports, and recorded trends.
5. **Prepare for review:** Add structured symptom information to the local handover queue.
6. **Export:** Download a JSON snapshot of the stored project information.

The current monitoring logic is **rule-based and explainable**. It is not a trained machine-learning model, and its labels are not clinical risk assessments or medical triage.

## 🛠️ Technology

- **Python** — application logic
- **Streamlit** — interactive web interface
- **Pandas** — data handling and trend preparation
- **Plotly** — interactive charts and body-region selection
- **SQLite** — local data persistence
- **JSON** — structured data export

## 📚 Project documentation

The detailed project documents are available in the [`docs/`](docs/) folder:

| Document | Description |
|---|---|
| [Project Overview](docs/project_overview.md) | Project purpose, scope, and overall concept |
| [Problem Statement](docs/problem_statement.md) | The challenge and the problem ASTRA HEALTH addresses |
| [Innovation](docs/innovation.md) | The project's approach and distinguishing features |
| [System Architecture](docs/system_architecture.md) | Main software components and their relationships |
| [Methodology](docs/methodology.md) | Development approach and application workflow |
| [Testing and Validation](docs/testing_and_validation.md) | Testing approach and validation notes |
| [Limitations](docs/limitations.md) | Current boundaries and important safety limitations |
| [Future Work](docs/future_work.md) | Potential improvements and next development steps |
| [Scientific References](docs/scientific_references.md) | Reference materials used during project research |

## 🚀 Run locally

### 1. Clone the repository

```bash
git clone https://github.com/Janyar2016/VANGUARD-2026.git
cd VANGUARD-2026
```

### 2. Create a virtual environment

**Windows (PowerShell):**

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

### 4. Launch ASTRA HEALTH

```bash
streamlit run app.py
```

Streamlit will provide a local address to open the application in your browser. The SQLite database is created locally when the application starts.

## 📁 Repository structure

```text
VANGUARD-2026/
├── app.py
├── requirements.txt
├── README.md
├── AI_USAGE.md
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

## ⚠️ Safety, scope, and limitations

ASTRA HEALTH is an **educational challenge prototype**, not a certified medical device or clinical decision-support system.

- It does not diagnose conditions, prescribe treatment, or make flight-medical decisions.
- Its demonstration rules and thresholds are illustrative and have not been clinically validated.
- The application relies on manually entered information; it does not connect to live spacecraft sensors or NASA telemetry.
- It does not contain a trained machine-learning prediction model.
- Symptom priority labels are administrative workflow labels, not medical triage.
- Handover records remain in the local application; they are not automatically sent to a clinician, flight surgeon, spacecraft, or mission control.
- Use fictional or synthetic values for demonstrations. Do not enter real personal medical information.
- Any real health concern must be handled through the appropriate approved procedures and qualified professionals.

## 🔭 Future development

Possible next steps include stronger software testing, evidence-based review of demonstration rules, improved privacy and security controls, and carefully evaluated integration with appropriate research datasets or authorized sensor interfaces.

These are future possibilities, not capabilities claimed by the current version.

## 👥 Team

**VANGUARD POLARIS**

- Janyar Rakhshanfar
- Sobhan Rakhshanfar

Created for the **NASA Space Apps Challenge 2026**.

---

<div align="center">

**ASTRA HEALTH**  
*Because Every Mission Matters.*

</div>
