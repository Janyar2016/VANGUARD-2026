# System Architecture
## ASTRA HEALTH Technical Architecture

**Application version:** 4.0.0

### 1. Architecture Overview

ASTRA HEALTH is a local Streamlit application. Its architecture separates user interaction, input validation, demonstration-rule assessment, local persistence, visualization, review workflow, and export.

### 2. Main Components

**1. User Interface — Streamlit**

The interface provides the Mission Dashboard, Interactive Body Map, Health Input, Symptom Report, Mission Intelligence, Mission Review Queue, Data Export, and Space Health Knowledge Base.

**2. Input and Validation**

Users manually enter health indicators, mission context, and symptom details. The application applies basic input handling and validation before processing the submitted information.

**3. Rule-Based Assessment**

The monitoring engine applies predefined demonstration rules to selected measurements and combinations of inputs. Findings are presented with explanations. The rules are transparent software examples, not clinical thresholds, medical triage, AI, or machine learning.

**4. Data Persistence — SQLite**

Python's `sqlite3` module stores application records in `astra_health.db`, created beside `app.py`.

| Table | Stored content |
|---|---|
| `health_history` | Record ID, timestamp, and JSON payload for each health-input record |
| `symptom_reports` | Report ID, timestamp, and JSON payload for each symptom report |
| `handover_queue` | Review-item ID, timestamp, workflow status, and JSON payload |

A submitted symptom report and its corresponding review-queue item are inserted within one database transaction. Review-item status changes are written to the local queue table.

**5. Visualization and Review**

The dashboard, body map, and trend charts present the information available in the local application state and stored history. The Mission Review Queue displays submitted symptom-review items and their workflow status.

**6. Export**

The Data Export page creates a JSON snapshot containing the project/version metadata, mission labels, current health snapshot, health history, symptom reports, and review queue.

### 3. Data Flow

**Health-input path**

User enters health measurements → input handling and validation → demonstration-rule assessment → SQLite `health_history` persistence → dashboard and trend views.

**Symptom-report path**

User selects a body region and enters symptom details → report construction and demonstration assessment → SQLite transaction inserts into `symptom_reports` and `handover_queue` → Mission Review Queue displays the item → status updates are saved to SQLite.

**Export path**

Current application records → JSON serialization → downloadable JSON snapshot.

### 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface and interaction |
| Pandas | Tabular data handling and trend preparation |
| Plotly | Interactive charts and body-map interaction |
| SQLite (`sqlite3`) | Local relational persistence |
| JSON | Structured record payloads and export |

### 5. Deployment and Storage Boundary

The application runs locally through Streamlit. The database file is stored on the same computer as the application unless the user changes the deployment environment. The current prototype does not provide cloud synchronization, secure multi-user authentication, encrypted clinical storage, live sensor ingestion, or automatic remote report transmission.

### 6. Design Principles

- **Explainability:** show which demonstration rule produced a finding.
- **Local-first data handling:** keep prototype records in a local SQLite file.
- **Separation of concerns:** distinguish user-entered records, rule-generated findings, and review workflow items.
- **Scientific transparency:** distinguish external research references from datasets actually ingested by the software.
- **Safe scope:** avoid diagnostic or operational medical claims.
