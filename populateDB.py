from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from constants import DATABASE_URL
from models import Car, Garage, Maintenance
from datetime import date

def create_and_add_garages(db):
    # Create Garage instances
    garages = [
        Garage(city="Velingrad", location="Velingrad", name="Garage01", capacity=30),
        Garage(city="Blagoevgrad", location="Blagoevgrad", name="Garage02", capacity=40),
        Garage(city="Sofiq", location="Sofiq", name="Garage03", capacity=80),
        Garage(city="Varna", location="Varna", name="Garage04", capacity=10),
    ]
    db.add_all(garages)
    db.commit()
    return garages


def create_and_add_cars(db, garages):
    # Create Car instances
    cars = [
        Car(make="Toyota", model="Corolla", productionYear=1999, licensePlate="DB12345", garages=[garages[0], garages[1]]),
        Car(make="BMW", model="F26", productionYear=2016, licensePlate="BG1224D", garages=[garages[2], garages[3]]),
        Car(make="Audi", model="e-tron", productionYear=2024, licensePlate="12322FF", garages=[garages[0], garages[3]]),
    ]
    db.add_all(cars)
    db.commit()
    return cars


def create_and_add_maintenances(db, cars, garages):
    # Create Maintenance instances
    maintenances = [
        Maintenance(carId=cars[0].id, garageId=garages[0].id, serviceType="Maintenance", scheduledDate=date(2015, 3, 1)),
        Maintenance(carId=cars[0].id, garageId=garages[0].id, serviceType="Yearly checkup", scheduledDate=date(2016, 3, 1)),
        Maintenance(carId=cars[0].id, garageId=garages[1].id, serviceType="Maintenance", scheduledDate=date(2018, 3, 1)),
        Maintenance(carId=cars[1].id, garageId=garages[2].id, serviceType="Maintenance", scheduledDate=date(2019, 3, 1)),
        Maintenance(carId=cars[1].id, garageId=garages[3].id, serviceType="Oil change", scheduledDate=date(2019, 3, 1)),
        Maintenance(carId=cars[2].id, garageId=garages[0].id, serviceType="Yearly checkup", scheduledDate=date(2015, 3, 1)),
        Maintenance(carId=cars[2].id, garageId=garages[0].id, serviceType="Maintenance", scheduledDate=date(2015, 3, 2)),
        Maintenance(carId=cars[2].id, garageId=garages[3].id, serviceType="Maintenance", scheduledDate=date(2023, 3, 1)),
    ]
    db.add_all(maintenances)
    db.commit()


def main():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = Session()

    try:
        # Create and add garages, cars, and maintenances to the database
        garages = create_and_add_garages(db)
        cars = create_and_add_cars(db, garages)
        create_and_add_maintenances(db, cars, garages)

    finally:
        db.close()


if __name__ == "__main__":
    main()