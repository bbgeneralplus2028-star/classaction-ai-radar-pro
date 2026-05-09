import { useEffect, useState } from "react";

function App() {
  const [lawsuits, setLawsuits] = useState([]);
showPopup(
  "New Lawsuit Alert",
  lawsuit.title
)
  useEffect(() => {
    fetch("http://localhost:8000/lawsuits")
      .then(res => res.json())
      .then(data => setLawsuits(data));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>ClassAction AI Radar Pro</h1>

      {lawsuits.map(l => (
        <div key={l.id} style={{ border: "1px solid #ccc", margin: 10, padding: 10 }}>
          <h3>{l.title}</h3>
          <p>{l.summary}</p>
          <a href={l.url} target="_blank">View Case</a>
        </div>
      ))}
    </div>
  );
}

export default App;
