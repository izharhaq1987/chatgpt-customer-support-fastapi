import uuid

def new_job_id() -> str:
    return str(uuid.uuid4())
