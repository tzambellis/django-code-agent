# 🧠 Django AI Project Generator (POC)

This is a **proof of concept** (POC) for an AI-powered Django app that takes a prompt and automatically scaffolds a Django project — models, views, templates, URLs, and more — using agents.

It includes a Celery background worker to process prompts and optionally pushes the generated Django app into a GitLab repository using a personal or deploy token.

⚠️ This project is still experimental and contains WIP/spaghetti code. You are welcome to try, fork, or contribute.

---

## 🚀 Features

- ✨ AI Agent builds Django apps from a natural language idea
- 🔁 Celery + Redis handles async background task processing
- 🗂️ Generated Django project is saved to `/tmp/project_<id>` and downloadable as `.zip`
- 🚀 Optionally pushes the result to a GitLab repo using user tokens
- 🛠 Prompt and key management via web UI

---

## 📦 Prerequisites

Before you can test the project with Docker, make sure you have:

- [Docker](https://www.docker.com/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

---

## ▶️ Quick Start with Docker

1. **Clone the repo**:

   ```bash
   git clone <REPO_URL>
   cd DjangoAgentDashboard
   ```

2. **Start all services (web, Celery worker, Redis)**:

   ```bash
   docker compose up --build
   ```

This will:
- Build the Django app container
- Start the Redis broker
- Run Celery worker in parallel
- Automatically apply migrations and start Gunicorn


3. **Open the app in your browser:**:
   ```bash
    http://localhost:8000/accounts/login
   ```

4. **Login**:
Use the credentials **admin** for username and password.
---

## 🧩 Services

- web: Django app via Gunicorn (port 8000)
- worker: Celery worker (internal)
- redis: Redis message broker (port 6379)

---

## 🗂 Notes

- Celery saves generated Django apps to /tmp/project_<id>
- A shared Docker volume makes it accessible to Django for download
- Download link appears when a prompt finishes with status "succeed"

---

## 🧪 Testing

Manual testing via the web UI. Automated tests coming later.

---

## 🧹 Cleanup

To stop everything and remove volumes:

   ```bash
   docker compose down --volumes
   ```

---
