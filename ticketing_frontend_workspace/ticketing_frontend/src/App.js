import React, { useState } from 'react';
import './App.css';

// Modular imports
import Sidebar from './components/Sidebar';
import AuthPage from './components/AuthPage';
import TicketMainArea from './components/TicketMainArea';
import TicketModal from './components/TicketModal';

// Placeholder: Auth state logic
const useSimpleAuth = () => {
  // "user" is null until logged in
  const [user, setUser] = useState(null);
  return { user, setUser };
};

function App() {
  // Simulate basic auth state
  const { user, setUser } = useSimpleAuth();
  // Control modal open/close
  const [modalOpen, setModalOpen] = useState(false);
  const [editingTicket, setEditingTicket] = useState(null);

  if (!user) {
    return (
      <div className="auth-bg">
        <AuthPage setUser={setUser} />
      </div>
    );
  }

  return (
    <div className="app-layout">
      <Sidebar onCreateTicket={() => { setModalOpen(true); setEditingTicket(null); }}/>
      <main className="main-section">
        <TicketMainArea
          onEditTicket={(ticket) => { setEditingTicket(ticket); setModalOpen(true); }}
        />
      </main>
      {modalOpen && (
        <TicketModal
          onClose={() => { setModalOpen(false); setEditingTicket(null); }}
          ticket={editingTicket}
        />
      )}
    </div>
  );
}

export default App;