from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

# 1. Define a standard model
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

# 2. CRITICAL MISTAKE: Creating an in-memory DB without StaticPool
# This engine will drop and recreate connections for different operations.
sqlite_url = "sqlite:///:memory:"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

# 3. Connection #1 opens, creates the table 'hero', and then CLOSES.
# The moment this connection closes, SQLite wipes the entire database out of RAM.
SQLModel.metadata.create_all(engine)

# 4. Connection #2 opens. It is a completely empty, fresh database.
with Session(engine) as session:
    hero = Hero(name="Deadpond")
    session.add(hero)
    
    # ❌ CRASHES HERE! 
    # sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: hero
    session.commit() 
    
with Session(engine) as session:
    statement = select(Hero)
    results = session.exec(statement)
    for hero in results:
        print(hero)
        
print("Your current pool class is:", engine.pool.__class__.__name__)
