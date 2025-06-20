import React, { useState } from "react";
import "./AuthPage.css";

/**
 * PUBLIC_INTERFACE
 * Authentication entry point (login/register).
 * Calls setUser on successful login (for demo, just returns a static user).
 */
function AuthPage({ setUser }) {
  const [mode, setMode] = useState("login");
  const [loading, setLoading] = useState(false);

  function onSubmit(e) {
    e.preventDefault();
    setLoading(true);
    // TODO: Replace with backend call
    setTimeout(() => {
      setUser({ id: 1, name: "Demo User" });
      setLoading(false);
    }, 500);
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-logo" aria-label="TicketFlow" role="img">
          🎟️
        </div>
        <h2>{mode === "login" ? "Login" : "Register"}</h2>
        <form onSubmit={onSubmit} className="auth-form">
          <input className="auth-input" placeholder="Email" required type="email" />
          <input className="auth-input" placeholder="Password" required type="password" />
          {mode === "register" && (
            <input className="auth-input" placeholder="Name" required />
          )}
          <button className="auth-btn" type="submit" disabled={loading}>
            {loading ? "..." : (mode === "login" ? "Login" : "Register")}
          </button>
        </form>
        <div className="auth-toggle">
          {mode === "login" ? (
            <span>
              Need an account?{" "}
              <button className="auth-link" type="button" onClick={() => setMode("register")}>
                Register
              </button>
            </span>
          ) : (
            <span>
              Already have an account?{" "}
              <button className="auth-link" type="button" onClick={() => setMode("login")}>
                Login
              </button>
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

export default AuthPage;
