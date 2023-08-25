from fastapi import FastAPI,Query,HTTPException,Path,status,Body, WebSocket
#from pydantic import Basemodel
from database import curr_address
from database import phone_number
from database import email
from typing import Optional, List, Dict
from pydantic import BaseModel, Field as PydanticField
from pydantic.fields import Field
from fastapi.encoders import jsonable_encoder

class CurrAddress(BaseModel):
    apt_no: Optional[int]
    street_name: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    pincode: Optional[int]

class PhoneNumber(BaseModel):
    number: Optional[str]

class Email(BaseModel):
    email: Optional[str]

app=FastAPI()

@app.get("/")
def root():
    return {"hello" : "RIA"}

#mailing crud
@app.get("/curr_address")
def get_curr_address(number:Optional[int]=Query("")):
    print(number)
    if number in curr_address:
        return { number : curr_address[number] }
    else:
        return {"404": "Customer Not Found"}
    
@app.get("/curr_address/{id}",response_model=CurrAddress)
def get_curr_address_by_id(id: int=Path(...)):
    curr_add=curr_address.get(id)
    if not curr_add:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Could not find current address by ID")
    return curr_add


@app.put("/curr_address/{id}",response_model=Dict[str,CurrAddress])
def update_curr_address(id: int,curr_add:CurrAddress=Body(...)):
    stored=curr_address.get(id)
    if not stored:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Could not find current address ")
    stored=CurrAddress(**stored)
    new=curr_add.dict(exclude_unset=True)
    new=stored.copy(update=new)
    curr_address[id]=jsonable_encoder(new)
    response={}
    response[id]=curr_address[id]
    return response

#phone number crud
@app.get("/phone_number")
def get_phone_number(number:Optional[int]=Query("")):
    print(number)
    if number in phone_number:
        return { number : phone_number[number] }
    else:
        return {"404": "Customer Not Found"}
    
@app.get("/phone_number/{id}",response_model=PhoneNumber)
def get_phone_number_by_id(id: int=Path(...)):
    phone_num=phone_number.get(id)
    if not phone_num:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Could not find current phone number by ID")
    return phone_num


@app.put("/phone_number/{id}",response_model=Dict[str,PhoneNumber])
def update_phone_number(id: int,phone_num:PhoneNumber=Body(...)):
    stored=phone_number.get(id)
    if not stored:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Could not find current phone number")
    stored=PhoneNumber(**stored)
    new=phone_num.dict(exclude_unset=True)
    new=stored.copy(update=new)
    phone_number[id]=jsonable_encoder(new)
    response={}
    response[id]=phone_number[id]
    return response

#email crud
@app.get("/email")
def get_email(number:Optional[int]=Query("")):
    print(number)
    if number in email:
        return { number : email[number] }
    else:
        return {"404": "Customer Not Found"}
    
@app.get("/email/{id}",response_model=Email)
def get_email_by_id(id: int=Path(...)):
    email_add=email.get(id)
    if not email_add:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Could not find current email by ID")
    return email_add


@app.put("/email/{id}",response_model=Dict[str,Email])
def update_email(id: int,email_add:Email=Body(...)):
    stored=email.get(id)
    if not stored:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Could not find current email")
    stored=PhoneNumber(**stored)
    new=email_add.dict(exclude_unset=True)
    new=stored.copy(update=new)
    email[id]=jsonable_encoder(new)
    response={}
    response[id]=email[id]
    return response
