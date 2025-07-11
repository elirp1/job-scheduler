from scheduler import Job, Crew, Scheduler
from weather import WeatherService
from datetime import datetime

# Example data
jobs = [
    Job(job_id=1, location="Ocean City", start_time=datetime(2025, 7, 13, 9), duration_hours=4, priority=1),
    Job(job_id=2, location="Salisbury", start_time=datetime(2025, 7, 14, 8), duration_hours=3, priority=2),
]

crews = [
    Crew(crew_id=101, available_from=datetime(2025, 7, 13, 7)),
    Crew(crew_id=102, available_from=datetime(2025, 7, 13, 7)),
]

scheduler = Scheduler(weather_service=WeatherService())
schedule = scheduler.assign_jobs(jobs, crews)

for assignment in schedule:
    print(assignment)
