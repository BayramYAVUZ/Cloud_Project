from fastapi import FastAPI, Depends, Body, HTTPException
from typing import Optional
from sqlalchemy.orm import Session # type: ignore
from database import Base, engine, SessionLocal
from models import Flight, Seat
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace # type: ignore
from opentelemetry.exporter.jaeger.thrift import JaegerExporter # type: ignore
from opentelemetry.sdk.resources import SERVICE_NAME, Resource # type: ignore
from opentelemetry.sdk.trace import TracerProvider # type: ignore
from opentelemetry.sdk.trace.export import BatchSpanProcessor # type: ignore
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor # type: ignore

#================================================================================

trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "flight-backend"}))
)

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

#================================================================================

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#================================================================================

@app.on_event("startup")
def seed_data():
    db = SessionLocal()

    if db.query(Flight).count() == 0:
        flights = [
            Flight(from_city="IST", to_city="AMS", date="2025-01-10", price=120, airline="CloudAir"),
            Flight(from_city="SRY", to_city="23", date="2025-01-11", price=150, airline="TechJet"),
            Flight(from_city="FRN", to_city="HAS", date="2025-01-12", price=180, airline="SkyWays"),
            Flight(from_city="ISP", to_city="HAMB", date="2025-01-13", price=200, airline="EuroFly"),
            Flight(from_city="AMR", to_city="PARS", date="2025-01-14", price=170, airline="JetCloud"),
            Flight(from_city="ADN", to_city="BAYRN", date="2025-01-15", price=220, airline="BlueAir"),
        ]

        for flight in flights:
            db.add(flight)
            db.commit()
            db.refresh(flight)

            seats = [
                "1A","1B","1C",
                "2A","2B","2C",
                "3A","3B","3C",
                "4A","4B","4C"
            ]

            for seat in seats:
                db.add(
                    Seat(
                        seat_number=seat,
                        is_booked=False,
                        flight_id=flight.id
                    )
                )
            db.commit()

    db.close()

#================================================================================

@app.get("/")
def root():
    return {"message": "Flight API running"}

#================================================================================

@app.get("/flights")
def get_flights(
    from_city: Optional[str] = None,
    to_city: Optional[str] = None,
    date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Flight)

    if from_city:
        query = query.filter(Flight.from_city.ilike(f"%{from_city}%"))
    if to_city:
        query = query.filter(Flight.to_city.ilike(f"%{to_city}%"))
    if date:
        query = query.filter(Flight.date == date)

    return query.all()

#================================================================================

@app.get("/flights/{flight_id}/seats")
def get_seats(flight_id: int, db: Session = Depends(get_db)):
    return db.query(Seat).filter(Seat.flight_id == flight_id).all()

#================================================================================

@app.post("/seats/{seat_id}/reserve")
def reserve_seat(
    seat_id: int,
    passenger_name: str = Body(..., embed=True),
    passenger_surname: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    seat = db.query(Seat).filter(Seat.id == seat_id).first()

    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")

    if seat.is_booked:
        raise HTTPException(status_code=400, detail="Seat already booked")

    seat.is_booked = True
    seat.passenger_name = passenger_name
    seat.passenger_surname = passenger_surname
    
    db.commit()
    db.refresh(seat)
    
    return {"message": "Seat reserved", "seat_number": seat.seat_number}