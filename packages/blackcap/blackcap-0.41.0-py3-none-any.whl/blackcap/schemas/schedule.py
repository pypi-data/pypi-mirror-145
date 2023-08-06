"""Schedule schema."""

from typing import Optional

from pydantic import BaseModel
from pydantic.types import UUID4

from blackcap.schemas.job import Job


class Schedule(BaseModel):
    """Schedule schema."""

    schedule_id: UUID4
    job_id: UUID4
    job: Optional[Job]
    assigned_cluster_id: UUID4
    messenger: str
    messenger_queue: str
    status: str = "PENDING"
    logs: str = ""
