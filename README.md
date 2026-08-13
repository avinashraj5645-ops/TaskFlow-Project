# ⚡ TaskFlow — Smart Task & Project Management App

TaskFlow ek modern full-stack Task & Project Management application hai jo **FastAPI (Python)** backend, **Vanilla JavaScript (ES Modules)** frontend, aur **Groq AI (Llama 3.3)** ke saath natural language task parsing support karta hai.

---

## ✨ Features

- 🔐 **Authentication & User Management:** JWT Token-based login, signup, profile caching, aur password update functionality.
- 🤖 **AI Quick-Add Task Parsing:** User ke natural language input (jaise *"Finish report tomorrow urgent"*) se AI (Groq API) automatically title, priority (`high`/`medium`/`low`), aur due date hint extract karta hai.
- 🛡️ **Smart Fallback System:** Agar AI service down ho ya API key na ho, toh system bina crash hue deterministic rule-based mock parser par fallback karta hai.
- 📁 **Project & Task Management:** Projects create karein, tasks manage karein, search & sort options ke saath.
- 🎨 **Modern Dark UI:** Clean responsive design eye-visibility password toggle aur smooth state transitions ke saath.

---

## 🛠️ Tech Stack

### **Backend**
- **Framework:** FastAPI (Python 3.13)
- **Server:** Uvicorn
- **Database / ORM:** SQLAlchemy
- **Validation:** Pydantic
- **AI Integration:** Groq API (`llama-3.3-70b-versatile` via OpenAI SDK)
- **Auth:** JWT (JSON Web Tokens) & Passlib / Bcrypt

### **Frontend**
- **Core:** HTML5, Modern CSS3, JavaScript (ES6+ Modules)
- **HTTP Client:** Fetch API (`api.js` abstraction layer)
- **Icons:** Inline SVG Icons

---

## 📂 Project Structure

```text
New project/
│
├── backend/
│   ├── main.py              # Main FastAPI application & routes
│   ├── database.py          # Database setup & session handling
│   ├── models.py            # SQLAlchemy Database Models
│   ├── auth.py              # Password hashing & JWT helpers
│   ├── quick_add.py         # Groq AI integration & Fallback Parser
│   ├── requirements.txt     # Python Dependencies
│   └── .env                 # Environment variables (Git-ignored)
│
├── frontend / root/
│   ├── index.html / login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── login.js             # Login page module
│   ├── api.js               # Central Fetch API Service
│   └── login.css
│
├── .gitignore               # Secrets & VirtualEnv ignore rules
└── README.md



# Windows (PowerShell)

python -m venv myenv
myenv\Scripts\Activate



# pip install -r backend/requirements.txt

fastapi
uvicorn[standard]
sqlalchemy
pydantic[email]
email-validator
requests
psysopg2-binar
supabase
python-dotenv
openai
bcrypt

# cd backend
uvicorn main:app --reload