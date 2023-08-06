"""Blackcap schedule routes."""


from flask import Blueprint

schedule_bp = Blueprint("schedule", __name__, url_prefix="/v1/schedule")

from blackcap.routes.schedule.get import get  # noqa: F401, E402, I100, E501
from blackcap.routes.schedule.post import post  # noqa: F401, E402, I100, E501
