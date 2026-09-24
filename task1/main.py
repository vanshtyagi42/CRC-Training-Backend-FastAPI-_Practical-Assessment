from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import Item, ALLOWED_STATUSES

app = FastAPI(title="Campus Lost & Found API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.get("/items", response_model=List[Item])
def get_items(session: Session = Depends(get_session)):
    items = session.exec(select(Item)).all()
    return items

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.title = updated_item.title
    item.description = updated_item.description
    item.category = updated_item.category
    item.location = updated_item.location
    item.reported_by = updated_item.reported_by
    item.status = updated_item.status

    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return None

@app.get("/items/status/{status}", response_model=List[Item])
def get_items_by_status(status: str, session: Session = Depends(get_session)):
    if status not in ALLOWED_STATUSES:
        raise HTTPException(status_code=400, detail=f"status must be one of {ALLOWED_STATUSES}")
    items = session.exec(select(Item).where(Item.status == status)).all()
    return items

@app.get("/items/category/{category}", response_model=List[Item])
def get_items_by_category(category: str, session: Session = Depends(get_session)):
    items = session.exec(select(Item).where(Item.category == category)).all()
    return items 