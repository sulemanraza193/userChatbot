# 🤖 AI User Management Chatbot

An AI-powered user management chatbot that allows an administrator to manage users through natural-language commands.

Instead of using traditional forms or manually writing database queries, the admin can simply communicate with the chatbot.

For example:

> "Add [john.smith@xyz.com](mailto:john.smith@xyz.com) with phone number +92332"

> "Remove [john.smith@xyz.com](mailto:john.smith@xyz.com)"

> "Update Samantha's city to Cordoba"

The AI understands the request and uses backend tools to perform the appropriate database operation.

## 🚀 Features

* 🔐 Simple admin authentication
* 💬 Natural-language chatbot interface
* ➕ Add users
* 🔍 Find users
* ✏️ Update user information
* 🗑️ Delete users
* 📋 List all users
* 🤖 AI-powered tool/function calling
* 🗄️ MongoDB database integration
* ⚡ FastAPI backend
* ⚛️ React frontend
* 📱 Responsive chat interface
* 🔒 API keys stored using environment variables

## 🛠️ Tech Stack

### Frontend

* React
* Vite
* JavaScript
* CSS

### Backend

* Python
* FastAPI
* Pydantic
* PyMongo

### Database

* MongoDB

### AI

* Groq API
* `openai/gpt-oss-120b`
* Function/tool calling

### Deployment

* Vercel — Frontend
* Railway — Backend
* MongoDB Atlas — Database

## 🏗️ Project Structure

```text
ai-user-management-chatbot/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── admin.py
│   │   │   └── user.py
│   │   │
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   └── users.py
│   │   │
│   │   ├── services/
│   │   │   └── gemini_service.py
│   │   │
│   │   ├── tools/
│   │   │   └── user_tools.py
│   │   │
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── chat.jsx
│   │   │   └── login.jsx
│   │   │
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── .gitignore
│
└── README.md
```

## 🧠 How It Works

The application follows this flow:

```text
Admin
  │
  ▼
React Chat Interface
  │
  ▼
FastAPI Backend
  │
  ▼
Groq AI
  │
  ▼
AI selects appropriate tool
  │
  ├── create_user()
  ├── find_user()
  ├── update_user()
  ├── delete_user()
  └── list_users()
  │
  ▼
MongoDB
  │
  ▼
Tool Result
  │
  ▼
Groq AI
  │
  ▼
Natural-language response
  │
  ▼
Admin
```

## 💬 Example Commands

### Add a user

```text
Add john.smith@xyz.com with phone number +92332
```

### Find a user

```text
Find john.smith@xyz.com
```

### Update a user

```text
Update Samantha's city to Cordoba
```

### Delete a user

```text
Remove john.smith@xyz.com
```

### List users

```text
Show me all users
```

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
```

Activate the virtual environment.

Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Backend environment variables

Create a `.env` file inside `backend`:

```env
MONGODB_URI=mongodb://127.0.0.1:27017
DATABASE_NAME=user_chatbot
GROQ_API_KEY=your_groq_api_key
FRONTEND_URL=http://localhost:5173
```

Never commit the `.env` file to GitHub.

### 4. Start the backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Frontend setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The React application will normally run at:

```text
http://localhost:5173
```

## 🔐 Environment Variables

### Backend

```env
MONGODB_URI=
DATABASE_NAME=
GROQ_API_KEY=
FRONTEND_URL=
```

### Frontend

```env
VITE_API_URL=
```

API keys and credentials should never be committed to the repository.

## 🌐 Deployment

### Frontend

The React/Vite frontend can be deployed using Vercel.

Set the Vercel environment variable:

```text
VITE_API_URL=https://your-backend-url
```

### Backend

The FastAPI backend can be deployed using Railway or another Python-compatible hosting platform.

Production environment variables:

```env
MONGODB_URI=your_mongodb_atlas_connection_string
DATABASE_NAME=user_chatbot
GROQ_API_KEY=your_groq_api_key
FRONTEND_URL=https://your-frontend.vercel.app
```

### Database

For production deployment, use MongoDB Atlas instead of:

```text
mongodb://127.0.0.1:27017
```

## 🔒 Security Notes

This project is designed as an internship assignment/demo application.

For production use, the authentication system should be extended with:

* Password authentication
* JWT/session-based authentication
* Role-based authorization
* Rate limiting
* Input validation
* Secure cookie configuration
* More detailed audit logging

## 📌 Assignment

This project was developed as an AI/Python internship assignment demonstrating:

* AI integration
* Natural-language processing
* Function/tool calling
* REST API development
* Database CRUD operations
* React frontend development
* Full-stack integration

## 👨‍💻 Author

**Suleman Raza**

Computer Science Student
AI & Full-Stack Developer
