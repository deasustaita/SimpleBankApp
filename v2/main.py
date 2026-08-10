from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello, World!"}

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def create_item(item: Item):
    return item

# post create customer profile

# get list customers

# get customer details
# MAIN.PY SHOULD BE IN CONTROLLERS NOT MODELS?


# MODELS WILL NOT INCLUDE THE DATABASE RN
# IT WILL BE HARD-CODED