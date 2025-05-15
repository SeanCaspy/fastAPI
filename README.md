# 🚀 FastAPI Blog Project – Educational Dockerized App

This is an **educational backend project** built with **FastAPI**, **MySQL**, and **Docker**.
It demonstrates how to create a full-featured backend API with user authentication, token management, and CRUD operations – all containerized using `docker-compose`.

---

## 🛠️ Technologies Used

* **FastAPI** – Python-based high-performance web framework
* **MySQL** – Relational database
* **SQLAlchemy** – ORM for database models
* **Pydantic** – For data validation
* **Docker & Docker Compose** – Containerization of app and database
* **JWT (JSON Web Tokens)** – Authentication system

---

## 🌐 Features

* User **registration**, **login**, and **JWT authentication**
* Secure **access tokens** and **refresh tokens**
* Protected endpoints for authenticated users
* **CRUD** operations for blog posts
* API documentation via **Swagger UI** (`/docs`)

---

## 📁 Project Structure

```
.
├── app/                      # FastAPI app (main.py, routers, models, auth, etc.)
├── Dockerfile                # Docker build config for FastAPI
├── docker-compose.yml        # Define services (app + MySQL)
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables
```

---

## ⚙️ Environment Variables (`.env`)

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://<user>:<password>@db:3306/<db_name>
MYSQL_DATABASE=<db_name>
MYSQL_USER=<user>
MYSQL_PASSWORD=<password>
MYSQL_ROOT_PASSWORD=<root_password>
```

---

## 🐳 Running with Docker Compose

Build and start the app and database:

```bash
docker-compose up --build
```

Stop and clean up all containers and volumes:

```bash
docker-compose down -v
```

---

## 🌍 Access the Application

Once running locally:

* API root: [http://localhost:8000](http://localhost:8000)
* Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📚 Purpose

This project is part of a personal learning journey to understand full-stack backend development with containers. It aims to simulate a real-world application setup with secure practices and modular design.
