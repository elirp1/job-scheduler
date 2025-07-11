from datetime import timedelta

class Job:
    def __init__(self, job_id, location, start_time, duration_hours, priority, outdoor=True):
        self.job_id = job_id
        self.location = location
        self.start_time = start_time
        self.duration = timedelta(hours=duration_hours)
        self.priority = priority
        self.outdoor = outdoor

class Crew:
    def __init__(self, crew_id, available_from):
        self.crew_id = crew_id
        self.available_from = available_from

class Scheduler:
    def __init__(self, weather_service):
        self.weather_service = weather_service

    def assign_jobs(self, jobs, crews):
        schedule = []
        sorted_jobs = sorted(jobs, key=lambda j: j.priority)

        for job in sorted_jobs:
            for crew in crews:
                if crew.available_from <= job.start_time:
                    if job.outdoor and self.weather_service.is_bad_weather(job.location, job.start_time):
                        continue

                    schedule.append({
                        'Job ID': job.job_id,
                        'Crew ID': crew.crew_id,
                        'Start': job.start_time,
                        'End': job.start_time + job.duration,
                        'Location': job.location
                    })

                    crew.available_from = job.start_time + job.duration
                    break

        return schedule
