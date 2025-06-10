# Project Setup Guide

A concise walkthrough for installing dependencies and running both the **Flask** backend and the **Vite/React** frontend locally.

---

## Prerequisites

| Tool                 | Version                 | Notes                                                                                     |
| -------------------- | ----------------------- | ----------------------------------------------------------------------------------------- |
| **Python**           | 3.10 + (tested on 3.11) | Install from [https://www.python.org/](https://www.python.org/) or via a package manager. |
| **Node.js & npm**    | 18 +                    | Download from [https://nodejs.org/](https://nodejs.org/).                                 |
| **Git** *(optional)* | latest                  | Recommended for cloning the repo.                                                         |

> **Tip** – verify installations:
>
> ```bash
> python --version
> node --version
> npm --version
> ```

---

## Repository Layout

```
├── backend/    # Flask API
│   ├── app.py
│   ├── requirements.txt
│   └── …
└── frontend/   # Vite + React client
    ├── src/
    ├── package.json
    └── …
```

---

## 1. Environment Variables

Use a `.env` file in `backend/` to store configuration variables. A sample template is provided below as `.env.example`.

```ini
# SYSTEM
DEBUG=True
SECRET_KEY=
DB_NAME=database
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# OPEN AI
OPENAI_DEFAULT_MODEL=gpt-4o
OPENAI_API_KEY=
```

To use:

1. Copy the example file:

   ```bash
   cp backend/.env.example backend/.env
   ```
2. Fill in the missing values as needed.

---

## 2. Backend Setup (Flask)

```bash
# 1 — move into the backend folder
cd backend

# 2 — create & activate a virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3 — install Python dependencies
pip install -r requirements.txt

# 4 — run the development server
flask --app app run --debug
```

The API will default to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

---

## 3. Frontend Setup (Vite / React)

Open a **second** terminal tab/window so the backend can keep running.

```bash
# 1 — move into the frontend folder
cd frontend

# 2 — install JS dependencies
npm install

# 3 — start Vite's dev server
npm run dev
```

The app will be served at [http://localhost:5173/](http://localhost:5173/) and should hot-reload on file changes.

---

Happy testing! 🚀
