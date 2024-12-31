from constants import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Car, Garage, Maintenance
from pydantic_models import GarageValidation

router = APIRouter()

@router.post("/", response_model=GarageValidation)
def create_garage(garage: GarageValidation, db: Session = Depends(get_db)):
    new_garage = Garage(**garage.dict())
    db.add(new_garage)
    db.commit()
    db.refresh(new_garage)
    return new_garage

@router.get("/{garage_id}", response_model=GarageValidation)
def retrieve_garage(garage_id: int, db: Session = Depends(get_db)):
    garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not garage:
        raise HTTPException(status_code=404, detail=f"Garage with id: {garage_id} not found")
    return garage

@router.get("/")
def list_garages(city: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Garage)
    if city:
        query = query.filter(Garage.city == city)
    garages = query.all()
    if not garages and city:
        raise HTTPException(status_code=404, detail=f"No garages found in city: {city}")
    return garages

@router.put("/{garage_id}", response_model=GarageValidation)
def update_garage(garage_id: int, garage: GarageValidation, db: Session = Depends(get_db)):
    existing_garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if not existing_garage:
        raise HTTPException(status_code=404, detail="Garage not found")

    for field, value in garage.dict().items():
        setattr(existing_garage, field, value)

    db.commit()
    db.refresh(existing_garage)
    return existing_garage

@router.delete("/{garage_id}")
def remove_garage(garage_id: int, db: Session = Depends(get_db)):
    garage_to_delete = db.query(Garage).filter(Garage.id == garage_id).first()
    if not garage_to_delete:
        raise HTTPException(status_code=404, detail="Garage not found")

    db.delete(garage_to_delete)
    db.commit()
    return {"message": "Garage deleted successfully"}