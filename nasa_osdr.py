"""NASA OSDR public research-data explorer for ASTRA HEALTH.

Downloads the public, processed OSD-575 Comprehensive Metabolic Panel CSV.
This is research data from the Inspiration4 mission, not live telemetry.
"""
from __future__ import annotations

from io import BytesIO

import pandas as pd
import requests
import streamlit as st

OSDR_STUDY_URL = "https://osdr.nasa.gov/bio/repo/data/studies/OSD-575"
OSDR_DOWNLOAD_URL = "https://osdr.nasa.gov/geode-py/ws/studies/OSD-575/download"
OSDR_FILE = "LSDS-8_Comprehensive_Metabolic_Panel_CMP_TRANSFORMED.csv"


@st.cache_data(ttl=21600, show_spinner=False)
def load_osdr_575() -> pd.DataFrame:
    """Fetch the public processed CSV from NASA OSDR and parse it."""
    response = requests.get(
        OSDR_DOWNLOAD_URL,
        params={"source": "datamanager", "file": OSDR_FILE},
        timeout=45,
        headers={"User-Agent": "ASTRA-HEALTH-NASA-OSDR-Explorer/1.0"},
    )
    response.raise_for_status()
    content_type = response.headers.get("content-type", "").lower()
    if "text/html" in content_type or response.content.lstrip().lower().startswith(b"<!doctype html"):
        raise ValueError("NASA OSDR returned a web page instead of the requested CSV file.")
    frame = pd.read_csv(BytesIO(response.content))
    if frame.empty or len(frame.columns) < 2:
        raise ValueError("The downloaded NASA file did not contain the expected tabular data.")
    return frame


def page_nasa_osdr() -> None:
    st.title("NASA OSDR · Inspiration4 Research Data")
    st.caption("ASTRA HEALTH / NASA OPEN SCIENCE DATA REPOSITORY")

    st.markdown(
        """
        This page connects ASTRA HEALTH to NASA's **OSD-575** public, processed
        blood-serum research dataset from the Inspiration4 mission. The study
        includes pre-flight and post-flight samples and reports comprehensive
        metabolic-panel measurements. It is research data—not continuous,
        real-time astronaut vital signs.
        """
    )

    st.info(
        "Scientific-use boundary: these measurements come from a small, four-person "
        "commercial spaceflight study. They are not universal astronaut reference "
        "ranges, clinical advice, or validated alert thresholds. ASTRA HEALTH does "
        "not use them to diagnose people or make flight decisions."
    )

    with st.spinner("Connecting to NASA OSDR and loading the public OSD-575 file..."):
        try:
            df = load_osdr_575()
        except Exception as exc:
            st.error(
                "The NASA OSDR file could not be loaded right now. Check the internet "
                "connection and try again. The rest of ASTRA HEALTH remains available."
            )
            st.caption(f"Technical detail: {type(exc).__name__}: {exc}")
            st.markdown(f"[Open the OSD-575 study page]({OSDR_STUDY_URL})")
            return

    c1, c2, c3 = st.columns(3)
    c1.metric("Research records", f"{len(df):,}")
    c2.metric("Data fields", f"{len(df.columns):,}")
    c3.metric("Source", "NASA OSDR · OSD-575")

    st.subheader("Research dataset")
    st.write(
        "The table below displays the processed NASA data as published by OSDR. "
        "Column names and units are retained from the source file."
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        st.subheader("Descriptive statistics")
        st.caption(
            "Summary statistics for numeric columns in the downloaded research file. "
            "These are descriptive summaries only; no clinical interpretation is made."
        )
        st.dataframe(numeric.describe().T, use_container_width=True)

    st.download_button(
        "Download the loaded NASA dataset (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="NASA_OSDR_OSD-575_Inspiration4_CMP.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown("### Dataset citation and access")
    st.markdown(
        f"""
        - **NASA study:** [OSD-575 — SpaceX Inspiration4 Blood Serum Metabolic Panel
          and Immune/Cardiac Cytokine Arrays]({OSDR_STUDY_URL})
        - **Repository:** [NASA Open Science Data Repository](https://osdr.nasa.gov/)
        - **Study DOI:** [10.26030/mc5d-p710](https://doi.org/10.26030/mc5d-p710)
        - **License shown on the study page:** CC0-1.0
        - **Data file:** `{OSDR_FILE}`
        """
    )
    st.caption(
        "The dataset contains research samples collected at defined time points "
        "around a short mission. It must not be presented as live in-flight monitoring "
        "or as representative of every astronaut."
    )
