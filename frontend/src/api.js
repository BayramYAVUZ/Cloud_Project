const API_URL = "http://127.0.0.1:8000";

export async function fetchFlights(from, to, date) {
  const params = new URLSearchParams();
  if (from) params.append("from_city", from);
  if (to) params.append("to_city", to);
  if (date) params.append("date", date);

  const res = await fetch(`${API_URL}/flights?${params}`);
  return res.json();
}

export async function fetchSeats(flightId) {
  const res = await fetch(`${API_URL}/flights/${flightId}/seats`);
  return res.json();
}

export async function reserveSeat(seatId, name, surname) {
  const res = await fetch(`${API_URL}/seats/${seatId}/reserve`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      passenger_name: name,
      passenger_surname: surname,
    }),
  });

  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || "Error booking seat");
  }

  return res.json();
}
//================================================================================