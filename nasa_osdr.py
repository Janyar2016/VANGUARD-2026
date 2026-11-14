"""NASA OSDR retrospective analytics for ASTRA HEALTH.

Uses the public, processed OSD-575 Inspiration4 serum CMP file.
The analysis is descriptive and source-traceable; it is not clinical decision support.
"""
from __future__ import annotations

from io import BytesIO
import re
from typing import Any

import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

OSDR_STUDY_URL = "https://osdr.nasa.gov/bio/repo/data/studies/OSD-575"
OSDR_DOWNLOAD_URL = "https://osdr.nasa.gov/geode-py/ws/studies/OSD-575/download"
OSDR_FILE = "LSDS-8_Comprehensive_Metabolic_Panel_CMP_TRANSFORMED.csv"

VISIT_ORDER = ["L-92", "L-44", "L-3", "R+1", "R+45", "R+82", "R+194"]
VISIT_LABELS = {
    "L-92": "92 days before launch",
    "L-44": "44 days before launch",
    "L-3": "3 days before launch",
    "R+1": "1 day after return",
    "R+45": "45 days after return",
    "R+82": "82 days after return",
    "R+194": "194 days after return",
}


@st.cache_data(ttl=21600, show_spinner=False)
def load_osdr_575() -> pd.DataFrame:
    """Fetch the public processed CSV from NASA OSDR."""
    response = requests.get(
        OSDR_DOWNLOAD_URL,
        params={"source": "datamanager", "file": OSDR_FILE},
        timeout=45,
        headers={"User-Agent": "ASTRA-HEALTH-NASA-OSDR-Analytics/2.0"},
    )
    response.raise_for_status()
    body = response.content
    if "text/html" in response.headers.get("content-type", "").lower():
        raise ValueError("NASA returned HTML instead of the requested CSV.")
    frame = pd.read_csv(BytesIO(body), encoding="utf-8-sig")
    if frame.empty or len(frame.columns) < 3:
        raise ValueError("The downloaded NASA file is empty or has an unexpected structure.")
    return frame


def _normal(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value).casefold())


def _sample_column(frame: pd.DataFrame) -> str | None:
    for col in frame.columns:
        key = _normal(col)
        if key in {"samplename", "sample"}:
            return str(col)
    for col in frame.columns:
        key = _normal(col)
        if "sample" in key and "name" in key:
            return str(col)
    return None


def _parse_sample(value: Any) -> tuple[str | None, str | None]:
    """Extract anonymised crew code and collection visit from OSDR sample label."""
    label = str(value).strip().upper()
    subject = re.search(r"(?<![A-Z0-9])(C\d{3})(?![A-Z0-9])", label)
    visit = re.search(r"(?<![A-Z0-9])(L-\d+|R\+\d+)(?![A-Z0-9])", label)
    return (
        subject.group(1) if subject else None,
        visit.group(1) if visit else None,
    )


def build_analysis(frame: pd.DataFrame) -> tuple[pd.DataFrame, list[str], str]:
    """Convert the wide OSDR table into a tidy, auditable sample/marker table."""
    sample_col = _sample_column(frame)
    if sample_col is None:
        raise ValueError(
            "Could not identify the OSDR sample-name column. "
            "Available columns: " + ", ".join(map(str, frame.columns[:18]))
        )

    value_cols = [
        str(c) for c in frame.columns
        if re.search(r"_value_", str(c), flags=re.IGNORECASE)
    ]
    if not value_cols:
        raise ValueError("No measurement columns matching the OSDR '*_value_*' pattern were found.")

    records: list[dict[str, Any]] = []
    for _, row in frame.iterrows():
        subject, visit = _parse_sample(row.get(sample_col))
        if subject is None or visit is None:
            continue
        for value_col in value_cols:
            match = re.match(r"(.+?)_value_(.+)$", value_col, flags=re.IGNORECASE)
            if not match:
                continue
            marker, unit = match.group(1), match.group(2)
            value = pd.to_numeric(pd.Series([row.get(value_col)]), errors="coerce").iloc[0]
            if pd.isna(value):
                continue
            min_col = f"{marker}_range_min_{unit}"
            max_col = f"{marker}_range_max_{unit}"
            lower = pd.to_numeric(pd.Series([row.get(min_col)]), errors="coerce").iloc[0] if min_col in frame.columns else float("nan")
            upper = pd.to_numeric(pd.Series([row.get(max_col)]), errors="coerce").iloc[0] if max_col in frame.columns else float("nan")
            records.append({
                "subject": subject,
                "visit": visit,
                "marker": marker.replace("_", " "),
                "unit": unit,
                "value": float(value),
                "range_min": float(lower) if pd.notna(lower) else None,
                "range_max": float(upper) if pd.notna(upper) else None,
                "sample_name": str(row.get(sample_col)),
                "value_column": value_col,
            })

    tidy = pd.DataFrame(records)
    if tidy.empty:
        raise ValueError(
            "Sample labels were found, but no numeric biomarker values could be parsed. "
            "Please check the OSDR column naming."
        )

    tidy["visit_order"] = tidy["visit"].map({v: i for i, v in enumerate(VISIT_ORDER)}).fillna(99)
    tidy["phase"] = tidy["visit"].map(
        lambda v: "Pre-flight" if str(v).startswith("L-") else "Post-flight"
    )
    tidy["range_status"] = "Range unavailable"
    has_range = tidy["range_min"].notna() & tidy["range_max"].notna()
    tidy.loc[has_range & (tidy["value"] < tidy["range_min"]), "range_status"] = "Below source range"
    tidy.loc[has_range & (tidy["value"] > tidy["range_max"]), "range_status"] = "Above source range"
    tidy.loc[has_range & tidy["value"].between(tidy["range_min"], tidy["range_max"]), "range_status"] = "Within source range"

    # Each crew member's baseline is the mean of their available pre-flight samples.
    baseline = (
        tidy[tidy["phase"] == "Pre-flight"]
        .groupby(["subject", "marker", "unit"], as_index=False)["value"]
        .mean()
        .rename(columns={"value": "preflight_mean"})
    )
    tidy = tidy.merge(baseline, on=["subject", "marker", "unit"], how="left")
    tidy["delta_from_preflight"] = tidy["value"] - tidy["preflight_mean"]
    tidy["pct_change_from_preflight"] = (
        tidy["delta_from_preflight"] / tidy["preflight_mean"].where(tidy["preflight_mean"] != 0)
    ) * 100
    return tidy.sort_values(["subject", "visit_order", "marker"]).reset_index(drop=True), value_cols, sample_col


def _chart_layout(fig: go.Figure, height: int = 390) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=12, r=12, t=28, b=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dce8f4"),
        legend=dict(orientation="h", y=1.12, x=0),
        hoverlabel=dict(bgcolor="#102238", font_color="#f4f8fc"),
    )
    fig.update_xaxes(gridcolor="rgba(130,160,190,.16)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(130,160,190,.16)", zeroline=False)
    return fig


def _fmt(value: Any, digits: int = 3) -> str:
    return "—" if pd.isna(value) else f"{float(value):,.{digits}f}"


def page_nasa_osdr() -> None:
    st.title("NASA OSDR · Spaceflight Health Analytics")
    st.caption("ASTRA HEALTH  /  INSPIRATION4  /  OSD-575")

    st.markdown(
        """
        Explore how published serum measurements changed across the Inspiration4
        collection timeline. ASTRA HEALTH calculates a **personal pre-flight reference**
        for each anonymised crew code, compares later samples with that reference,
        and keeps the source-provided laboratory ranges visible.
        """
    )
    st.info(
        "Research boundary: OSD-575 contains retrospective samples from four crew members. "
        "It is not live telemetry, a representative astronaut reference cohort, a diagnostic "
        "tool, or a validated alert system. Comparisons describe this dataset only."
    )

    with st.spinner("Retrieving the public OSD-575 dataset from NASA..."):
        try:
            raw = load_osdr_575()
            data, value_cols, sample_col = build_analysis(raw)
        except Exception as exc:
            st.error("NASA OSDR data could not be loaded or interpreted.")
            st.caption(f"Technical detail: {type(exc).__name__}: {exc}")
            st.markdown(f"[Open the official OSD-575 study]({OSDR_STUDY_URL})")
            return

    subjects = sorted(data["subject"].dropna().unique().tolist())
    markers = sorted(data["marker"].dropna().unique().tolist())
    visits = [v for v in VISIT_ORDER if v in data["visit"].unique()]
    post_visits = [v for v in VISIT_ORDER if v.startswith("R+") and v in visits]

    a, b, c, d = st.columns(4)
    a.metric("Samples parsed", f"{data['sample_name'].nunique():,}")
    b.metric("Crew codes", f"{len(subjects)}")
    c.metric("Biomarkers with values", f"{len(markers)}")
    d.metric("Post-flight visits", f"{len(post_visits)}")

    st.divider()
    overview_tab, trend_tab, compare_tab, raw_tab = st.tabs(
        ["Overview", "Biomarker timeline", "Change analysis", "Source data"]
    )

    with overview_tab:
        st.subheader("Collection timeline")
        timeline = go.Figure()
        for phase, color in [("Pre-flight", "#58b7ff"), ("Post-flight", "#52d6b0")]:
            part = data[data["phase"] == phase][["subject", "visit", "visit_order"]].drop_duplicates()
            if not part.empty:
                timeline.add_trace(go.Scatter(
                    x=part["visit_order"], y=part["subject"], mode="markers",
                    marker=dict(size=13, color=color, symbol="circle"),
                    name=phase, text=part["visit"],
                    hovertemplate="%{y} · %{text}<extra></extra>",
                ))
        timeline.update_layout(
            xaxis=dict(
                tickmode="array",
                tickvals=list(range(len(VISIT_ORDER))),
                ticktext=VISIT_ORDER,
                title="Sample collection visit",
            ),
            yaxis_title="Anonymised crew code",
        )
        _chart_layout(timeline, 270)
        st.plotly_chart(timeline, use_container_width=True)
        st.caption(
            "Each point represents a sample visit. L− visits are before launch; R+ visits are after return. "
            "No continuous in-flight measurements are represented in this CMP file."
        )

        st.subheader("What this analysis computes")
        left, right = st.columns(2)
        with left:
            st.markdown(
                """
                **Personal pre-flight reference**

                For each crew code and biomarker, the app averages the available
                L−92, L−44 and L−3 measurements. It does not pool different people
                into one baseline.
                """
            )
        with right:
            st.markdown(
                """
                **Traceable comparison**

                Each later sample is compared with that person's own pre-flight
                mean. The source's sample-specific lower and upper ranges are shown
                separately from the personal comparison.
                """
            )

    with trend_tab:
        st.subheader("Explore one biomarker over time")
        left, right = st.columns([1, 1])
        with left:
            subject_choice = st.selectbox("Crew member", subjects, key="osdr_trend_subject")
        with right:
            marker_choice = st.selectbox("Biomarker", markers, key="osdr_trend_marker")
        part = data[(data["subject"] == subject_choice) & (data["marker"] == marker_choice)].sort_values("visit_order")
        if part.empty:
            st.warning("No values are available for this selection.")
        else:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=part["visit"], y=part["value"], mode="lines+markers",
                name="Measured value", line=dict(color="#55d6c2", width=3),
                marker=dict(size=9),
                error_y=dict(
                    type="data",
                    symmetric=False,
                    array=(part["range_max"] - part["value"]).clip(lower=0).fillna(0),
                    arrayminus=(part["value"] - part["range_min"]).clip(lower=0).fillna(0),
                    color="#8da9c4",
                    thickness=1.2,
                    width=5,
                ),
                customdata=part[["phase", "range_status", "sample_name"]].to_numpy(),
                hovertemplate=(
                    "%{x}<br>Value: %{y:.4g}<br>%{customdata[0]}"
                    "<br>%{customdata[1]}<br>%{customdata[2]}<extra></extra>"
                ),
            ))
            baseline_value = part["preflight_mean"].dropna()
            if not baseline_value.empty:
                fig.add_hline(
                    y=float(baseline_value.iloc[0]),
                    line_dash="dash", line_color="#f4bd62",
                    annotation_text="Personal pre-flight mean",
                )
            fig.update_layout(
                xaxis=dict(categoryorder="array", categoryarray=VISIT_ORDER, title="Collection visit"),
                yaxis_title=f"{marker_choice} ({part['unit'].iloc[0]})",
            )
            _chart_layout(fig, 410)
            st.plotly_chart(fig, use_container_width=True)
            st.caption(
                "Whiskers show the source-provided range for each sample when both bounds are available. "
                "The dashed line is this crew member's pre-flight mean, not a clinical threshold."
            )
            display = part[[
                "visit", "phase", "value", "unit", "preflight_mean",
                "delta_from_preflight", "pct_change_from_preflight", "range_min",
                "range_max", "range_status",
            ]].copy()
            st.dataframe(display, hide_index=True, use_container_width=True)

    with compare_tab:
        st.subheader("Retrospective change analysis")
        if not post_visits:
            st.info("No post-flight collection visits were parsed from this file.")
        else:
            left, right = st.columns(2)
            with left:
                compare_subject = st.selectbox("Crew member", subjects, key="osdr_compare_subject")
            with right:
                compare_visit = st.selectbox(
                    "Recovery visit",
                    post_visits,
                    index=len(post_visits) - 1,
                    format_func=lambda v: f"{v} · {VISIT_LABELS.get(v, v)}",
                    key="osdr_compare_visit",
                )

            selected = data[
                (data["subject"] == compare_subject)
                & (data["visit"] == compare_visit)
                & data["preflight_mean"].notna()
            ].copy()
            selected["absolute_pct_change"] = selected["pct_change_from_preflight"].abs()
            selected = selected.sort_values("absolute_pct_change", ascending=False)

            if selected.empty:
                st.warning("No comparable numeric measurements were found for this crew member and visit.")
            else:
                changed = selected.iloc[0]
                m1, m2, m3 = st.columns(3)
                m1.metric("Measurements compared", f"{len(selected)}")
                m2.metric("Largest absolute change", f"{abs(changed['pct_change_from_preflight']):.1f}%")
                m3.metric("Visit", compare_visit)
                st.caption(
                    "The largest change is a descriptive ranking by absolute percentage difference "
                    "from the personal pre-flight mean. It is not a severity or risk score."
                )

                fig = go.Figure()
                colors = [
                    "#55d6c2" if x >= 0 else "#f4bd62"
                    for x in selected["pct_change_from_preflight"].fillna(0)
                ]
                fig.add_trace(go.Bar(
                    x=selected["pct_change_from_preflight"],
                    y=selected["marker"],
                    orientation="h",
                    marker_color=colors,
                    customdata=selected[["value", "preflight_mean", "unit", "range_status"]].to_numpy(),
                    hovertemplate=(
                        "%{y}<br>Change: %{x:.2f}%"
                        "<br>Measured: %{customdata[0]:.4g} %{customdata[2]}"
                        "<br>Pre-flight mean: %{customdata[1]:.4g}"
                        "<br>%{customdata[3]}<extra></extra>"
                    ),
                ))
                fig.add_vline(x=0, line_color="#9db0c3", line_width=1)
                fig.update_layout(
                    xaxis_title="Difference from personal pre-flight mean (%)",
                    yaxis_title="",
                    yaxis=dict(autorange="reversed"),
                )
                _chart_layout(fig, max(340, min(650, 26 * len(selected) + 110)))
                st.plotly_chart(fig, use_container_width=True)

                table = selected[[
                    "marker", "value", "unit", "preflight_mean",
                    "delta_from_preflight", "pct_change_from_preflight",
                    "range_min", "range_max", "range_status", "sample_name",
                ]].copy()
                st.dataframe(table, hide_index=True, use_container_width=True)
                st.download_button(
                    "Download this comparison (CSV)",
                    data=table.to_csv(index=False).encode("utf-8"),
                    file_name=f"OSD575_{compare_subject}_{compare_visit}_comparison.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

    with raw_tab:
        st.subheader("Original NASA table")
        st.caption(
            "The original processed table is preserved below for transparency. "
            "The analysis above is derived from these source rows."
        )
        st.dataframe(raw, hide_index=True, use_container_width=True)
        st.download_button(
            "Download original NASA CSV",
            data=raw.to_csv(index=False).encode("utf-8"),
            file_name="NASA_OSDR_OSD-575_Inspiration4_CMP.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.divider()
    st.subheader("Data provenance")
    st.markdown(
        f"""
        - **Study:** [OSD-575 — Inspiration4 blood-serum metabolic and immune/cardiac assays]({OSDR_STUDY_URL})
        - **Repository:** [NASA Open Science Data Repository](https://osdr.nasa.gov/)
        - **DOI:** [10.26030/mc5d-p710](https://doi.org/10.26030/mc5d-p710)
        - **Source file:** `{OSDR_FILE}`
        - **Sample identifier field detected:** `{sample_col}`
        """
    )
    st.caption(
        "Method: per-person mean of available pre-flight visits (L−92, L−44, L−3); "
        "post-flight difference = measured value − personal pre-flight mean; "
        "percentage difference = difference ÷ pre-flight mean × 100. "
        "Missing values are omitted, not imputed. Source ranges are displayed as supplied."
    )
