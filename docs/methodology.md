# Methodology
## How ASTRA HEALTH Works

**Application version:** 4.0.0

### 1. General Approach

ASTRA HEALTH demonstrates a workflow for entering, organizing, reviewing, and exporting astronaut-health-related information. It combines manually entered demonstration measurements, self-reported symptom records, historical data, transparent demonstration rules, and a local review queue.

### 2. Data Entry

**Health Input**

Users enter the health indicators and mission-context fields exposed by the application. The submitted record receives an identifier and timestamp and is stored in the local health history.

**Symptom Report**

Users select a body region and submit structured symptom information. The form captures the symptom details exposed by the application, including description, severity, onset/progression information, and selected warning indicators.

### 3. Input Handling and Storage

The application performs basic input handling and stores record payloads as JSON text in SQLite tables.

- Health-input records are inserted into `health_history`.
- Symptom reports are inserted into `symptom_reports`.
- A corresponding local review item is inserted into `handover_queue`.

The symptom report and its associated queue item are written in a single SQLite transaction. The application reloads stored records when initializing its local state.

### 4. Demonstration-Rule Assessment

The monitoring logic evaluates selected entered values and combinations against predefined rules in the code. When a rule is met, the application creates an explainable finding that identifies the rule condition.

These thresholds are illustrative software settings only. They are not official NASA or CSA limits, clinical reference ranges, validated risk scores, or medical triage criteria. The engine is rule-based; it is not a trained AI or machine-learning model.

### 5. Historical Views

The Mission Intelligence page presents available historical measurements through charts and summary statistics. These views describe the records entered into the local application. They do not establish causation, predict a medical outcome, or diagnose a condition.

### 6. Mission Review Queue

The Mission Review Queue displays local workflow items associated with submitted symptom reports. Each item includes identifying and summary information, a demonstration priority label, body-region context, and a workflow status. Status changes are persisted to the SQLite queue table.

The queue is an administrative software workflow only. It does not send reports to a medical team, flight surgeon, spacecraft, or mission control.

### 7. Knowledge Base and External References

The Space Health Knowledge Base summarizes selected NASA human-spaceflight hazard topics and links to NASA and CSA research/educational pages. These sources are provided for scientific context. The application does not download or analyze the linked organizations' telemetry or research datasets.

### 8. Data Export

The Data Export page serializes the available project data into a downloadable JSON snapshot. The export includes the project and version, mission labels, current health snapshot, health history, symptom reports, review queue, and disclaimer.

### 9. Testing Method

Software behavior can be checked with fictional or synthetic inputs. Testing should cover form submission, database persistence, rule activation, chart display, review-status changes, and JSON export. Testing software behavior does not validate clinical accuracy or medical safety.

### 10. Methodological Limitations

The current method is a local software demonstration based on manual/synthetic inputs and illustrative rules. It has not been validated with astronaut medical datasets, operational spacecraft systems, or qualified clinical review.
