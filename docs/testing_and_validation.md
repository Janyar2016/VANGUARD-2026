# Testing and Validation
## ASTRA HEALTH Software Testing

**Application version:** 4.0.0

### 1. Testing Objective

Testing evaluates whether the prototype handles demonstration inputs, applies its implemented rules consistently, stores records, presents trends, updates the local review workflow, and exports structured data.

Software testing does not establish clinical accuracy, medical safety, or readiness for astronaut operations.

### 2. Testing Environment

The application is built with Python, Streamlit, Pandas, Plotly, and SQLite (`sqlite3`). Testing should use fictional or synthetic data only.

### 3. Functional Test Plan

| Test ID | Feature | Test | Expected result |
|---|---|---|---|
| T01 | Mission Dashboard | Open the dashboard | Dashboard renders and presents the available snapshot |
| T02 | Interactive Body Map | Select a body region | Selected region is identified |
| T03 | Symptom Report | Submit a synthetic symptom report | Structured report is created and stored |
| T04 | Rule Assessment | Enter values matching a demonstration rule | Corresponding explainable finding is shown |
| T05 | Health Input | Submit synthetic measurements | Record is saved to local health history |
| T06 | Mission Intelligence | Add multiple synthetic records | Available historical trends are displayed |
| T07 | Mission Review Queue | Submit a symptom report and open the queue | Corresponding local review item is listed |
| T08 | Queue Status | Change a review item's workflow status | Updated status is saved locally |
| T09 | Data Export | Download the JSON snapshot | Export is valid JSON and contains the documented data sections |
| T10 | Database Persistence | Restart the app after creating test records | Previously saved records remain available |

### 4. Suggested Test Scenarios

**Scenario A — Normal data entry:** Submit synthetic values within the app's demonstration ranges and verify that the record appears in the available history.

**Scenario B — Rule activation:** Submit synthetic values that match a documented rule and verify the displayed explanation. Do not interpret the result as a medical assessment.

**Scenario C — Symptom reporting:** Submit a fictional symptom report, confirm that it appears in the Symptom Report history and Mission Review Queue, and check that its displayed details are consistent.

**Scenario D — Queue status persistence:** Change a queue item's workflow status, restart the application, and confirm that the new status remains.

**Scenario E — Historical trends:** Add multiple synthetic health records and confirm that the available trend chart and summary statistics reflect those records.

**Scenario F — JSON export:** Export the data and open the resulting JSON file with a JSON-aware editor to inspect its structure.

### 5. Validation Boundaries

- Functional tests assess software behavior only.
- Demonstration-rule tests assess consistency with the code, not medical correctness.
- Synthetic-data tests do not establish performance with real astronaut data.
- No test in this document should be interpreted as clinical validation or NASA certification.

### 6. Results Recording

The table below is a results template. A test should be marked **Passed** only after the named test has actually been executed against the version being documented.

| Test ID | Actual result | Status |
|---|---|---|
| T01–T10 | Record observations after executing each test | Not recorded in this document |

### 7. Further Validation Needed

Before any real-world medical or mission use, the system would require appropriate dataset governance, independent software verification, qualified aerospace-medicine review, safety assessment, privacy and security assessment, and validation under representative operational conditions.
