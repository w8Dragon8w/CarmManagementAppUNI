from pydantic import BaseModel
from datetime import date

class GarageValidation(BaseModel):
    id: int = None
    city: str
    location: str
    name: str
    capacity: int = 0

    class Config:
        from_attributes = True


class GarageAvailabilityReport(BaseModel):
    date: date
    requests: int
    available_capacity: int

    class Config:
        from_attributes = True


class CarValidationPOST(BaseModel):
    make: str
    model: str
    production_year: int
    license_plate: str
    garage_ids: list[int]

    class Config:
        from_attributes = True


class CarValidationGET(BaseModel):
    id: int
    make: str
    model: str
    production_year: int
    license_plate: str
    garages: list["GarageValidation"]

    class Config:
        from_attributes = True


class MaintenanceValidationGET(BaseModel):
    id: int
    car_id: int
    car_name: str
    service_type: str
    scheduled_date: date
    garage_id: int
    garage_name: str

    class Config:
        from_attributes = True


class MaintenanceValidationPOST(BaseModel):
    car_id: int
    garage_id: int
    scheduled_date: date
    service_type: str

    class Config:
        from_attributes = True


class YearMonth(BaseModel):
    year: int
    month: str
    leap_year: bool
    month_value: int


class MaintenanceMonthlyRequestsReport(BaseModel):
    year_month: YearMonth
    requests: int