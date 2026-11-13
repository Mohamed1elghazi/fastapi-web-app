# FastAPI Web-App

Eine moderne Webanwendung auf Basis von **FastAPI**, **SQLModel/SQLAlchemy** und einem HTML-Frontend.

## Projektstruktur
- `main_2.py` – Hauptanwendung mit den FastAPI-Routen und API-Endpunkten
- `database.py` – Datenbankverbindung und Tabellenerstellung (SQLite)
- `models.py` – Datenmodelle und Schemas
- `index.html` – Benutzeroberfläche (Frontend)
- `requirements.txt` – Benötigte Python-Pakete

## Installation & Start

1. **Repository klonen:**
   ```bash
   git clone https://github.com
   cd fastapi-web-app
   ```

2. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Server starten:**
   ```bash
   uvicorn main_2:app --reload
   ```
   Die Anwendung ist anschließend unter `http://127.0.0.1:8000` erreichbar.
