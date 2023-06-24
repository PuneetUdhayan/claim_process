from typing import Any
from datetime import datetime

from pydantic import BaseModel, Field


class StandarResponse(BaseModel):
    time: datetime = Field(default_factory=datetime.utcnow)
    status: bool = True
    data: Any
