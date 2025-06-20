import React from "react";
import "./Sidebar.css";

// PUBLIC_INTERFACE
function Sidebar({ onCreateTicket }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <span className="sidebar-logo" aria-label="logo" role="img">
          🎟️
        </span>
        <span className="sidebar-title">TicketFlow</span>
      </div>
      <nav className="sidebar-nav">
        <button className="sidebar-link" tabIndex="0">
          My Tickets
        </button>
        <button className="sidebar-link" tabIndex="0">
          All Tickets
        </button>
        <button className="sidebar-link" tabIndex="0">
          Closed Tickets
        </button>
      </nav>
      <button className="sidebar-btn-accent" onClick={onCreateTicket}>
        + New Ticket
      </button>
      <div className="sidebar-footer">
        <button className="sidebar-link sidebar-link-secondary">Logout</button>
      </div>
    </aside>
  );
}

export default Sidebar;
