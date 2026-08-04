import streamlit as st
import requests
import json
import time

# --- Configuration ---
st.set_page_config(
    page_title="SAP CPI Auto-Recovery Agent",
    page_icon="🤖",
    layout="wide"
)

# Backend API URL (FastAPI)
API_URL = "http://127.0.0.1:8000/analyze-log"

# --- Header & Styling ---
st.title("🤖 SAP CPI Autonomous Recovery Agent")
st.markdown("Automated root-cause analysis and payload correction for SAP Integration Suite.")

# Top-level metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Monitored iFlows", "14 Active")
col2.metric("Failed Messages (24h)", "3")
col3.metric("Auto-Recovered", "2")
col4.metric("Avg MTTR", "5.2s", delta="-42m", delta_color="inverse")
st.divider()

# ==========================================================
# --- Main Dashboard ---
# ==========================================================

st.subheader("📡 Live SAP Message Processing Logs (OData Monitor)")

# Fetch logs dynamically from the FastAPI backend
@st.cache_data(ttl=5)  # Cache for 5 seconds
def get_live_logs():
    try:
        response = requests.get("http://127.0.0.1:8000/api/fetch-logs")

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch logs: {response.text}")
            return []

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to FastAPI backend. Is uvicorn running?")
        return []


# Load logs
failed_logs = get_live_logs()

# Stop app if no logs available
if not failed_logs:
    st.warning("Waiting for connection to SAP CPI OData API...")
    st.stop()

# Select a log
selected_log_name = st.selectbox(
    "Select a failed Message Processing Log (MPL) to diagnose:",
    options=[
        f"{log['log_id']} - {log['integration_flow_name']}"
        for log in failed_logs
    ]
)

# Get selected log
selected_log = next(
    log for log in failed_logs
    if log["log_id"] in selected_log_name
)

# Display error
st.error(f"**🔴 SAP Trace Error:** {selected_log['error_message']}")

# Display payload
with st.expander("View Raw Incoming Payload", expanded=True):
    if selected_log["raw_payload"].startswith("<"):
        st.code(selected_log["raw_payload"], language="xml")
    else:
        st.code(selected_log["raw_payload"], language="json")

# ==========================================================
# --- Action Area ---
# ==========================================================

if st.button("🚀 Run AI Root-Cause Analysis & Recovery", type="primary"):

    with st.spinner("Connecting to FastAPI backend... Routing broken payload to LangChain..."):

        try:
            response = requests.post(API_URL, json=selected_log)

            if response.status_code == 200:

                result = response.json()

                st.success("Analysis Complete! Payload corrected.")

                st.info(
                    f"**🧠 AI Root Cause Analysis:**\n"
                    f"{result['root_cause_explanation']}"
                )

                st.markdown("### 🔄 Payload Diff Comparison")

                diff_col1, diff_col2 = st.columns(2)

                with diff_col1:
                    st.markdown("**Original (Failed)**")

                    if selected_log["raw_payload"].startswith("<"):
                        st.code(selected_log["raw_payload"], language="xml")
                    else:
                        st.code(selected_log["raw_payload"], language="json")

                with diff_col2:
                    st.markdown(
                        f"**Corrected (Auto-Fixed)** - Confidence: "
                        f"{result['confidence_score']*100:.1f}%"
                    )

                    if result["corrected_payload"].startswith("<"):
                        st.code(result["corrected_payload"], language="xml")
                    else:
                        st.code(result["corrected_payload"], language="json")

                st.button(
                    "✅ Approve & Re-trigger in SAP CPI",
                    type="secondary"
                )

            else:
                st.error(
                    f"Backend Error: {response.status_code} - {response.text}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Could not connect to FastAPI backend. "
                "Make sure uvicorn is running on http://127.0.0.1:8000"
            )

            # Demo fallback
            st.warning(
                "⚠️ Showing mock response for demonstration because backend is down."
            )

            time.sleep(1)

            st.info(
                "**🧠 AI Root Cause Analysis:** (Mock)\n"
                "Detected schema error. Fixed date format and added closing tag."
            )

            st.code(
                "<Order><Header><OrderID>100234</OrderID>"
                "<OrderDate>2026-12-31</OrderDate></Header>"
                "<Item><MaterialID>MAT-901</MaterialID>"
                "<Quantity>500</Quantity></Item></Order>",
                language="xml",
            )