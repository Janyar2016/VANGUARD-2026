
# System Architecture
## ASTRA HEALTH Technical Architecture

### 1. Architecture Overview

ASTRA HEALTH uses a modular software architecture designed to organize astronaut health information, analyze available records, and present results through an interactive interface.

The system is divided into several functional layers.

### 2. System Layers

**Layer 1: User Input**

The system receives information through user interactions, including:
- Physiological measurements.
- Sleep duration.
- Mood and well-being records.
- Symptom descriptions.
- Selected body regions.
- Mission-related information.

**Layer 2: Data Management**

Entered information is organized into structured records.

This layer manages health measurements, symptom reports, and available historical records.

**Layer 3: Data Validation**

Input values are checked to identify missing, invalid, or incorrectly formatted information before analysis.

**Layer 4: Health Analysis Engine**

The analysis layer evaluates available information using the rules currently implemented in the prototype.

It also supports comparisons between current measurements and previously recorded values.

**Layer 5: Alert Assessment**

The system evaluates selected conditions and assigns demonstration alert priorities.

Alerts are presented with relevant information to support further review.

**Layer 6: Visualization and Reporting**

The results are displayed through:
- Health monitoring dashboard.
- Interactive body map.
- Trend charts.
- Alert notifications.
- Medical handover reports.
- Structured data exports.

### 3. System Workflow

The general workflow is:

1. The user enters health information.
2. The system organizes the submitted data.
3. Input values are checked.
4. Available information is analyzed.
5. Selected rules are evaluated.
6. Relevant alerts are displayed.
7. Reports are organized for medical review.

### 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main application logic |
| Streamlit | Interactive user interface |
| Pandas | Data organization and processing |
| NumPy | Numerical operations |
| Plotly | Charts and interactive visualizations |
| JSON | Structured report export |

### 5. Data Flow

The main data flow can be represented as:

User Input → Data Management → Validation → Health Analysis → Alert Assessment → Dashboard and Reports

### 6. Architecture Design Principles

The architecture follows these principles:

**Modularity**

Different application functions are organized into separate components to make maintenance and future development easier.

**Clarity**

Health information and system-generated alerts are presented in an understandable format.

**Extensibility**

The architecture can be extended to support additional measurements, data sources, and analysis methods.

**Data Awareness**

The system distinguishes between entered information, historical records, and system-generated assessments.

### 7. Current Implementation Scope

The current prototype uses manually entered or demonstration data.

Its current storage and analysis capabilities are limited to the implemented application environment. It is not connected to operational spacecraft systems, real astronaut medical sensors, or external medical databases.
