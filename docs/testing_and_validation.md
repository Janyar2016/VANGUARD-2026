
# Testing and Validation
## ASTRA HEALTH Software Testing

### 1. Testing Objective

The purpose of testing ASTRA HEALTH is to evaluate whether its implemented features operate correctly, process entered information consistently, and produce the expected software outputs.

Testing focuses on functionality, data handling, alert logic, visualization, and report generation.

### 2. Testing Environment

The prototype is developed using:

- Python
- Streamlit
- Pandas
- NumPy
- Plotly

Testing is performed in the local application environment using manually entered and synthetic data.

### 3. Functional Testing

The following features are included in the functional testing plan:

| Test ID | Feature | Test Description | Expected Result |
|---|---|---|---|
| T01 | Dashboard | Open the main dashboard | Dashboard loads correctly |
| T02 | Body Map | Select a body region | Selected region is identified |
| T03 | Symptom Report | Submit a symptom report | A structured report is created |
| T04 | Alert Assessment | Enter data matching a demonstration alert rule | Relevant alert is displayed |
| T05 | Health Input | Submit health measurements | New record is stored |
| T06 | Trend Analysis | Add multiple health records | Available trends are displayed |
| T07 | Medical Handover | Open the report queue | Submitted reports are listed |
| T08 | Data Export | Export a report | A valid JSON file is generated |

### 4. Test Scenarios

**Scenario 1: Normal Data Entry**

The user enters a set of health measurements within the application's demonstration ranges.

Expected result: The system stores the information and displays it correctly.

**Scenario 2: Symptom Reporting**

The user selects a body region and submits a symptom report.

Expected result: The system creates a structured report containing the submitted information.

**Scenario 3: Alert Assessment**

The user enters information that matches one of the implemented demonstration alert rules.

Expected result: The system highlights the relevant condition and displays the associated report priority.

**Scenario 4: Historical Comparison**

The user enters multiple records over time.

Expected result: The system displays available historical information and selected measurement trends.

**Scenario 5: Report Export**

The user exports a submitted report.

Expected result: The exported JSON file contains the corresponding structured information.

### 5. Validation Criteria

The software is evaluated according to the following criteria:

- Correctness of user input handling.
- Consistency of data organization.
- Correct selection and identification of body regions.
- Consistency of implemented alert rules.
- Accuracy of displayed historical comparisons.
- Completeness of generated reports.
- Successful data export.

### 6. Test Results

Actual test results will be recorded after executing each test.

| Test ID | Actual Result | Status | Notes |
|---|---|---|---|
| T01 | Dashboard loaded successfully | passed | |
| T02 | Interactive body map successfully detects body-region clicks highlights the selected region, and displays its name. | Passed | |
| T03 | Symptom report was successfully submitted. The system generated a unique Report ID, detected the selected urgent warning sign, displayed an emergency alert, and made the report available in Medical Handover. | Passed | |
| T04 | Health indicators were processed by the alert assessment system, and the corresponding health status and alert messages were displayed.	 | Passed | |
| T05 | Health input values were successfully entered, validated, and reflected in the dashboard. | Passed | |
| T06 | Health trend charts successfully displayed available historical health data and changes over time. | Passed | |
| T07 | Medical handover report was successfully generated and displayed the relevant symptom and health information. | Passed | |
| T08 | Health data was successfully exported in JSON format with the expected data structure. | Passed | |

### 7. Testing Limitations

The current testing process evaluates software functionality using synthetic or manually entered information.

It does not establish clinical accuracy, medical safety, or readiness for actual astronaut operations.

Further validation using appropriate datasets, expert review, and representative mission conditions would be required.
