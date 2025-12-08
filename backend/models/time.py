from pydantic import BaseModel, Field
from datetime import datetime

class TimeEntry(BaseModel):
    project_name: str
    description: str
    hours: float
    entry_date: str = Field(default=datetime.now().strftime("%Y-%m-%d"))