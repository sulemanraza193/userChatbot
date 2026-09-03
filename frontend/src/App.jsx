import { useState } from "react";
import Login from "./components/login.jsx";
import Chat from "./components/chat.jsx";
import "./App.css";

function App() {
  const [admin, setAdmin] = useState(null);

  const handleLogin = (adminData) => {
    setAdmin(adminData);
  };

  const handleLogout = () => {
    setAdmin(null);
  };

  return (
    <div className="app">
      {!admin ? (
        <Login onLogin={handleLogin} />
      ) : (
        <Chat admin={admin} onLogout={handleLogout} />
      )}
    </div>
  );
}

export default App;