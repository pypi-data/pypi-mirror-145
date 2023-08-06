"""Blackcap Schedule PUT route schemas."""

from typing import Any, Dict, List, Union, Optional

from pydantic import BaseModel
from pydantic.types import UUID4

from blackcap.schemas.schedule import Schedule


class ScheduleUpdate(BaseModel):
    """Schema to parse update schedule requests."""

    schedule_id: UUID4
    protagonist_id: UUID4
    status: Optional[str]
    logs: Optional[str]


class SchedulePUTRequest(BaseModel):
    """Schedule PUT request schema."""

    schedule_list: List[ScheduleUpdate]


class SchedulePUTResponse(BaseModel):
    """Schedule PUT response schema."""

    items: Dict[str, List[Union[Schedule, Any]]] = {}
