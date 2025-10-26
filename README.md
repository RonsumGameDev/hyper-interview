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
```
To open the website on your browser

Use : http://127.0.0.1:8080/register
