from sqlmodel import Field, SQLModel
from typing import Optional


class HallOfFameEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contexte: str
    reponse: str
    score: int = Field(index=True)
