from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import User, User_Pydantic, UserIn_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundErrorn, register_tortoise
from typing import List


app = FastAPI(title="Base RH")

class Messa(BaseModel)


list_user= []


@app.get("/")
async def hello_world():
    return {"hello" : "world"}


#crud : create, read, update delete

#read
@app.get("/users/", response_model=List[User])
async def get_all_users():
    #on récupère la liste de tous les utilisateurs
    return list_user

#read
@app.get("/user/{id}")
async def get_user(id: int):
    #On récupère un utilisateur en fonction de son ID et on renvoie une 404 s'il n'est pas trouver dans la DB
    try:
        return list_user[id]
    except:
        raise HTTPException(status_code=404, detail="User not found in DB")

#create
@app.post("/create/")
async def add_user(user: User):
    #On créer dans la liste user un nouvel utilisateur
    list_user.append(user)
    return user

#update
@app.put("/update/{id}")
async def update_user(id: int, new_user: User):
    #On récupère les informations d'un utilisateur en fonction de son id et on lui entre de nouvelles valeurs avant de le réinjecter dans la liste.
    #On renvoi une 404 s'il n'est pas trouver dans la DB
    try:
        list_user[id] = new_user
        return list_user[id]
    except:
        raise HTTPException(status_code=404, detail="User not found in DB")

 #delete   
@app.delete("/delete/{id}")
async def delete_user(id: int):
    #On récupère les informations d'un utilisateur et on supprime celles-ci en fonction de son id. On renvoi un 404 s'il n'est pas trouver dans la DB
    try:
        obj = list_user[id]
        list_user.pop(id)
        return obj
    except:
        raise HTTPException(status_code=404, detail="User not found in DB")

    if __name__ == "__main__":
        uvicorn.run(app, host="127.0.0.1",port=8000)