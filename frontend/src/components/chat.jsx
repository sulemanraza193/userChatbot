import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL;

function Chat({ admin, onLogout }) {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! I'm your User Management AI. You can ask me to add, find, update, delete, or list users.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    const message = input.trim();

    if (!message || loading) {
      return;
    }

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: message,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/chat/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong");
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.message,
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: `Error: ${error.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage();
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-container">

      <header className="chat-header">
        <div>
          <h2> User Management </h2>
          <span>Admin: {admin.email}</span>
        </div>

        <button className="logout-button" onClick={onLogout}>
          Logout
        </button>
      </header>

      <main className="chat-messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message-row ${message.role}`}
          >
            <div className={`message ${message.role}`}>
              {message.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message-row assistant">
            <div className="message assistant typing">
              AI is thinking...
            </div>
          </div>
        )}
      </main>

      <div className="suggestions">
        <button
          onClick={() =>
            setInput("Add john.smith@xyz.com with phone number +92332")
          }
        >
          Add user
        </button>

        <button
          onClick={() =>
            setInput("Find samantha@example.com")
          }
        >
          Find user
        </button>

        <button
          onClick={() =>
            setInput("Update Samantha's city to Cordoba")
          }
        >
          Update user
        </button>

        <button
          onClick={() =>
            setInput("Show me all users")
          }
        >
          List users
        </button>
      </div>

      <form className="chat-input-area" onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a command, e.g. Add john@example.com..."
          rows="1"
          disabled={loading}
        />

        <button type="submit" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>

    </div>
  );
}

export default Chat;
