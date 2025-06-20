import React, { useState } from "react";
import "./TicketMainArea.css";

// PUBLIC_INTERFACE
function TicketMainArea({ onEditTicket }) {
  // Placeholder data, replace with API fetch
  const [selected, setSelected] = useState(null);
  const demoTickets = [
    { id: 1, title: "Cannot access dashboard", status: "open", created: "2024-06-10" },
    { id: 2, title: "Feature Request: Dark Mode", status: "open", created: "2024-06-08" },
    { id: 3, title: "App crash on login", status: "closed", created: "2024-06-01" }
  ];

  // Show either the ticket list or ticket detail when selected
  return (
    <div className="main-area">
      <div className="main-header">
        <h1>Tickets</h1>
      </div>
      <div className="ticket-panel">
        <div className="ticket-list">
          {demoTickets.map((ticket) => (
            <div
              key={ticket.id}
              className={`ticket-list-item${selected === ticket.id ? " selected" : ""}`}
              onClick={() => setSelected(ticket.id)}
              tabIndex={0}
            >
              <span className="ticket-title">{ticket.title}</span>
              <span className={`ticket-status status-${ticket.status}`}>
                {ticket.status}
              </span>
            </div>
          ))}
        </div>
        <div className="ticket-detail">
          {selected !== null ? (
            <div>
              <h2>Ticket: {demoTickets.find((t) => t.id === selected).title}</h2>
              <p>Status: {demoTickets.find((t) => t.id === selected).status}</p>
              <p>Created: {demoTickets.find((t) => t.id === selected).created}</p>
              <button className="edit-btn" onClick={() => onEditTicket(demoTickets.find((t) => t.id === selected))}>
                Edit
              </button>
            </div>
          ) : (
            <div className="ticket-detail-placeholder">
              <span>Select a ticket to view details</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default TicketMainArea;
