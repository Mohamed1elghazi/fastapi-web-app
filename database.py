from sqlmodel import Session, SQLModel, create_engine

#DATABASE_URL = "postgresql+psycopg://admin:geheim@localhost:5432/eintraege_db"
# Für schnellen Test ohne PostgreSQL-Server:
DATABASE_URL = "sqlite:///datenbank.db"

#engine = create_engine(DATABASE_URL, echo=True)


engine = create_engine(
    DATABASE_URL, 
    echo=True, 
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
