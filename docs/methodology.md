
# Methodology
## How ASTRA HEALTH Works

### 1. General Approach

ASTRA HEALTH follows a structured workflow for collecting, organizing, reviewing, and presenting astronaut health information.

The methodology combines user-entered health measurements, symptom reports, historical records, and rule-based assessment.

### 2. Data Collection

The system collects different categories of information:

**Physiological Measurements**
- Heart rate.
- Blood pressure.
- Body temperature.
- Blood glucose, when available.

**Daily Health Information**
- Sleep duration.
- Mood and self-reported well-being.

**Symptom Information**
- Selected body region.
- Symptom description.
- Reported severity.
- Time of onset.
- Symptom progression.

### 3. Data Organization and Validation

Submitted information is organized into structured records.

The system checks input completeness and basic validity before using the information in its analysis.

Missing or invalid values should be distinguished from actual measurements.

### 4. Health Indicator Assessment

Available measurements are reviewed using the demonstration rules implemented in the current prototype.

The system can identify selected values or combinations of inputs that meet predefined conditions.

These rules are intended to demonstrate the software workflow and are not clinically validated medical thresholds.

### 5. Personal Trend Comparison

When historical records are available, the system compares selected current measurements with previous records.

This comparison helps highlight changes from an individual's recorded history.

Historical differences are treated as observations that may require review, not as proof of a medical condition.

### 6. Symptom Assessment

When a user submits a symptom report, the system organizes the information according to:
- Body location.
- Symptom description.
- Reported severity.
- Onset.
- Progression.
- Selected warning indicators.

The system then applies its implemented demonstration rules to assign a report priority.

### 7. Alert Generation

The alert assessment process evaluates the available information and highlights reports that meet selected conditions.

The resulting alert includes relevant information about the submitted data and the reason the report was highlighted.

The alert is intended to support human review and does not provide a medical diagnosis.

### 8. Reporting and Data Export

The system organizes symptom reports and available health information into structured records.

These records can be reviewed through the application and exported in JSON format for further analysis.

### 9. Testing Approach

The methodology can be evaluated using synthetic test scenarios with different combinations of health measurements and reported symptoms.

Testing focuses on:
- Correct data entry and validation.
- Accurate selection of body regions.
- Consistent application of demonstration rules.
- Correct generation of reports.
- Appropriate display of alerts.
- Successful data export.

### 10. Methodological Limitations

The current methodology is based on a software prototype and demonstration rules.

It has not been clinically validated using astronaut medical datasets or operational mission conditions.

Further research, reliable spaceflight health references, and expert review would be necessary before operational use.
