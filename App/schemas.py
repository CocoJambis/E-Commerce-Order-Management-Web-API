from pydantic import BaseModel, EmailStr, ConfigDict

#User Models
class UserCreate(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr

class UserResponse(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:EmailStr

    model_config = ConfigDict(from_attributes=True)


#Articolo Models
class ArticoloCreate(BaseModel):
    name:str
    desc:str
    prezzo:float
    quantità:int

class ArticoloResponse(BaseModel):
    id:int
    name:str
    desc:str
    prezzo:float
    quantità:int

    model_config = ConfigDict(from_attributes= True)

class ModificaPrezzoArticolo(BaseModel):
    prezzo:float

class ModificaGiacenzaArticolo(BaseModel):
    quantità:int


#Order Models
class OrderArt(BaseModel):
    articolo_id:int
    quantità:int


class OrderCreate(BaseModel):
    user_id:int
    articoli:list[OrderArt]


class OrderResponse(BaseModel):
    id:int
    user_id:int
    total:float

    model_config = ConfigDict(from_attributes=True)


#OrderArticolo models
class ArticoliOrdinati(BaseModel):
    order_id:int
    articolo_id:int
    quantità_ordinata:int

    model_config = ConfigDict(from_attributes=True)
