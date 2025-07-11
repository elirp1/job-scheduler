import streamlit as st
import pandas as pd
from datetime import datetime
from scheduler import Job, Crew, Scheduler
from weather import WeatherService
from database import init_db, JobModel
from sqlalchemy.exc import SQLAlchemyError
from plotly import express as px

SessionLocal = init_db()
weather_service = WeatherService(api_key="YOUR_OPENWEATHERMAP_API_KEY")
scheduler = Scheduler(weather_service)

st.set_page_config(page_title="Job & Crew Scheduler", layout="wide")
st.title("🔧 Smart Job & Crew Scheduler")

session = SessionLocal()

# Add job form
st.sidebar.header("📅 Add Jobs")
with st.sidebar.form("job_form"):
    job_id = st.text_input("Job ID")
    location = st.text_input("Location", value="Ocean City")
    start_time = st.text_input("Start DateTime (YYYY-MM-DD HH:MM)", value="2025-07-13 09:00")
    duration = st.number_input("Duration (hours)", min_value=1, max_value=12, value=4)
    priority = st.number_input("Priority (lower = higher priority)", min_value=1, max_value=10, value=1)
    outdoor = st.checkbox("Outdoor Job", value=True)
    submitted = st.form_submit_button("Add Job")

    if submitted:
        try:
            new_job = JobModel(
                job_id=job_id,
                location=location,
                start_time=datetime.strptime(start_time, "%Y-%m-%d %H:%M"),
                duration_hours=duration,
                priority=priority,
                outdoor=outdoor
            )
            session.add(new_job)
            session.commit()
            st.success(f"Job {job_id} added.")
        except SQLAlchemyError as e:
            st.error(f"Error adding job: {e}")

# Crew list (simplified)
crews = [
    Crew(crew_id="Crew A", available_from=datetime(2025, 7, 13, 7)),
    Crew(crew_id="Crew B", available_from=datetime(2025, 7, 13, 7)),
]

# Show jobs and schedule tabs
tab1, tab2, tab3 = st.tabs(["Jobs", "Schedule", "Gantt Chart"])

with tab1:
    jobs = session.query(JobModel).all()
    if jobs:
        job_data = [{
            'Job ID': j.job_id,
            'Location': j.location,
            'Start': j.start_time,
            'Duration (h)': j.duration_hours,
            'Priority': j.priority,
            'Outdoor': j.outdoor
        } for j in jobs]
        st.dataframe(pd.DataFrame(job_data))
    else:
        st.info("No jobs added yet.")

# Run scheduler
if st.button("⏳ Run Scheduler"):
    jobs = session.query(JobModel).all()
    job_objs = [Job(
        job_id=j.job_id,
        location=j.location,
        start_time=j.start_time,
        duration_hours=j.duration_hours,
        priority=j.priority,
        outdoor=j.outdoor
    ) for j in jobs]

    schedule = scheduler.assign_jobs(job_objs, crews)
    df_schedule = pd.DataFrame(schedule)

    with tab2:
        if df_schedule.empty:
            st.warning("No jobs scheduled (likely due to bad weather).")
        else:
            st.success("Schedule generated!")
            st.dataframe(df_schedule)

    with tab3:
        if not df_schedule.empty:
            fig = px.timeline(df_schedule, x_start="Start", x_end="End", y="Crew ID", color="Job ID")
            fig.update_yaxes(autorange="reversed")
            st.plotly_chart(fig)
        else:
            st.info("No Gantt chart to display.")

else:
    with tab2:
        st.info("Run the scheduler to see results.")
    with tab3:
        st.info("Run the scheduler to generate a Gantt chart.")
