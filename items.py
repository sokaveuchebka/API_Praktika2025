from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ItemDB
from schemas import ItemCreate, ItemResponse, ItemUpdate
from auth import get_current_user, require_role

router = APIRouter()

@router.get("/", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(ItemDB).all()

@router.post("/", response_model=ItemResponse)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role(["Admin"]))
):
    db_item = ItemDB(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item_update: ItemUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_role(["Admin"]))
):
    db_item = db.query(ItemDB).filter(item_id == ItemDB.id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    if item_update.name is not None:
        db_item.name = item_update.name
    if item_update.description is not None:
        db_item.description = item_update.description

    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role(["Admin"]))
):
    item = db.query(ItemDB).filter(item_id == ItemDB.id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}
