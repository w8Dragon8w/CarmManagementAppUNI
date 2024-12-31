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
    availableCapacity: int

    class Config:
        from_attributes = True


class CarValidationPOST(BaseModel):
    make: str
    model: str
    productionYear: int
    licensePlate: str
    garageIds: list[int]

    class Config:
        from_attributes = True


class CarValidationGET(BaseModel):
    id: int
    make: str
    model: str
    productionYear: int
    licensePlate: str
    garages: list["GarageValidation"]

    class Config:
        from_attributes = True


class MaintenanceValidationGET(BaseModel):
    id: int
    carId: int
    carName: str
    serviceType: str
    scheduledDate: date
    garageId: int
    garageName: str

    class Config:
        from_attributes = True


class MaintenanceValidationPOST(BaseModel):
    carId: int
    garageId: int
    scheduledDate: date
    serviceType: str

    class Config:
        from_attributes = True


class YearMonth(BaseModel):
    year: int
    month: str
    leapYear: bool
    monthValue: int


class MaintenanceMonthlyRequestsReport(BaseModel):
    yearMonth: YearMonth
    requests: int