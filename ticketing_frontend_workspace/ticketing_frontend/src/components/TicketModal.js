import React from "react";
import "./TicketModal.css";

/**
 * PUBLIC_INTERFACE
 * Modal for creating or editing a ticket.
 * Props:
 *   - onClose(): function to close the modal
 *   - ticket: ticket object (if editing)
 */
function TicketModal({ onClose, ticket }) {
  // Placeholder for form content
  return (
    <div className="ticket-modal-backdrop">
      <div className="ticket-modal">
        <h2>{ticket ? "Edit Ticket" : "Create Ticket"}</h2>
        <form>
          <input
            className="modal-input"
            placeholder="Title"
            required
            defaultValue={ticket?.title || ""}
          />
          <textarea className="modal-input" placeholder="Description" rows={5} defaultValue={ticket?.description || ""} />
          <div className="modal-actions">
            <button type="submit" className="modal-save">
              Save
            </button>
            <button type="button" className="modal-cancel" onClick={onClose}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default TicketModal;
