from pydantic import BaseModel


class GarageValidation(BaseModel):
    id: int = None
    city: str
    location: str
    name: str
    capacity: int = 0

    class Config:
        from_attributes = True