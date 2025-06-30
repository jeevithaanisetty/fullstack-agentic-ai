from fastapi import FastAPI, Query
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

# Pydantic model
class Item(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool

class Data(BaseModel):
    in_stock:bool

# Fake in-memory "database"  i.e data stored in RAM not in disk so it disappears in memory when u restart app
items_db = [
    Item(id=1, name="Apple", price=1.2, in_stock=True),
    Item(id=2, name="Banana", price=0.5, in_stock=False),
    Item(id=3, name="Orange", price=0.8, in_stock=True),
    Item(id=4, name="Pineapple", price=2.0, in_stock=True),
    Item(id=5, name="Grape", price=1.5, in_stock=False),
]

@app.get("/search", response_model=List[Item])  # saying response could be a list of items(optional bt highly reco fro type safety)
def search_items(
    name: Optional[str] = Query(None, description="Filter by name (partial match)"),  #use opt for params that r not required r none
    in_stock: Optional[bool] = Query(None, description="Filter by stock availability")
): # 'http://127.0.0.1:8000/search?name=grape&in_stock=true'
    results = items_db

    if name:
        results = [item for item in results if name.lower() in item.name.lower()]
    if in_stock is not None:
        results = [item for item in results if item.in_stock == in_stock]
    
    return results

# WAY1  POST  --->USING PAYLOAD
@app.post("/list_all",response_model=List[Item])  #list[data]-->gives o/p consists of your data cls values only i.e [{in_stock=true},{in_stock=true},....] not full item values only in data values
def list_items(data:Data):
    present_in_stock=data.in_stock
    result=items_db
    if present_in_stock is not None:
        result=[i for i in result if i.in_stock==present_in_stock]
    return result

#WAY2   GET -->USING QUERY PARAMS    http://127.0.0.1:8000/list_all_items?in_stock=true

@app.get("/list_all_items",response_model=List[Item])  #list[data]-->gives o/p consists of your data cls values only i.e [{in_stock=true},{in_stock=true},....] not full item values only in data values
def list_items(in_stock:Optional[bool]=Query(None,description="filter based on stock")):
    result=items_db
    if in_stock is not None:
        result=[i for i in result if i.in_stock==in_stock]
    return result