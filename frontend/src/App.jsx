import { useEffect, useState } from "react";
import { fetchFlights, fetchSeats } from "./api";
import FlightList from "./FlightList";
import SeatMap from "./SeatMap";
import "./App.css";

export default function App() {
  const [flights, setFlights] = useState([]);
  const [seats, setSeats] = useState([]);
  const [fromCity, setFromCity] = useState("");
  const [toCity, setToCity] = useState("");
  const [date, setDate] = useState("");

  useEffect(() => {
    loadFlights();
  }, []);

  const loadFlights = async () => {
    const data = await fetchFlights(fromCity, toCity, date);
    setFlights(data);
  };

  return (
    <div className="app-background">
      <div className="overlay">
        <header className="header">
          <img src="/logo-1.png" alt="Logo" className="logo" />
        </header>

        <div className="container">
          <h1>Flight Search V</h1>

          <div className="filters">
            <input
              placeholder="From"
              value={fromCity}
              onChange={(e) => setFromCity(e.target.value)}
            />
            <input
              placeholder="To"
              value={toCity}
              onChange={(e) => setToCity(e.target.value)}
            />
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
            <button onClick={loadFlights}>Search</button>
          </div>

          <FlightList
            flights={flights}
            onSelect={async (f) => {
              const s = await fetchSeats(f.id);
              setSeats(s);
            }}
          />

          {seats.length > 0 && <SeatMap seats={seats} />}
        </div>
      </div>
    </div>
  );
}
