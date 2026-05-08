# Project Context: Python & Django Learning Workspace

This workspace is a structured environment for learning Python and Django, combining educational theory, practice exercises, and a real-world project development (`todo_project`).

## 1. Project Overview

### **Educational Structure**
The workspace is organized into "Phases" for progressive learning:
- **Phase A (Khởi động):** Environment setup and basics.
- **Phase B (Nền tảng):** Syntax, execution flow, and basic logic.
- **Phase C (Collections):** Data structures (lists, dicts, sets) and modularity.
- **Phase D (OOP):** Object-Oriented Programming concepts.
- **Django Docs:** Comprehensive notes on Django MVT, ORM, Templates, and Forms.

### **The Todo Project (`todo_project/`)**
A functional "Todo List" application built with Django.
- **Framework:** Django 4.2.30
- **Database:** MySQL (`todo_db`) with `pymysql`.
- **Key Features:**
    - Task management (CRUD).
    - Project categorization for tasks.
    - Status filtering (Active/Done).
    - Modal-based creation for Projects and Tasks.
    - Template inheritance using a modular structure (`base_pro.html`, `header.html`, `sidebar.html`, etc.).

## 2. Technical Setup

### **Environment**
- **Python Version:** 3.x
- **Virtual Environment:** Located at `todo_project/.venv/`.
- **Database:** Local MySQL instance on port 3306.
    - DB Name: `todo_db`
    - User: `root`
    - Password: `12345678` (configured in `settings.py`).

### **Core Commands**
Run these commands from within the `todo_project/` directory:
- **Activate Venv:** `source .venv/bin/activate`
- **Run Server:** `python manage.py runserver`
- **Database Migrations:**
    - `python manage.py makemigrations`
    - `python manage.py migrate`
- **Create Admin:** `python manage.py createsuperuser`

## 3. Development Conventions & Workflow

### **GSD (Get-Shit-Done) Workflow**
This project follows a specialized AI-driven workflow defined in `gsd-guide.md`.
- **Process:** Discuss -> Plan -> Execute -> Verify.
- **Key Files for GSD:**
    - `.planning/`: Directory for AI planning state (usually filtered out in PRs).
    - `ROADMAP.md`: High-level project goals.
    - `STATE.md`: Current progress state.
- **Mandate:** Always use `/gsd-do` or specific GSD commands when initiating feature development to maintain consistency and a clean git history.

### **Coding Standards**
- **Views:** Prefer Function-Based Views (FBV) for simplicity, following the learning roadmap.
- **Models:** Use Descriptive `__str__` methods.
- **Error Handling:** Use `get_object_or_404()` for all object retrievals in views.
- **Templates:** Use modular components (in `templates/tasks/components/`) and template inheritance.

## 4. Key Documentation
- `gsd-guide.md`: Detailed instructions for the GSD workflow.
- `todo_project/00-SETUP-LOG.md`: Step-by-step log of how the Django project was built.
- `django-docs/`: In-depth explanations of Django concepts (Migrations, Models, Views, etc.).

## 5. Current Focus
The project is currently in the **Django Templates & Forms** phase, focusing on building a polished UI and handling complex filtering and editing logic within the `home_page` view.
