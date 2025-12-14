from database import SessionLocal, engine
import models

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

flights = [
    models.Flight(from_city="IST", to_city="AMS", date="2025-01-10", price=120, airline="CloudAir"),
    models.Flight(from_city="IST", to_city="PAR", date="2025-01-11", price=150, airline="TechJet"),
    models.Flight(from_city="IST", to_city="BER", date="2025-01-12", price=180, airline="SkyWays"),
    models.Flight(from_city="IST", to_city="ROM", date="2025-01-13", price=200, airline="EuroFly"),
    models.Flight(from_city="IST", to_city="MAD", date="2025-01-14", price=170, airline="JetCloud"),
    models.Flight(from_city="IST", to_city="LON", date="2025-01-15", price=220, airline="BlueAir"),
]

for flight in flights:
    db.add(flight)
    db.commit()
    db.refresh(flight)

    seats = []
    for row in range(1, 7):
        for col in ["A", "B", "C", "D", "E", "F"]:
            seats.append(
                models.Seat(
                    seat_number=f"{row}{col}",
                    is_booked=False,
                    flight_id=flight.id
                )
            )

    db.add_all(seats)
    db.commit()

db.close()
print(" Seed OK")
