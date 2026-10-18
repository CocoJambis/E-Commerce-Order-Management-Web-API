from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional

#User Models
class UserCreate(BaseModel):
    first_name:str = Field(min_length=3, max_length=20)
    last_name:str = Field(min_length=3, max_length=20)
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:EmailStr
    is_active:bool
    role:str

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


class UserLogin(BaseModel):
    email:str
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    email: Optional[str] = None

