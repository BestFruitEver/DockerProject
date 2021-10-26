from fastapi import FastAPI, HTTPException, Depends
from typing import List
from pydantic import BaseModel,Field
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.functions import user
from time import sleep
import sqlalchemy
import uvicorn

DATABASE_URL = "mysql+mysqlconnector://{}:{}@{}:{}/{}".format('root', 'example', 'db', '3306', 'project')

metadata = sqlalchemy.MetaData()

user = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("prenom",sqlalchemy.String(500)),
    sqlalchemy.Column("nom",sqlalchemy.String(500))
)

engine = create_engine(
    DATABASE_URL, connect_args={}
)

print('Waiting for database...')
while True:
    try:
        connection = engine.connect()
        break
    except Exception:
        sleep(1.5)
        print("still waiting...")

print('Found database')

metadata.create_all(engine)

app = FastAPI(title="Base RH")

class User(BaseModel):
    id: int
    prenom: str
    nom: str

class UserIn(BaseModel):
    prenom: str
    nom: str

#Chemin de base quand rien n'est spécifié
@app.get("/")
async def hello():
    return {"Hello" : " World"}

#Chemin et fonction pour créer un user
@app.post("/user/", response_model=User)
async def create(u: UserIn):
    query = user.insert().values(
        prenom = u.prenom,
        nom = u.nom
    )
    record_id = connection.execute(query).inserted_primary_key[0]
    query = user.select().where(user.c.id == record_id)
    row = connection.execute(query).fetchone()
    return row

#Sélectionner un user via son ID
@app.get("/user/{id}", response_model=User)
async def get_one(id: int):
    query = user.select().where(user.c.id == id)
    users = connection.execute(query).fetchone()
    return {**users}

#Sélectionner tous les user
@app.get("/user/", response_model=List[User])
async def get_all():
    query = user.select()
    return connection.execute(query).fetchall()

#Mettre à jour les informations d'un user
@app.put("/user/{id}", response_model=User)
async def update(id: int, u: UserIn):
    query = user.update().where(user.c.id == id).values(
        nom = u.nom,
        prenom = u.prenom 
    )
    connection.execute(query)
    query = user.select().where(user.c.id == id)
    row = connection.execute(query).fetchone()
    return {**row}

#Supprimer un user
@app.delete("/user/{id}", response_model=User)
async def delete(id: int):
    query = user.delete().where(user.c.id == id)
    connection.execute(query)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)