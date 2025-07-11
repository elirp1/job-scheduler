import streamlit as st
import pandas as pd
from datetime import datetime
from scheduler import Job, Crew, Scheduler
from weather import WeatherService

st.set_page_config(page_title="Job & Crew Scheduler", layout="wide")
st.title("🛠️ Smart Job & Crew Scheduler")

# Weather service and scheduler
weather_service = WeatherService()
scheduler = Scheduler(weather_service=weather_service)

# Sample input forms
st.sidebar.header("📅 Add Jobs")
jobs = []
if 'jobs' not in st.session_state:
    st.session_state.jobs = []

with st.sidebar.form("job_form"):
    job_id = st.text_input("Job ID")
    location = st.text_input("Location", value="Ocean City")
    start_time = st.text_input("Start DateTime (YYYY-MM-DD HH:MM)", value="2025-07-13 09:00")
    duration = st.number_input("Duration (hours)", min_value=1, max_value=12, value=4)
    priority = st.number_input("Priority (lower = higher priority)", min_value=1, max_value=10, value=1)
    outdoor = st.checkbox("Outdoor Job", value=True)

    submitted = st.form_submit_button("Add Job")
    if submitted:
        st.session_state.jobs.append(Job(
            job_id=job_id,
            location=location,
            start_time=datetime.strptime(start_time, "%Y-%m-%d %H:%M"),
            duration_hours=duration,
            priority=priority,
            outdoor=outdoor
        ))

# Crew list (simplified for MVP)
crews = [
    Crew(crew_id="Crew A", available_from=datetime(2025, 7, 13, 7)),
    Crew(crew_id="Crew B", available_from=datetime(2025, 7, 13, 7)),
]

# Display current jobs
tab1, tab2 = st.tabs(["Jobs", "Schedule"])

with tab1:
    if st.session_state.jobs:
        job_data = [{
            'Job ID': j.job_id,
            'Location': j.location,
            'Start': j.start_time,
            'Duration (h)': j.duration.total_seconds() / 3600,
            'Priority': j.priority,
            'Outdoor': j.outdoor
        } for j in st.session_state.jobs]
        st.dataframe(pd.DataFrame(job_data))
    else:
        st.info("No jobs added yet.")

# Run scheduler
if st.button("⏳ Run Scheduler"):
    schedule = scheduler.assign_jobs(st.session_state.jobs, crews)
    df_schedule = pd.DataFrame(schedule)

    with tab2:
        if df_schedule.empty:
            st.warning("No jobs scheduled (likely due to bad weather).")
        else:
            st.success("Schedule generated!")
            st.dataframe(df_schedule)
else:
    with tab2:
        st.info("Run the scheduler to see results.")
