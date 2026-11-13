# Limitations
## Current Limitations of ASTRA HEALTH

**Application version:** 4.0.0

### 1. Prototype Status

ASTRA HEALTH is an educational challenge prototype. It is not certified or approved as a medical device and is not intended for operational medical use during space missions.

### 2. Input Data

The current application relies on manually entered or synthetic demonstration information. It does not connect to real astronaut medical sensors, spacecraft telemetry, or operational NASA/CSA systems.

### 3. NASA and CSA Resources

The Space Health Knowledge Base provides summaries and links to selected NASA and Canadian Space Agency resources. These references provide background context only. The prototype does not ingest, download, or analyze the linked organizations' telemetry or research datasets. The inclusion of a reference does not imply NASA or CSA endorsement.

### 4. Rule and Threshold Validity

The monitoring rules and thresholds are illustrative software settings. They have not been clinically validated and must not be interpreted as official NASA/CSA limits, diagnostic criteria, validated risk scores, or medical triage.

### 5. Database and Privacy

SQLite provides local persistence for the prototype's health history, symptom reports, and review queue. The current implementation is not a secure clinical records system. It does not provide encrypted medical storage, multi-user authentication, role-based access control, cloud backup, or secure synchronization. Only fictional or synthetic data should be used in demonstrations.

### 6. Review Workflow and Connectivity

Mission Review Queue is a local workflow. It does not automatically communicate with a clinician, flight surgeon, spacecraft, or mission control. Live communication and remote medical-team integration are not implemented.

### 7. Analytical Scope

The application uses transparent, rule-based demonstration checks. It does not contain a trained machine-learning model or an automated predictive system. Historical charts describe entered records and do not establish medical conclusions.

### 8. Environmental and Mission Data

The current version does not integrate radiation dosimeter readings, spacecraft environmental sensors, exercise equipment, or other live mission systems.

### 9. Requirements Before Real-World Use

Any future operational direction would require, at minimum:
- Appropriate and lawfully usable astronaut-health datasets.
- Review by qualified aerospace-medicine and software-safety experts.
- Clinical and operational validation under representative conditions.
- Strong privacy, cybersecurity, access-control, and data-governance measures.
- Integration and reliability testing with authorized systems.

### 10. Conclusion

The current prototype demonstrates a local information-management and review workflow. These limitations define what the software currently does and what remains outside its scope.
