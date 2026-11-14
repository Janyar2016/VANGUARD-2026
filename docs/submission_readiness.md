# Submission Readiness and Compliance Notes

**Project:** ASTRA HEALTH  
**Team:** VANGUARD POLARIS  
**Challenge:** Create Health Monitoring Software for Astronauts on Space Missions  
**Documentation snapshot:** 2026-11-14  
**Application version documented:** 4.0.0

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

The current version does **not** connect to live astronaut sensors, spacecraft telemetry, or NASA/CSA operational systems. It does **not** download, ingest, or analyze NASA/CSA research datasets. Its rules are not a trained AI model, medical device, clinical decision system, or official NASA/CSA threshold set.

## 2. NASA Space Apps organizer guidance

The NASA Space Apps GO Team stated in its response to Discussion #1827 (November 5, 2026) that teams should not begin developing their challenge projects before the official hackathon start. The response says working ahead can lead to disqualification. Before the start, participants may select a challenge, review resources, research the topic, and form their team.

For a Universal Event team, the stated start time is 9:00 AM on Saturday in the Team Owner's area of residence. The team must use its actual event start time when assessing its timeline.

**Important:** This repository contains earlier project history. This documentation update does not change or conceal that history. The team must describe its actual project-development timeline truthfully. If there is uncertainty about how the guidance applies to this team's circumstances, ask the NASA Space Apps GO Team or the appropriate organizer for a written determination. This file does not claim that the project is eligible or ineligible.

Organizer clarification: https://github.com/nasa/spaceapps/discussions/1827

## 3. NASA data requirement and current gap

The same GO Team response states that teams interested in Global Awards must use at least one NASA data source included with the selected challenge's Resources. It also says that all data, resources, and tools used must be listed in the submission references.

The current ASTRA HEALTH implementation documents NASA and CSA pages as **background references only**. It does not currently demonstrate the ingestion or analysis of a NASA dataset. Therefore, the repository must not claim that a NASA dataset has been integrated or analyzed.

A separate community discussion about this challenge explains that there may not be one unified downloadable astronaut-health dataset and suggests exploring NASA research repositories. That response is useful context, but it is not a substitute for checking the official challenge Resources and the actual dataset terms.

Challenge-specific discussion: https://github.com/nasa/spaceapps/discussions/2025

Before claiming NASA-data use, the team would need to:
1. Select an appropriate NASA data source that satisfies the challenge's official Resources requirement.
2. Confirm that the data can lawfully be accessed and reused.
3. Actually use the data in the project in a clearly described way.
4. Keep research data distinct from synthetic demonstration telemetry.
5. Cite the dataset, version or study identifier, access date, and relevant documentation.
6. Update the application and documentation to describe exactly what was used.

Until those steps are completed, describe the current app as using manual/synthetic demonstration inputs and NASA/CSA background references only.

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

> ASTRA HEALTH is a local, explainable, rule-based astronaut-health information-management prototype. It organizes manually entered or synthetic demonstration measurements, symptom reports, historical records, and a local review workflow. NASA and CSA publications are used as scientific background references. The current version does not ingest NASA/CSA datasets or live astronaut telemetry and is not clinically validated or intended for operational medical decisions.

## 8. Official and project references

- NASA Space Apps 2026: https://www.spaceappschallenge.org/2026/
- Official challenge: https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/
- GO Team guidance on pre-event development and NASA data: https://github.com/nasa/spaceapps/discussions/1827
- Challenge-specific dataset discussion: https://github.com/nasa/spaceapps/discussions/2025
- Project Submission Guide: https://www.spaceappschallenge.org/resources/
- [Scientific references in this repository](scientific_references.md)
- [AI assistance disclosure](../AI_USAGE.md)
