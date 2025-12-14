export default function FlightList({ flights, onSelect }) {
  return (
    <div>
      {flights.map((f) => (
        <div key={f.id} className="flight-card" onClick={() => onSelect(f)}>
          <b>{f.from_city} → {f.to_city}</b>
          <div>{f.date}</div>
          <div>{f.airline} • ${f.price}</div>
        </div>
      ))}
    </div>
  );
}
