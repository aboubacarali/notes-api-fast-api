from pydantic import BaseModel
from datetime import datetime


class NoteSchema(BaseModel):
    title: str
    content: str
    visibiliy: str
    # created_at: datetime
    # updated_at: datetime

    class Config:
        form_attributes = True