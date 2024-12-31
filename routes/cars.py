from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from constants import get_db
from models import Car, Garage, Maintenance, GarageCar
from pydantic_models import CarValidationPOST, CarValidationGET

router = APIRouter()


@router.post("/", response_model=CarValidationGET)
def create_car(car_data: CarValidationPOST, db: Session = Depends(get_db)):
    # Fetch garages by IDs
    garages = db.query(Garage).filter(Garage.id.in_(car_data.garage_ids)).all()

    # Validate that all provided garage IDs exist
    if len(garages) != len(car_data.garage_ids):
        raise HTTPException(status_code=404, detail="Some garages were not found")

    # Create a new Car instance
    new_car = Car(
        make=car_data.make,
        model=car_data.model,
        productionYear=car_data.production_year,
        licensePlate=car_data.license_plate,
        garages=garages,
    )

    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


@router.put("/{car_id}", response_model=CarValidationGET)
def update_car(car_id: int, car_data: CarValidationPOST, db: Session = Depends(get_db)):
    # Fetch the car by ID
    db_car = db.query(Car).filter(Car.id == car_id).first()

    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")

    # Fetch garages by IDs
    garages = db.query(Garage).filter(Garage.id.in_(car_data.garage_ids)).all()

    if len(garages) != len(car_data.garage_ids):
        raise HTTPException(status_code=404, detail="Some garages were not found")

    # Update the car fields
    db_car.make = car_data.make
    db_car.model = car_data.model
    db_car.productionYear = car_data.production_year
    db_car.licensePlate = car_data.license_plate
    db_car.garages = garages

    db.commit()
    db.refresh(db_car)
    return db_car


@router.get("/{car_id}", response_model=CarValidationGET)
def retrieve_car(car_id: int, db: Session = Depends(get_db)):
    # Fetch the car by ID
    car = db.query(Car).filter(Car.id == car_id).first()

    if not car:
        raise HTTPException(status_code=404, detail=f"Car with id {car_id} not found")

    return car


@router.get("/", response_model=list[CarValidationGET])
def list_cars(
    car_make: str | None = None,
    garage_id: int | None = None,
    from_year: int | None = None,
    to_year: int | None = None,
    db: Session = Depends(get_db),
):
    # Base query for cars
    query = db.query(Car)

    # Apply filters based on provided query parameters
    if car_make:
        query = query.filter(Car.make == car_make)

    if from_year:
        query = query.filter(Car.productionYear >= from_year)

    if to_year:
        query = query.filter(Car.productionYear <= to_year)

    if garage_id:
        query = query.join(GarageCar).filter(GarageCar.garageId == garage_id)

    cars = query.all()
    return cars


@router.delete("/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    # Fetch the car by ID
    db_car = db.query(Car).filter(Car.id == car_id).first()

    if not db_car:
        raise HTTPException(status_code=404, detail=f"Car with id {car_id} not found")

    # Delete the car
    db.delete(db_car)
    db.commit()
    return {"message": f"Car with id {car_id} deleted successfully"}