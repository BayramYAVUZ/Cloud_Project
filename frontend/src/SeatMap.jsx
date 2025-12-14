import React, { useState } from "react";
import { reserveSeat } from "./api";

export default function SeatMap({ seats }) {
  const [selectedSeat, setSelectedSeat] = useState(null);
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");

  const handleSeatClick = (seat) => {
    if (seat.is_booked) return;
    setSelectedSeat(seat);
    setName("");
    setSurname("");
  };

  const handleReserve = async () => {
    if (!name || !surname) {
      alert("Please enter your first and last name.");
      return;
    }

    try {
      await reserveSeat(selectedSeat.id, name, surname);
      alert(` Seat ${selectedSeat.seat_number}  Retrieved successfully!`);
      window.location.reload(); 
    } catch (error) {
      alert("Error : " + error.message);
    }
  };

  return (
    <div style={{ marginTop: "20px", textAlign: "center" }}>
      <h2>Koltuk Seçimi</h2>
      
      {}
      <div className="seat-grid" style={{ 
          display: "grid", 
          gridTemplateColumns: "repeat(4, 50px)", 
          gap: "10px", 
          justifyContent: "center",
          margin: "0 auto",
          maxWidth: "300px"
      }}>
        {seats.map((s) => (
          <div
            key={s.id}
            onClick={() => handleSeatClick(s)}
            className={`seat ${s.is_booked ? "booked" : "free"}`}
            style={{
              height: "50px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              borderRadius: "8px",
              cursor: s.is_booked ? "not-allowed" : "pointer",
              backgroundColor: s.is_booked ? "#dc3545" : (selectedSeat?.id === s.id ? "#007bff" : "#28a745"),
              color: "white",
              fontWeight: "bold",
              border: selectedSeat?.id === s.id ? "3px solid #0056b3" : "none",
              opacity: s.is_booked ? 0.5 : 1
            }}
          >
            {s.seat_number}
          </div>
        ))}
      </div>

      {}
      {selectedSeat && !selectedSeat.is_booked && (
        <div style={{ 
            marginTop: "20px", 
            padding: "20px", 
            background: "#f8f9fa", 
            borderRadius: "10px",
            border: "1px solid #ddd",
            display: "inline-block"
        }}>
          <h3>Seçilen Koltuk: {selectedSeat.seat_number}</h3>
          <div style={{ marginBottom: "10px" }}>
            <input
              placeholder="Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              style={{ padding: "8px", marginRight: "5px", borderRadius: "4px", border: "1px solid #ccc" }}
            />
            <input
              placeholder="Surname"
              value={surname}
              onChange={(e) => setSurname(e.target.value)}
              style={{ padding: "8px", borderRadius: "4px", border: "1px solid #ccc" }}
            />
          </div>
          <button 
            onClick={handleReserve}
            style={{
              padding: "10px 20px",
              backgroundColor: "#007bff",
              color: "white",
              border: "none",
              borderRadius: "5px",
              cursor: "pointer",
              fontWeight: "bold"
            }}
          >
            Rezerve Et
          </button>
        </div>
      )}
    </div>
  );
}
//================================================================================