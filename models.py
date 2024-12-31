from pyexpat import model
from sqlalchemy import Column, Date, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from constants import DATABASE_URL

Base = declarative_base()

class Garage(Base):
    __tablename__ = "Garage"

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    location = Column(String, nullable=False)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False, default=0)

    cars = relationship("Car", secondary="GarageCar", back_populates="garages")


class Car(Base):
    __tablename__ = "Car"

    id = Column(Integer, primary_key=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    productionYear = Column(Integer, nullable=False)
    licensePlate = Column(String, nullable=False)

    garages = relationship("Garage", secondary="GarageCar", back_populates="cars")


class GarageCar(Base):
    __tablename__ = "GarageCar"

    id = Column(Integer, primary_key=True)
    carId = Column(Integer, ForeignKey("Car.id"), nullable=False)
    garageId = Column(Integer, ForeignKey("Garage.id"), nullable=False)


class Maintenance(Base):
    __tablename__ = "Maintenance"

    id = Column(Integer, primary_key=True)
    carId = Column(Integer, ForeignKey("Car.id"), nullable=False)
    garageId = Column(Integer, ForeignKey("Garage.id"), nullable=False)
    serviceType = Column(String, nullable=False)
    scheduledDate = Column(Date, nullable=False)

    garage = relationship("Garage", backref="maintenances")  # backref keeps the Maintenance objects
    car = relationship("Car", backref="maintenances")

    @property
    def garageName(self) -> str:
        return self.garage.name

    @property
    def carName(self) -> str:
        return self.car.model

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base.metadata.create_all(bind=engine)