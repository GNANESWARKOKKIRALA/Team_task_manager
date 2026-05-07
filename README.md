# 🗂️ Team Task Manager — Full-Stack Web App

> A full-stack project management web application with **role-based access control (Admin/Member)**, built with **Flask + SQLAlchemy + SQLite**, deployed on **Render**.

---

## 📌 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Database Design (ER Diagram)](#database-design)
6. [Role-Based Access Control](#role-based-access-control)
7. [How to Run Locally (VS Code Step-by-Step)](#how-to-run-locally)
8. [Deployment on Railway](#deployment-on-railway)
9. [API / Route Reference](#api--route-reference)
10. [Screenshots](#screenshots)
11. [Author](#author)

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

| Feature | Description |
|---|---|
| ✅ Authentication | Signup / Login / Logout with hashed passwords |
| ✅ Role-Based Access | Admin can create projects, add members, delete tasks; Member can view and update their tasks |
| ✅ Project Management | Create projects, view members, track task counts |
| ✅ Task Management | Create tasks with priority (High/Medium/Low), due date, assignment |
| ✅ Status Tracking | Kanban-style board: Todo → In Progress → Done |
| ✅ Overdue Detection | Auto-detects and highlights overdue tasks on dashboard |
| ✅ Dashboard | Overview of all stats: total tasks, completed, in-progress, overdue |
| ✅ Deployment | Live on Railway via Gunicorn |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Flask Jinja2 Templates + Bootstrap 5 |
| **Backend** | Flask (Python) — REST-style routes |
| **Database** | SQLite (via SQLAlchemy ORM) |
| **Auth** | Flask-Login + Werkzeug password hashing |
| **Deployment** | Railway + Gunicorn |

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
├── Procfile                    # Railway deployment command
├── .gitignore
└── README.md
```

---

## 🗄️ Database Design

### Tables

#### `users`
| Column | Type | Description |
|---|---|---|
| id | Integer (PK) | Auto-increment |
| username | String | Unique username |
| email | String | Unique email |
| password_hash | String | Bcrypt hashed password |
| role | String | `Admin` or `Member` |
| created_at | DateTime | Registration time |

#### `projects`
| Column | Type | Description |
|---|---|---|
| id | Integer (PK) | Auto-increment |
| name | String | Project name |
| description | Text | Optional description |
| owner_id | ForeignKey(users.id) | Admin who created it |
| status | String | Active / Completed / Archived |
| created_at | DateTime | Creation timestamp |

#### `project_members` (Join Table)
| Column | Type | Description |
|---|---|---|
| id | Integer (PK) | Auto-increment |
| project_id | ForeignKey(projects.id) | The project |
| user_id | ForeignKey(users.id) | The member |
| joined_at | DateTime | When added |

#### `tasks`
| Column | Type | Description |
|---|---|---|
| id | Integer (PK) | Auto-increment |
| title | String | Task title |
| description | Text | Optional details |
| project_id | ForeignKey(projects.id) | Belongs to project |
| assigned_to | ForeignKey(users.id) | Who it's assigned to |
| created_by | ForeignKey(users.id) | Who created it |
| status | String | `Todo` / `In Progress` / `Done` |
| priority | String | `Low` / `Medium` / `High` |
| due_date | DateTime | Optional deadline |
| created_at | DateTime | Creation time |
| updated_at | DateTime | Last update time |

### Relationships

```
User ──< ProjectMember >── Project
                                └──< Task >── User (assigned_to)
```

---

## 🔐 Role-Based Access Control

| Action | Admin | Member |
|---|---|---|
| Create Project | ✅ | ❌ |
| Delete Project | ✅ | ❌ |
| Add Members to Project | ✅ | ❌ |
| Create Tasks | ✅ | ✅ (in their projects) |
| Delete Tasks | ✅ | ❌ |
| Update Task Status | ✅ | ✅ (their own tasks) |
| View Dashboard | ✅ (all) | ✅ (own tasks only) |
| View Projects | ✅ (all) | ✅ (assigned only) |

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

You should see a terminal at the bottom of VS Code.

---

### 🐍 Step 3: Create a Virtual Environment

In the terminal, type:

```bash
python -m venv venv
```

This creates a `venv/` folder — a private Python environment for this project.

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

> ⚠️ If Windows shows an error about execution policy, run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

### 📦 Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs Flask, SQLAlchemy, Flask-Login, Gunicorn, etc.

Wait for all packages to install (takes 1–2 minutes on first run).

---

### 🗄️ Step 6: Run the App

```bash
python run.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

### 🌐 Step 7: Open in Browser

Open your browser and go to:
```
http://127.0.0.1:5000
```

You will be redirected to the **Login page**.

---

### 👤 Step 8: Create Your First Account

1. Click **Sign up** on the login page
2. Enter username, email, password
3. Select role: **Admin** (to get full access)
4. Click **Create Account**
5. Login with those credentials

---

### 🧪 Step 9: Test the App

1. **As Admin:**
   - Go to Projects → New Project
   - Open the project → Add Task
   - Create a second Member account, add them to the project

2. **As Member:**
   - Login with the member account
   - View assigned tasks
   - Update task status using the dropdown

---

### 🔄 Restart Tips

Every time you restart VS Code:
1. Open terminal (Ctrl + `)
2. Activate venv: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. Run: `python run.py`

---

## ☁️ Deployment on Railway

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit - Team Task Manager"
git remote add origin https://github.com/YOUR_USERNAME/team-task-manager.git
git push -u origin main
```

### Step 2: Deploy on Railway
1. Go to https://railway.app and sign in with GitHub
2. Click **New Project → Deploy from GitHub Repo**
3. Select your repository
4. Railway auto-detects Python and reads `Procfile`
5. Click **Deploy**

### Step 3: Get Live URL
- After deployment, click **Settings → Generate Domain**
- Your app is live at: `https://your-app.railway.app`

### Environment Variables on Railway
Set these in Railway → Variables:
```
SECRET_KEY=your-strong-random-secret-key-here
```

---

## 🔗 API / Route Reference

| Method | Route | Description | Access |
|---|---|---|---|
| GET | `/` | Dashboard | Authenticated |
| GET/POST | `/auth/signup` | Register | Public |
| GET/POST | `/auth/login` | Login | Public |
| GET | `/auth/logout` | Logout | Authenticated |
| GET | `/projects/` | List all projects | Authenticated |
| GET/POST | `/projects/create` | Create project | Admin only |
| GET | `/projects/<id>` | View project + tasks | Member of project |
| POST | `/projects/<id>/add_member` | Add member | Admin only |
| POST | `/projects/<id>/delete` | Delete project | Admin only |
| GET/POST | `/tasks/create/<project_id>` | Create task | Project member |
| POST | `/tasks/<id>/update_status` | Update task status | Assigned user / Admin |
| POST | `/tasks/<id>/delete` | Delete task | Admin only |

---

## 📸 Screenshots

> Dashboard, Project Kanban Board, Login — all rendered via Flask Jinja2 + Bootstrap 5

---

## 👨‍💻 Author

**Kokkirala Gnaneswara Anjani Prasad (Gap)**  
B.Tech CSE | Tirumala Engineering College, 2026  
GitHub: [github.com/GNANESWARKOKKIRALA](https://github.com/GNANESWARKOKKIRALA)  
Portfolio: [gnaneswarkokkirala-portfolio.netlify.app](https://gnaneswarkokkirala-portfolio.netlify.app)

---

## 📄 License

This project is submitted as an academic assignment.
