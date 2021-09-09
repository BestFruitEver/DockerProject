from fastapi import FastAPI, HTTPException, Depends
from typing import List
from pydantic import BaseModel,Field
from sqlalchemy.sql.functions import user
import databases
import sqlalchemy

DATABASE_URL ="sqlite:///./user.db"

metadata = sqlalchemy.MetaData()

database = databases.Database(DATABASE_URL)

user = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("prenom",sqlalchemy.String(500)),
    sqlalchemy.Column("nom",sqlalchemy.String(500))
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)

app = FastAPI(title="Base RH")

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

class User(BaseModel):
    id: int
    prenom: str
    nom: str

class UserIn(BaseModel):
    prenom: str = Field(...)
    nom: str = Field(...)

@app.post("/create/", response_model=User)
async def create(u: UserIn = Depends()):
    query = user.insert().values(
        prenom = u.prenom,
        nom = u.nom
    )
    record_id = await database.execute(query)
    query = user.select().where(user.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@app.get("/user/{id}", response_model=User)
async def get_one(id: int):
    query = user.select().where(user.c.id == id)
    users = await database.fetch_one(query)
    return {**users}

@app.get("/user/", response_model=List[User])
async def get_all():
    query = user.select()
    all_get = await database.fetch_all(query)
    return all_get

@app.put("/update/{id}", response_model=User)
async def update(id: int, u: UserIn = Depends()):
    query = user.update().where(user.c.id == id).values(
        nom = u.nom,
        prenom = u.prenom 
    )
    record_id = await database.execute(query)
    query = user.select().where(user.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@app.delete("/delete/{id}", response_model=User)
async def delete(id: int):
    query = user.delete().where(user.c.id == id)
    await database.execute(query)