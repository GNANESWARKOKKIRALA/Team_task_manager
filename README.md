# 🗂️ Team Task Manager — Full-Stack Web App

> A full-stack project management web application with **role-based access control (Admin/Member)**, built with **Flask + SQLAlchemy + SQLite**, deployed on **Render**.

---

## 📌 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Database Design](#database-design)
6. [Role-Based Access Control](#role-based-access-control)
7. [How to Run Locally (VS Code Step-by-Step)](#how-to-run-locally)
8. [Deployment on Render](#deployment-on-render)
9. [API / Route Reference](#api--route-reference)
10. [Author](#author)

---

## 📖 Project Overview

**Team Task Manager** is a collaborative project management tool that allows teams to:

- Create and manage projects
- Assign tasks to team members
- Track task status (Todo → In Progress → Done)
- View overdue tasks on a real-time dashboard
- Control access using **Admin** and **Member** roles

This project was built as a **full-stack web application assignment** covering REST-like routing, database modeling, authentication, and cloud deployment.

---

## 🚀 Features

| Feature               | Description                                                                                  |
| --------------------- | -------------------------------------------------------------------------------------------- |
| ✅ Authentication     | Signup / Login / Logout with hashed passwords                                                |
| ✅ Role-Based Access  | Admin can create projects, add members, delete tasks; Member can view and update their tasks |
| ✅ Project Management | Create projects, view members, track task counts                                             |
| ✅ Task Management    | Create tasks with priority (High/Medium/Low), due date, assignment                           |
| ✅ Status Tracking    | Kanban-style board: Todo → In Progress → Done                                              |
| ✅ Overdue Detection  | Auto-detects and highlights overdue tasks on dashboard                                       |
| ✅ Dashboard          | Overview of all stats: total tasks, completed, in-progress, overdue                          |
| ✅ Deployment         | Live on Render via Gunicorn                                                                  |

---

## 🛠️ Tech Stack

| Layer                | Technology                              |
| -------------------- | --------------------------------------- |
| **Frontend**   | Flask Jinja2 Templates + Bootstrap 5    |
| **Backend**    | Flask (Python) — REST-style routes     |
| **Database**   | SQLite (via SQLAlchemy ORM)             |
| **Auth**       | Flask-Login + Werkzeug password hashing |
| **Deployment** | Render + Gunicorn                       |

---

## 📁 Project Structure

```
team_task_manager/
│
├── app/                        # Main application package
│   ├── __init__.py             # App factory (create_app)
│   ├── models.py               # SQLAlchemy DB models
│   │
│   ├── routes/                 # Blueprint route handlers
│   │   ├── auth.py             # /auth/signup, /auth/login, /auth/logout
│   │   ├── dashboard.py        # / and /dashboard
│   │   ├── projects.py         # /projects/...
│   │   └── tasks.py            # /tasks/...
│   │
│   └── templates/              # Jinja2 HTML templates
│       ├── base.html           # Base layout (sidebar + navbar)
│       ├── auth/
│       │   ├── login.html
│       │   └── signup.html
│       ├── dashboard/
│       │   └── index.html
│       ├── projects/
│       │   ├── list.html
│       │   ├── create.html
│       │   └── view.html
│       └── tasks/
│           └── create.html
│
├── run.py                      # Entry point — runs Flask app
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment config
├── .gitignore
└── README.md
```

---

## 🗄️ Database Design

### Tables

#### `users`

| Column        | Type         | Description              |
| ------------- | ------------ | ------------------------ |
| id            | Integer (PK) | Auto-increment           |
| username      | String       | Unique username          |
| email         | String       | Unique email             |
| password_hash | String       | Werkzeug hashed password |
| role          | String       | `Admin` or `Member`  |
| created_at    | DateTime     | Registration time        |

#### `projects`

| Column      | Type                 | Description                   |
| ----------- | -------------------- | ----------------------------- |
| id          | Integer (PK)         | Auto-increment                |
| name        | String               | Project name                  |
| description | Text                 | Optional description          |
| owner_id    | ForeignKey(users.id) | Admin who created it          |
| status      | String               | Active / Completed / Archived |
| created_at  | DateTime             | Creation timestamp            |

#### `project_members` (Join Table)

| Column     | Type                    | Description    |
| ---------- | ----------------------- | -------------- |
| id         | Integer (PK)            | Auto-increment |
| project_id | ForeignKey(projects.id) | The project    |
| user_id    | ForeignKey(users.id)    | The member     |
| joined_at  | DateTime                | When added     |

#### `tasks`

| Column      | Type                    | Description                           |
| ----------- | ----------------------- | ------------------------------------- |
| id          | Integer (PK)            | Auto-increment                        |
| title       | String                  | Task title                            |
| description | Text                    | Optional details                      |
| project_id  | ForeignKey(projects.id) | Belongs to project                    |
| assigned_to | ForeignKey(users.id)    | Who it's assigned to                  |
| created_by  | ForeignKey(users.id)    | Who created it                        |
| status      | String                  | `Todo` / `In Progress` / `Done` |
| priority    | String                  | `Low` / `Medium` / `High`       |
| due_date    | DateTime                | Optional deadline                     |
| created_at  | DateTime                | Creation time                         |
| updated_at  | DateTime                | Last update time                      |

### Relationships

```
User ──< ProjectMember >── Project
                                └──< Task >── User (assigned_to)
```

---

## 🔐 Role-Based Access Control

| Action                 | Admin    | Member                 |
| ---------------------- | -------- | ---------------------- |
| Create Project         | ✅       | ❌                     |
| Delete Project         | ✅       | ❌                     |
| Add Members to Project | ✅       | ❌                     |
| Create Tasks           | ✅       | ✅ (in their projects) |
| Delete Tasks           | ✅       | ❌                     |
| Update Task Status     | ✅       | ✅ (their own tasks)   |
| View Dashboard         | ✅ (all) | ✅ (own tasks only)    |
| View Projects          | ✅ (all) | ✅ (assigned only)     |

---

## 💻 How to Run Locally (VS Code Step-by-Step)

### ✅ Prerequisites

Make sure you have installed:

- **Python 3.10+** — download from https://python.org
- **VS Code** — download from https://code.visualstudio.com
- **Python extension for VS Code** — install from Extensions panel (Ctrl+Shift+X)

---

### 📥 Step 1: Download and Open the Project

1. Download the project ZIP file and **extract** it to a folder (e.g., `Documents/team_task_manager`)
2. Open **VS Code**
3. Click **File → Open Folder** and select the extracted folder `team_task_manager`
4. You should see all project files in the left sidebar

---

### 🖥️ Step 2: Open the Terminal in VS Code

Press **Ctrl + `** (backtick) OR go to **Terminal → New Terminal**

---

### 🐍 Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

---

### ▶️ Step 4: Activate the Virtual Environment

**On Windows:**

```bash
venv\Scripts\activate
```

**On Mac/Linux:**

```bash
source venv/bin/activate
```

After activation, you'll see `(venv)` at the start of your terminal line.

> ⚠️ If Windows shows an execution policy error, run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

### 📦 Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🗄️ Step 6: Run the App

```bash
python run.py
```

You should see:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

### 🌐 Step 7: Open in Browser

```
http://127.0.0.1:5000
```

Sign up with role **Admin** to get full access.

---

## ☁️ Deployment on Render

### Step 1: Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit - Team Task Manager"
git remote add origin https://github.com/GNANESWARKOKKIRALA/Team_task_manager.git
git push -u origin main
```

---

### Step 2: Create Account on Render

Go to **https://render.com** → Sign in with GitHub

---

### Step 3: Create New Web Service

1. Click **New +** → **Web Service**
2. Click **Connect a repository**
3. Select **Team_task_manager** → click **Connect**

---

### Step 4: Fill Configuration Settings

| Field         | Value                               |
| ------------- | ----------------------------------- |
| Name          | team-task-manager                   |
| Region        | Singapore                           |
| Branch        | main                                |
| Runtime       | Python 3                            |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn run:app`                |
| Instance Type | Free                                |

---

### Step 5: Add Environment Variables

Scroll to **Environment Variables** → click **Add Environment Variable**:

| Key                | Value                         |
| ------------------ | ----------------------------- |
| `SECRET_KEY`     | `gnaneswar-secret-key-2024` |
| `PYTHON_VERSION` | `3.11.0`                    |

> ⚠️ **Important:** Setting `PYTHON_VERSION=3.11.0` is required. Render defaults to Python 3.14 which is incompatible with SQLAlchemy 2.0.x.

---

### Step 6: Deploy

Click **Create Web Service** → wait 2–3 minutes → status shows **Live** ✅

Your app URL:

```
https://team-task-manager.onrender.com
```

---

### Step 7: Auto-Redeploy (After Any Code Change)

```bash
git add .
git commit -m "your update message"
git push
```

Render automatically redeploys on every push. ✅

---

### ⚠️ Render Free Tier Notes

| Issue                       | Explanation                                                   |
| --------------------------- | ------------------------------------------------------------- |
| First load takes 30–50 sec | Free tier sleeps after 15 min of inactivity — normal         |
| Database resets on redeploy | SQLite is file-based — use PostgreSQL for persistent data    |
| Python version must be set  | Always set `PYTHON_VERSION=3.11.0` in environment variables |

---

## 🔗 API / Route Reference

| Method   | Route                          | Description          | Access                |
| -------- | ------------------------------ | -------------------- | --------------------- |
| GET      | `/`                          | Dashboard            | Authenticated         |
| GET/POST | `/auth/signup`               | Register             | Public                |
| GET/POST | `/auth/login`                | Login                | Public                |
| GET      | `/auth/logout`               | Logout               | Authenticated         |
| GET      | `/projects/`                 | List all projects    | Authenticated         |
| GET/POST | `/projects/create`           | Create project       | Admin only            |
| GET      | `/projects/<id>`             | View project + tasks | Member of project     |
| POST     | `/projects/<id>/add_member`  | Add member           | Admin only            |
| POST     | `/projects/<id>/delete`      | Delete project       | Admin only            |
| GET/POST | `/tasks/create/<project_id>` | Create task          | Project member        |
| POST     | `/tasks/<id>/update_status`  | Update task status   | Assigned user / Admin |
| POST     | `/tasks/<id>/delete`         | Delete task          | Admin only            |

---

## 👨‍💻 Author

**Kokkirala Gnaneswara Anjani Prasad (Gap)**
B.Tech CSE | Tirumala Engineering College, 2026
GitHub: [github.com/GNANESWARKOKKIRALA](https://github.com/GNANESWARKOKKIRALA)
Portfolio: [gnaneswarkokkirala-portfolio.netlify.app](https://gnaneswarkokkirala-portfolio.netlify.app)

---

## 📄 License

This project is submitted as an academic assignment.
