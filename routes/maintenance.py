import calendar
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, date

from constants import get_db
from models import Car, Garage, Maintenance
from pydantic_models import MaintenanceValidationGET, MaintenanceValidationPOST, MaintenanceMonthlyRequestsReport
from routes.reports import build_monthly_report

router = APIRouter()


def get_car_and_garage(db: Session, car_id: int, garage_id: int):
    db_car = db.get(Car, car_id)
    db_garage = db.get(Garage, garage_id)

    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")
    if not db_garage:
        raise HTTPException(status_code=404, detail="Garage not found")

    return db_car, db_garage


def validate_car_belongs_to_garage(db_car, db_garage, selected_garage_id: int):
    selected_car_garage_ids = [garage.id for garage in db_car.garages]
    if selected_garage_id not in selected_car_garage_ids:
        raise HTTPException(
            status_code=400,
            detail=f"The selected car '{db_car.model}' does not belong to the selected garage '{db_garage.name}'"
        )


@router.post("/", response_model=MaintenanceValidationGET)
def post_maintenance(maintenance: MaintenanceValidationPOST, db: Session = Depends(get_db)):
    db_car, db_garage = get_car_and_garage(db, maintenance.carId, maintenance.garageId)

    validate_car_belongs_to_garage(db_car, db_garage, maintenance.garageId)

    new_maintenance = Maintenance(
        carId=db_car.id,
        garageId=db_garage.id,
        serviceType=maintenance.serviceType,
        scheduledDate=maintenance.scheduledDate,
    )

    db.add(new_maintenance)
    db.commit()
    db.refresh(new_maintenance)

    return new_maintenance


@router.get("/monthlyRequestsReport", response_model=list[MaintenanceMonthlyRequestsReport])
def garage_report(
    garageId: int,
    startMonth: str,
    endMonth: str,
    db: Session = Depends(get_db),
):
    db_garage = db.get(Garage, garageId)
    if not db_garage:
        raise HTTPException(status_code=404, detail="Garage not found")

    try:
        start_date = datetime.strptime(f"{startMonth}-01", "%Y-%m-%d")
        end_date = datetime.strptime(f"{endMonth}-{calendar.monthrange(int(endMonth[:4]), int(endMonth[5:7]))[1]}", "%Y-%m-%d")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format passed. It should adhere to 'yyyy-mm':\n{e}")

    maintenances = db.query(Maintenance).filter(
        Maintenance.garageId == garageId,
        Maintenance.scheduledDate >= start_date,
        Maintenance.scheduledDate <= end_date
    ).all()

    response = build_monthly_report(maintenances, start_date.year, end_date.year)
    return JSONResponse(content=response, status_code=200)


@router.put("/{maintenance_id}", response_model=MaintenanceValidationGET)
def update_maintenance(maintenance_id: int, maintenance: MaintenanceValidationPOST, db: Session = Depends(get_db)):
    db_car, db_garage = get_car_and_garage(db, maintenance.carId, maintenance.garageId)

    db_maintenance = db.get(Maintenance, maintenance_id)
    if not db_maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")

    validate_car_belongs_to_garage(db_car, db_garage, maintenance.garageId)

    db_maintenance.carId = maintenance.carId
    db_maintenance.garageId = maintenance.garageId
    db_maintenance.serviceType = maintenance.serviceType
    db_maintenance.scheduledDate = maintenance.scheduledDate

    db.commit()
    db.refresh(db_maintenance)

    return db_maintenance


@router.get("/{maintenance_id}", response_model=MaintenanceValidationGET)
def get_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    db_maintenance = db.get(Maintenance, maintenance_id)
    if not db_maintenance:
        raise HTTPException(status_code=404, detail=f"Maintenance with id: {maintenance_id} not found")

    return db_maintenance


@router.get("/", response_model=list[MaintenanceValidationGET])
def get_maintenances(
    carId: int | None = None,
    garageId: int | None = None,
    startDate: date | None = None,
    endDate: date | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Maintenance)

    if startDate and endDate and startDate > endDate:
        raise HTTPException(status_code=400, detail="startDate cannot be after endDate")

    if carId:
        query = query.filter(Maintenance.carId == carId)
    if garageId:
        query = query.filter(Maintenance.garageId == garageId)
    if startDate:
        query = query.filter(Maintenance.scheduledDate >= startDate)
    if endDate:
        query = query.filter(Maintenance.scheduledDate <= endDate)

    return query.all()


@router.delete("/{maintenance_id}")
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    db_maintenance = db.get(Maintenance, maintenance_id)

    if not db_maintenance:
        raise HTTPException(status_code=404, detail=f"Maintenance with id: {maintenance_id} not found")

    db.delete(db_maintenance)
    db.commit()

    return {"message": "Maintenance deleted successfully"}