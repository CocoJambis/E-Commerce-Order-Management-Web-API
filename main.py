from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from App.db import get_db
from App.schemas import *
import App.crud as crud
import uvicorn
from App.config import settings

app = FastAPI()

@app.get("/")
def home():
    return {"message" : "Welcome!"}

#Crea utente
@app.post("/user", response_model=UserResponse)
def create_user(new_user:UserCreate, db:Session = Depends(get_db)):
    return crud.create_user(db, new_user=new_user)

#Tutti gli utenti
@app.get("/users/", response_model=list[UserResponse])
def all_users(db:Session = Depends(get_db)):
    return crud.user_list(db)

#Crea articolo
@app.post("/articolo", response_model=ArticoloResponse)
def crea_articolo(articolo:ArticoloCreate, db:Session = Depends(get_db)):
    return crud.create_articolo(db, articolo= articolo)

#Lista articoli
@app.get("/articoli/", response_model=list[ArticoloResponse])
def lista_articoli(db:Session = Depends(get_db)):
    return crud.all_articoli(db)

#Crea ordine
@app.post("/ordine/", response_model=OrderResponse)
def add_order(order:OrderCreate, db:Session = Depends(get_db)):
    return crud.create_order(db=db, ordine=order)

#Lista ordini
@app.get("/ordini/", response_model=list[OrderResponse])
def all_orders(db:Session = Depends(get_db)):
    return crud.all_orders(db)

#Lista articoli ordinati dall'id ordine
@app.get("/articoliordinati/{ordine_id}", response_model=list[ArticoliOrdinati])
def lista_articoli_ordinati(ordine_id:int, db:Session = Depends(get_db)):
    return crud.lista_articoli_ordinati_by_order_id(order_id=ordine_id, db=db)

#Lista ordini user
@app.get("/user/orders/{user_id}", response_model=list[OrderResponse])
def lista_orders_user(user_id:int, db:Session = Depends(get_db)):
    return crud.get_user_orders(user_id=user_id, db=db)

#Modifica prezzo articolo
@app.put("/articolo/{articolo_id}", response_model=ArticoloResponse)
def modifica_prezzo(nuovo_prezzo:ModificaPrezzoArticolo, articolo_id:int, db:Session = Depends(get_db)):
    return crud.prezzo_articolo(nuovo_prezzo=nuovo_prezzo, articolo_id=articolo_id, db=db)

@app.put("/ordinearticolo/{ordine_id}", response_model=ArticoliOrdinati)
def modifica_quantità_articolo_ordinata(ordine_id:int, nuova_quantità:OrderArt, db:Session = Depends(get_db)):
    return crud.edit_order(nuova_quantità=nuova_quantità, order_id=ordine_id, db=db)

#Aggiungi quantità disponibile
@app.put("/articolo/aggiungigiacenza/{articolo_id}", response_model=ArticoloResponse)
def aggiungi_quantità(nuova_quantità:ModificaGiacenzaArticolo, articolo_id:int, db:Session = Depends(get_db)):
    return crud.modifica_giacenza(articolo_id = articolo_id, nuova_giacenza=nuova_quantità, db=db)

#Elimina articolo
@app.delete("/articolo/{articolo_id}")
def delete_articolo(articolo_id:int, db:Session = Depends(get_db)):
    return crud.delete_articolo(articolo_id=articolo_id, db= db)

#Elimina user
@app.delete("/user/{user_id}")
def delete_user(user_id:int, db:Session = Depends(get_db)):
    return crud.delete_user(user_id=user_id, db=db)

#Elimina ordine
@app.delete("/ordini/{ordine_id}")
def delete_order(order_id:int, db:Session = Depends(get_db)):
    return crud.delete_order(order_id=order_id, db=db)

#Elimina articolo in ordine
@app.delete("/ordini/articolo{ordine_id}/{articolo_id}")
def delete_articolo_order(articolo_id:int, ordine_id:int, db:Session = Depends(get_db)):
    return crud.delete_order_articolo(order_id=ordine_id, 
                                      articolo_id=articolo_id,
                                      db=db)


if __name__ == "__main__":
    uvicorn.run(app, port=settings.port)