from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory database
db = []

# Item model
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: str

# Create
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    item.id = len(db) + 1
    db.append(item)
    return item

# Read all
@app.get("/items/", response_model=List[Item])
def read_items():
    return db

# Read one
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    item = next((item for item in db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Update
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for item in db:
        if item.id == item_id:
            item.name = updated_item.name
            item.description = updated_item.description
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# Delete
@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    for index, item in enumerate(db):
        if item.id == item_id:
            return db.pop(index)
    raise HTTPException(status_code=404, detail="Item not found")