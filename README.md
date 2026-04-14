# bug-free-guacamole

A RESTful Todo API built with Flask, SQLAlchemy, Marshmallow, and JWT authentication.

> **Note:** This guide is written for Linux users, specifically Ubuntu.

---

## Prerequisites

Before getting started, ensure you have the following installed:

- **Python 3.12.3** — [Download here](https://www.python.org/downloads/)
- **uv package manager** — [Installation guide](https://github.com/astral-sh/uv)

> **Important:** If you have a different version of Python installed, update the version in `.python-version` before running any installation commands. You may also need to update the Python version in `pyproject.toml` to match.

---

## Installation

**1. Clone the repository:**

```bash
git clone git@github.com:Gklelei/bug-free-guacamole.git
cd bug-free-guacamole
```

**2. Create the virtual environment:**

```bash
uv venv
```

**3. Activate the virtual environment:**

```bash
source .venv/bin/activate
```

**4. Install dependencies:**

```bash
uv sync
```

---

## Database Migration

After installation, set up your database by running the existing migrations:

```bash
flask db upgrade
```

This will create all the necessary tables in the database. If you make changes to the models in the future, generate and apply new migrations with:

```bash
flask db migrate -m "describe your changes"
flask db upgrade
```

---

## Seeding the Database

To populate the database with sample data for development and testing, run the seed script from the project root:

```bash
python -m app.seed.seed
```

This will create:
- **5 users** with randomly generated names and emails
- **10 todos** randomly assigned to those users with varying statuses

All seeded users share the same password for convenience:

```
password: password1234
```

To log in with a seeded user, check your database for any email and use `password1234` as the password.

> **Note:** Run migrations before seeding — the tables must exist first.

---

## Running the Application

Before running, go through this checklist:

- [ ] Virtual environment is created and activated
- [ ] Correct Python version is set in `.python-version`
- [ ] Dependencies are installed via `uv sync`
- [ ] Database migrations have been applied

**Set the Flask app entry point:**

```bash
export FLASK_APP=main.py
```

**Start the server:**

```bash
flask run
```

The server will start at `http://localhost:5000`.

---

## Available Routes

### Auth Routes

All auth routes are prefixed with `/api/auth`.

#### Register User
- **Method:** `POST`
- **URL:** `http://localhost:5000/api/auth/register`
- **Request Body:**
```json
{
  "name": "John Doe",
  "email": "johndoe@gmail.com",
  "password": "yourpassword"
}
```
- **Success Response:**
```json
{
  "message": "User created successfully"
}
```

---

#### Login
- **Method:** `POST`
- **URL:** `http://localhost:5000/api/auth/login`
- **Request Body:**
```json
{
  "email": "johndoe@gmail.com",
  "password": "yourpassword"
}
```
- **Success Response:**
```json
{
  "message": "Login successful"
}
```
> A JWT token is set as an `access_token_cookie` cookie on successful login.

---

#### Verify Token (Check Session)
- **Method:** `GET`
- **URL:** `http://localhost:5000/api/auth/validate-token`
- **Auth Required:** Yes
- **Request Body:** None
- **Success Response:**
```json
{
  "id": 4,
  "name": "John Doe",
  "email": "johndoe@gmail.com"
}
```

---

#### Logout
- **Method:** `POST`
- **URL:** `http://localhost:5000/api/auth/logout`
- **Auth Required:** Yes
- **Request Body:** None
- **Success Response:**
```json
{
  "message": "Logout successful"
}
```

---

### Todo Routes

All todo routes are prefixed with `/api/todos`. **All routes require the user to be logged in.**

#### Create Todo
- **Method:** `POST`
- **URL:** `http://localhost:5000/api/todos`
- **Request Body:**
```json
{
  "title": "Assignment",
  "description": "Optional description",
  "status": "PENDING"
}
```
- **Success Response:**
```json
{
  "message": "Todo Created Successfully"
}
```

---

#### Get User Todos
- **Method:** `GET`
- **URL:** `http://localhost:5000/api/todos`
- **Request Body:** None
- **Success Response:**
```json
[
  {
    "id": 3,
    "title": "Assignment",
    "description": "Continue reading 28 commandments",
    "status": "PENDING",
    "user_id": 4
  }
]
```

---

#### Update Todo
- **Method:** `PATCH`
- **URL:** `http://localhost:5000/api/todos/<todo_id>`
- **Request Body:** (all fields optional)
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "STARTED"
}
```
- **Success Response:**
```json
{
  "message": "Todo updated successfully",
  "data": {
    "id": 3,
    "title": "Updated title",
    "description": "Updated description",
    "status": "STARTED",
    "user_id": 4
  }
}
```

---

#### Delete Todo
- **Method:** `DELETE`
- **URL:** `http://localhost:5000/api/todos/<todo_id>`
- **Request Body:** None
- **Success Response:**
```json
{
  "message": "Todo Deleted Successfully"
}
```

---

## Todo Status Values

Valid values for the `status` field are:

- `PENDING`
- `STARTED`
- `COMPLETED`
- `FAILED`

---

## Dependencies

```
faker>=40.13.0
flask>=3.1.3
flask-bcrypt>=1.0.1
flask-jwt-extended>=4.7.1
flask-marshmallow>=1.4.0
flask-migrate>=4.1.0
flask-restful>=0.3.10
flask-sqlalchemy>=3.1.1
marshmallow>=4.3.0
marshmallow-sqlalchemy>=1.5.0
pytest>=9.0.3
python-dotenv>=1.2.2
sqlalchemy>=2.0.49
```