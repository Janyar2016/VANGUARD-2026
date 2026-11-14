# Submission Readiness and Compliance Notes

**Project:** ASTRA HEALTH  
**Team:** VANGUARD POLARIS  
**Challenge:** Create Health Monitoring Software for Astronauts on Space Missions  
**Documentation snapshot:** 2026-11-14  
**Application version documented:** 4.1.0

> This document records the current project state and submission checks. It is not a certification of contest eligibility, NASA review, or clinical validation.

## 1. Current implementation status

ASTRA HEALTH is a local, explainable, rule-based software prototype built with Python, Streamlit, and SQLite.

The documented implementation includes:
- Manually entered or synthetic health indicators.
- Structured symptom reports and an interactive body-region selector.
- Illustrative, explainable software rules.
- Historical views based on records entered into the local application.
- A local Mission Review Queue for submitted symptom reports.
- JSON export and a Space Health Knowledge Base.

Version 4.1.0 adds a NASA OSDR research-data page that downloads and displays the public processed OSD-575 Comprehensive Metabolic Panel CSV from the Inspiration4 study and calculates descriptive statistics. The app still does **not** connect to live astronaut sensors, spacecraft telemetry, or NASA/CSA operational systems. The OSD-575 dataset is a limited research dataset with samples collected at defined pre-flight and post-flight time points; it is not continuous in-flight telemetry and does not set the app's illustrative alert thresholds. Its rules are not a trained AI model, medical device, clinical decision system, or official NASA/CSA threshold set.

## 2. NASA Space Apps organizer guidance

The NASA Space Apps GO Team stated in its response to Discussion #1827 (November 5, 2026) that teams should not begin developing their challenge projects before the official hackathon start. The response says working ahead can lead to disqualification. Before the start, participants may select a challenge, review resources, research the topic, and form their team.

For a Universal Event team, the stated start time is 9:00 AM on Saturday in the Team Owner's area of residence. The team must use its actual event start time when assessing its timeline.

**Important:** This repository contains earlier project history. This documentation update does not change or conceal that history. The team must describe its actual project-development timeline truthfully. If there is uncertainty about how the guidance applies to this team's circumstances, ask the NASA Space Apps GO Team or the appropriate organizer for a written determination. This file does not claim that the project is eligible or ineligible.

Organizer clarification: https://github.com/nasa/spaceapps/discussions/1827

## 3. NASA data requirement and current gap

The same GO Team response states that teams interested in Global Awards must use at least one NASA data source included with the selected challenge's Resources. It also says that all data, resources, and tools used must be listed in the submission references.

The current ASTRA HEALTH implementation now includes a separate NASA OSDR data explorer for the public processed OSD-575 dataset. The app downloads the CMP CSV from NASA OSDR, displays its source columns, and computes descriptive statistics for numeric columns. This is a genuine use of a NASA-hosted research dataset, but it is not real-time astronaut monitoring, does not establish clinical reference ranges, and does not change the app's illustrative rule thresholds. The team must verify that OSD-575 satisfies the exact NASA-data requirement for this challenge's official Resources list before claiming Global Award eligibility.

A separate community discussion about this challenge explains that there may not be one unified downloadable astronaut-health dataset and suggests exploring NASA research repositories. That response is useful context, but it is not a substitute for checking the official challenge Resources and the actual dataset terms.

Challenge-specific discussion: https://github.com/nasa/spaceapps/discussions/2025

The implementation uses the public processed CSV from NASA OSDR study OSD-575 (Inspiration4 blood-serum Comprehensive Metabolic Panel). The app retrieves the file from the NASA OSDR download endpoint when the NASA OSDR Research Data page is opened, caches it for six hours, displays the tabular data, and computes descriptive statistics for numeric columns. The source study page lists a CC0-1.0 license. The team must still confirm that this dataset is one of the NASA resources permitted or listed for this specific challenge. Do not claim that the dataset provides continuous in-flight vital signs or that it supplies clinical alert thresholds.

## 4. Submission demo checks

According to the Project Submission Guide, the demo must be either:
- A video no longer than 30 seconds, or
- A slide deck of no more than 7 slides, including title and closing slides.

The project submission and linked materials must be in English. A video spoken in another language requires English subtitles. The demo link must be publicly accessible without sign-in or permission requests and should be tested in a private/incognito browser window.

**Under-18 likeness restriction:** The Project Submission Guide states that project demos and final projects must not include images, video, audio, or other likenesses of people under 18. Use an app-only screen recording, interface captures, diagrams, and text. Do not include a minor's face, voice, or other likeness.

## 5. AI and external-resource disclosure

The repository includes [AI_USAGE.md](../AI_USAGE.md). Before submission, every team member should review it and make sure it accurately lists the AI tools and the kinds of assistance actually used.

The final submission should list all external resources and tools actually used, including code, text, images, datasets, and other materials, even when they are open source or freely available. Do not list a source as a dataset used if it was only read as background material.

## 6. Universal Event and deadline checks

For a Universal Event team:
- At least 2 participants are required for Global Judging eligibility.
- The team must satisfy the published team-size and registration requirements.
- The relevant submission deadline is based on the Team Owner's local time, as described in the official guide.

The team should verify that all members appear on the official team page and that the Project tab contains every required field. Save progress, test all links, and complete the final submission before the deadline shown for the Team Owner.

## 7. Final factual description

A careful description of the current implementation is:

> ASTRA HEALTH is a local, explainable, rule-based astronaut-health information-management prototype. Its main monitoring workflow organizes manually entered or synthetic demonstration measurements, symptom reports, historical records, and a local review queue. A separate research-data page retrieves and displays NASA OSDR study OSD-575 processed blood-serum metabolic-panel data and provides descriptive statistics. This dataset is not live telemetry and does not set clinical thresholds. The app is not clinically validated and is not intended for operational medical decisions.

## 8. Official and project references

- NASA Space Apps 2026: https://www.spaceappschallenge.org/2026/
- Official challenge: https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/
- GO Team guidance on pre-event development and NASA data: https://github.com/nasa/spaceapps/discussions/1827
- Challenge-specific dataset discussion: https://github.com/nasa/spaceapps/discussions/2025
- Project Submission Guide: https://www.spaceappschallenge.org/resources/
- [Scientific references in this repository](scientific_references.md)
- [AI assistance disclosure](../AI_USAGE.md)
