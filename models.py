from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

class EintragBasis(SQLModel):
    name: str
    email: EmailStr
    alter: int = Field(gt=0, le=120)
    nachricht: str

class Eintrag(EintragBasis, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class EintragEingabe(EintragBasis):
    pass

class EintragAusgabe(EintragBasis):
    id: int




