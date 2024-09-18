import os
import json

def check_cache(job_title: str) -> bool:
    if not os.path.exists('./config/jobs.json'):
        with open("./config/jobs.json", "w") as f:
            f.write("{}")

    with open("./config/jobs.json", "r") as f:
        jobs = json.load(f)

        if job_title in jobs:
            return True

    return False
        
def cache_job(job_title: str, job_description: str):
    if not os.path.exists('./config/jobs.json'):
        with open("./config/jobs.json", "w") as f:
            f.write("{}")

    with open("./config/jobs.json", "r") as f:
        jobs = json.load(f) 

    with open("./config/jobs.json", "w") as f:
        jobs[job_title] = job_description

        json.dump(jobs, f)
