import { useEffect, useState } from "react";

function Notifications() {

  const [notes, setNotes] = useState([]);

  useEffect(() => {

    fetch("http://localhost:8000/notifications")
      .then(res => res.json())
      .then(data => setNotes(data));

  }, []);

  return (
    <div>

      <h2>Live Alerts</h2>

      {notes.map(note => (
        <div key={note.id}
          style={{
            border: "1px solid #444",
            padding: 10,
            marginBottom: 10
          }}
        >
          <h4>{note.title}</h4>
          <p>{note.message}</p>
        </div>
      ))}

    </div>
  );
}

export default Notifications;
