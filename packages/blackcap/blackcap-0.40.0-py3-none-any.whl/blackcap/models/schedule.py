"""Schedule DBModel."""

from sqlalchemy import Column, DateTime, String

from blackcap.models.meta.mixins import (
    DBModel,
    SurrogatePKUUID,
    TimestampMixin,
)
from blackcap.models.meta.orm import reference_col


class ScheduleDB(DBModel, TimestampMixin, SurrogatePKUUID):
    """Schedule table."""

    __tablename__ = "schedule"
    job_id = reference_col("job")
    assigned_cluster_id = reference_col("cluster")
    messenger = Column(String, nullable=False, default="GCP")
    messenger_queue = Column(String, nullable=False, default="main")
    # TODO: this should be an Enum with the possible status values
    status = Column(String, nullable=False, default="PENDING")
    logs = Column(String, default="")
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    protagonist_id = reference_col("protagonist")
