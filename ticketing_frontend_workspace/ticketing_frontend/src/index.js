import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";

// New: import all feature styles
import "./components/Sidebar.css";
import "./components/AuthPage.css";
import "./components/TicketMainArea.css";
import "./components/TicketModal.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
