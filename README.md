# Mini Leave Management System

**A quick, high-performance leave-management API powered by Python & FastAPI.**  
Built for startups (~50 employees) to easily add users, apply for leave, track balances, and light administrative operations.

---

## Project Demo
[Project Demo](https://leave-management-teal.vercel.app/docs)


## Table of Contents

1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Tech Stack](#tech-stack)  
4. [Getting Started](#getting-started)  
   - [Prerequisites](#prerequisites)  
   - [Installation](#installation)  
   - [Running the Application](#running-the-application)  
5. [Project Structure](#project-structure)  
6. [API Endpoints](#api-endpoints)  
7. [Edge Case Handling](#edge-case-handling)  
8. [Configuration](#configuration)  
9. [Contributing](#contributing)

---

## Project Overview

This project provides an MVP-level Leave Management API. Key functions include:

- Adding employees (Name, Email, Department, Joining Date)  
- Applying for, approving, or rejecting leave requests  
- Tracking individual leave balances  

The system emphasizes maintainable architecture, solid validation, and automatic documentation via FastAPI.

---

## Features

- **Employee Administration** – Create and manage employee records  
- **Leave Lifecycle** – Submit, approve, and reject leave requests  
- **Balance Management** – Accurate deduction and balance tracking  
- **Robust Validation** – Detect leave requests before joining date, overlapping entries, invalid date ranges, and imbalance  
- **Interactive Documentation** – Auto-generated via FastAPI’s Swagger UI and ReDoc  
- **Scalable Architecture** – Clean separation into models, schemas, business logic, and routing  

---

## Tech Stack

- **Python 3.8+**  
- **FastAPI** – for building fast, scalable APIs  
- **Pydantic** – for model validation and serialization  
- **Uvicorn** – ASGI server for development and production  

---

## Getting Started

### Prerequisites

- Python 3.8 or newer  
- Git (optional)  
- Virtual environment tool (`venv`, `pipenv`, or `poetry`)

### Installation

```bash
git clone https://github.com/<your-username>/mini-leave-management.git
cd mini-leave-management
python -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

## Open documentation:

Swagger UI: http://127.0.0.1:8000/docs

## Project Structure
```bash
mini-leave-management/
├── app/
│   ├── main.py              # FastAPI app and routers
│   ├── api/v1/
│   │   ├── employees.py     # Employee-related routes
│   │   └── leaves.py        # Leave request routes
│   ├── core/
│   │   └── config.py        # Settings and environment variables
│   ├── models/              # Database or in-memory models
│   ├── schemas/             # Pydantic schemas for validation
│   ├── services/            # Business logic layer
│   ├── dependencies.py      # Dependency injection setup
│   └── utils/               # Utility/helper functions
├── tests/                   # pytest tests for endpoints and logic
├── .env.example             # Sample environment variables
├── requirements.txt
└── README.md
```

## Edge Case Handling

* Disallows leave before the joining date
* Blocks leave exceeding the available balance
* Detects and rejects overlapping leave periods
* Grabs invalid date ranges (end date before start date)
* Handles non-existent employee IDs gracefully with clear error message

## Configuration
Setup environmental variables in .env:

```bash
PROJECT_NAME="Leave Management System"
API_V1_STR="/api/v1"
DATABASE_URL="sqlite:///./dev.db"
```
Use .env.example to guide setup without leaking sensitive info.

## Contributing
Contributions are welcome! To get started:

* Fork the project
* Create a feature branch (feature/your-feature)
* Adhere to existing code style and structure
* Write/update tests
* Document your changes
* Submit a pull request

## Made by
Yash Kumar
