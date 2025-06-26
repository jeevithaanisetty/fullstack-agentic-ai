from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel
import os
import json

app=FastAPI(title="Inventory Store API",version="1.0.0",description="This FastAAPI application is about Inventory ")

@app.get("/")
async def health():
    return {"message":"API is running....."}

DATAFILE="store.json"

class Store:
    def __init__(self,name,location,products):
       self.name=name
       self.location=location
       self.products=[Products(**p) for p in products]


    def __str__(self):
        return f"name:{self.name} , location:{self.location} , products:{self.products}"
    
    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "products": [p.to_dict() for p in self.products]
        }

class Products:
    def __init__(self,name,price,product_id,discount):
       self.name=name
       self.price=price
       self.product_id=product_id
       self.discount=discount

    def __str__(self):
        return f"name:{self.name} , price:{self.price} , product_id:{self.product_id} , discount:{self.discount}"
    
    def to_dict(self):
        return vars(self)
    
    @property
    def discount_applied(self):
        return self.price*(1-(self.discount/100))
    
class Item(BaseModel):
    name:str
    price:float
    product_id:str
    discount:int=None

class Store_details(BaseModel):
    name:str="d-mart"
    location:str=None

class Discount(BaseModel):
    product_id:str

class ProductDelete(BaseModel):
    product_id: str


@app.post("/edit_store")
async def edit_store_details(data:Store_details):
    stores=await load_from_json()
    stores[0].name=data.name
    stores[0].location=data.location
    await save_to_json(stores)
    return {"message":"store details were edited successfully...."}

@app.post("/add_product")
async def add_product_to_store(data:Item):
    stores= await load_from_json()
    if not stores:
        store=Store(name="d-mart",location="lalapet guntur",products=[])
        stores.append(store)     #now i have store to add product
    
    product=Products(
        name=data.name,
        price=data.price,
        product_id=data.product_id,
        discount=data.discount
    )
    stores[0].products.append(product)  # considering i have only one store and im appending to that store(first)
    await save_to_json(stores)
    return {"message":"product added to store successfully"}

@app.get("/list_all_products")
async def list_of_products():
    store=await load_from_json()
    if not store:
        raise HTTPException(status_code=404, detail="No store found.")
    items=[]
    for p in store[0].products:
        items.append(p)
    return items

@app.post("/discounted_price")
async def discount_value(data:Discount):
    store=await load_from_json()
    if not store:
        raise HTTPException(status_code=404, detail="No store found.")
    for p in store[0].products:
        if p.product_id==data.product_id:
            discounted_price=p.discount_applied 
            return {"message":f"discount is {p.discount} and price after discount applied is {discounted_price:.4f}"}

@app.post("/delete_product")
async def delete_product(data: ProductDelete):
    stores = await load_from_json()
    
    if not stores:
        raise HTTPException(status_code=404, detail="No store found.")
    original_count = len(stores[0].products)
    
    stores[0].products = [p for p in stores[0].products if p.product_id != data.product_id]
    
    if len(stores[0].products) == original_count:
        raise HTTPException(status_code=404, detail="Product not found.")
    
    await save_to_json(stores)
    return {"message": f"Product with ID {data.product_id} deleted successfully.."}

async def load_from_json():
    if not os.path.exists(DATAFILE):
        return []
    with open (DATAFILE,"r")as f:
        items=json.load(f)
    return [Store(**i) for i in items]

async def save_to_json(data):
    with open(DATAFILE,"w")as f:
        json.dump([i.to_dict() for i in data],f,indent=4)


