from sqlalchemy import Column, Integer, String, Boolean, ForeignKey # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from database import Base

#================================================================================

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    from_city = Column(String)
    to_city = Column(String)
    date = Column(String)
    price = Column(Integer)
    airline = Column(String)

    seats = relationship("Seat", back_populates="flight")

#================================================================================

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    seat_number = Column(String)
    is_booked = Column(Boolean, default=False) 
    
    passenger_name = Column(String, nullable=True)
    passenger_surname = Column(String, nullable=True)

    flight_id = Column(Integer, ForeignKey("flights.id"))

    flight = relationship("Flight", back_populates="seats")