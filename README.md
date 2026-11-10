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

Space missions place unique demands on the human body. Health information can become difficult to review when measurements, symptoms, and trends are spread across different records.

**ASTRA HEALTH** is a prototype designed to make that information easier to organize, explore, and review. It brings health inputs, visual trends, symptom reports, and medical handover notes into one interface.

Our goal is simple:

> Help make astronaut health information clearer and easier for a mission team to review.

## ✨ What ASTRA HEALTH can do

| Feature | What it does |
|---|---|
| **Mission Dashboard** | Presents a mission-focused overview of recorded health information. |
| **Interactive Body Map** | Lets a user select a body region when recording a symptom. |
| **Health Input** | Records selected health indicators and mission-related information. |
| **Explainable Rule Checks** | Applies transparent demonstration rules to highlight patterns that may deserve review. |
| **Mission Intelligence** | Visualizes recorded measurements and changes over time. |
| **Symptom Reports** | Organizes symptom details, intensity, onset, and reported trend. |
| **Medical Handover** | Creates and tracks structured notes for human review. |
| **Data Export** | Supports exporting project records in JSON format. |

## 🧠 How the prototype works

1. **Record** — Enter mission and health information.
2. **Organize** — Store records locally in an SQLite database.
3. **Analyze** — Run transparent, rule-based checks on the entered demonstration data.
4. **Visualize** — Explore measurements and trends through charts and the dashboard.
5. **Review** — Prepare symptom and handover information for a qualified human reviewer.

The current analysis is **rule-based and explainable**. It is not a trained machine-learning model and does not make medical decisions.

## 🛠️ Technology

- **Python** — application logic
- **Streamlit** — interactive web interface
- **Pandas** — data handling
- **Plotly** — interactive visualizations
- **SQLite** — local data storage

## 🚀 Run the project locally

### 1. Get the code

```bash
git clone https://github.com/Janyar2016/VANGUARD-2026.git
cd VANGUARD-2026
```

### 2. Create and activate a virtual environment

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

Install the packages used by the app:

```bash
python -m pip install streamlit pandas plotly
```

### 4. Start the app

If the main application file is named `app.py`:

```bash
streamlit run app.py
```

If your local main file has a different name, replace `app.py` with that filename.

## 🗂️ Project documentation

The `docs/` directory contains the project's supporting documents:

- Project overview
- Problem statement
- Innovation
- System architecture
- Methodology
- Testing and validation
- Limitations
- Future work
- Scientific references

These documents explain the project's purpose, design choices, current scope, and areas that still need further work.

## ⚠️ Important scope and limitations

ASTRA HEALTH is an **educational challenge prototype**, not a certified medical device or clinical decision-support system.

- It does not diagnose diseases or prescribe treatment.
- Its demonstration rules are illustrative and have not been clinically validated.
- It does not currently connect to live spacecraft sensors or NASA telemetry.
- Demonstration or manually entered data should not be interpreted as verified astronaut medical data.
- A human expert must review any health concern; the prototype must not be used to make real mission or treatment decisions.

## 🔭 Next steps

The next development stage is to review the official challenge resources and determine which relevant datasets, references, or tools can be responsibly incorporated. Further work may include stronger validation, clearer evidence for analysis rules, and improved data-handling safeguards.

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
