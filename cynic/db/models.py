from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional


class HallOfFameEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contexte: str
    reponse: str
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    score: int = Field(index=True)
