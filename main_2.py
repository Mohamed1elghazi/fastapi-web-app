import os
import uvicorn
from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Security, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from sqlmodel import Session, select



# Sauberer Import aus deinen eigenen Dateien
from database import create_db_and_tables, get_session
from models import Eintrag, EintragEingabe, EintragAusgabe
from fastapi.responses import FileResponse


@asynccontextmanager 
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="FastAPI Web-App Praxis-Guide", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "123"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def check_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ungültiger API-Key")
    return api_key

@app.post("/api/eintraege", response_model=EintragAusgabe, status_code=status.HTTP_201_CREATED)
def eintrag_erstellen(eintrag: EintragEingabe, session: Session = Depends(get_session), api_key: str = Depends(check_api_key)):
    db_eintrag = Eintrag.model_validate(eintrag)
    session.add(db_eintrag)
    session.commit()
    session.refresh(db_eintrag)
    return db_eintrag



@app.get("/")
def startseite():
    return FileResponse("index.html")

@app.get("/api/eintraege", response_model=List[EintragAusgabe])
def eintraege_abrufen(session: Session = Depends(get_session), api_key: str = Depends(check_api_key)):
    return session.exec(select(Eintrag)).all()


@app.put("/api/eintraege/{eintrag_id}", response_model=EintragAusgabe)
def eintrag_aktualisieren(eintrag_id: int, neue_daten: EintragEingabe, session: Session = Depends(get_session), api_key: str = Depends(check_api_key)):
    db_eintrag = session.get(Eintrag, eintrag_id)
    if not db_eintrag:
        raise HTTPException(status_code=404, detail="Eintrag nicht gefunden")
    for key, value in neue_daten.model_dump().items():
        setattr(db_eintrag, key, value)
    session.add(db_eintrag)
    session.commit()
    session.refresh(db_eintrag)
    return db_eintrag

@app.delete("/api/eintraege/{eintrag_id}", status_code=status.HTTP_204_NO_CONTENT)
def eintrag_loeschen(eintrag_id: int, session: Session = Depends(get_session), api_key: str = Depends(check_api_key)):
    db_eintrag = session.get(Eintrag, eintrag_id)
    if not db_eintrag:
        raise HTTPException(status_code=404, detail="Eintrag nicht gefunden")
    session.delete(db_eintrag)
    session.commit()
    return None

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    dateiname = os.path.splitext(os.path.basename(__file__))[0]
    uvicorn.run(f"{dateiname}:app", host="127.0.0.1", port=8000, reload=True)
