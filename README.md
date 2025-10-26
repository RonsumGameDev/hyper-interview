# Hackathon Portal 🏁

This project hosts a hackathon website using a **Flask frontend**, a **FastAPI backend**, and an **NGINX load balancer**.

## 🔧 Architecture
- Flask handles registration and UI.
- FastAPI handles problem selection and database operations.
- NGINX distributes requests across multiple FastAPI servers.

## ⚙️ Setup
### 1. Clone
```bash
git clone https://github.com/<your-username>/hackathon-portal.git
cd hackathon-portal
python -m venv venv
venv\scripts\activate
```

```bash backend
cd backend
pip install -r requirements.txt
cd ..
```

```bash frontend
cd frontend
pip install -r requirements.txt
cd ..
```

### 2. Running the server
```bash Console 1
cd hackathon-portal
venv\scripts\activate
uvicorn backend.main:app --port 8001
```
This intializes the Database then press ctrl + c
In the same console write 

```bash
uvicorn backend.api:app --reload --port 8001
```

```bash Console 2
cd hackathon-portal
venv\scripts\activate
python frontend/app.py
```

Go to your Nginx directory in your PC not the project ONE
Paste nginx.conf from the project to your main nginx.conf
Then from the console start your main nginx
```Console 3
cd nginx
start nginx
```

To open the website on your browser

Use : http://localhost:8080/register
