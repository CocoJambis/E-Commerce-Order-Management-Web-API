# E-Commerce & Order Management Web API

A powerful, production-ready RESTful API for an e-commerce platform built with **FastAPI**, **SQLAlchemy ORM**, and **Pydantic v2**. This microservice handles complex relational database structures, user authentications, and transactional business logic like inventory deduction during order placement.

## 🚀 Key Features

- **Relational Order Management System:** Features complex table associations mapping relational joints between Users, Items (Catalog), and Orders.
- **Atomic Stock Transaction Logic:** Automatically verifies physical item availability in the warehouse before confirming an order, reducing quantities in real-time, and rolling back safely to ensure data consistency.
- **Decoupled Request/Response Payloads:** Built following the Data Transfer Object (DTO) pattern using **Pydantic v2** schemas to encapsulate internal entity states and protect sensitive columns.
- **Robust Endpoint Validation:** Leverages specialized field typings (`EmailStr`) and native web error formatting using `HTTPException` codes (e.g., `404 Not Found`, `400 Bad Request`).
- **Interactive API Playgrounds:** Full runtime inspection and request execution directly through built-in **Swagger UI** (`/docs`) and **ReDoc** suites.

---

## 🛠️ Architecture & Modularity

The project architecture enforces clean code principles and a strict **Separation of Concerns (SoC)**:

- **`main.py` (Controller/API Layer):** Manages routing configurations, captures network payload states, and handles declarative web exceptions.
- **`crud.py` (Persistence Layer):** Isolates the business logic and database operation workflows (queries, updates, stock manipulation).
- **`models.py` (Entity & Schema Layer):** Maps object-relational schemas (inheriting from an abstract base class to share standard constraints) alongside Pydantic verification structures.
- **`db.py` (Infrastructure Layer):** Handles connection engine lifecycles and provides managed transactions per HTTP request via Dependency Injection (`Depends(get_db)`).

### Tech Stack
* **Framework:** FastAPI 
* **Validation:** Pydantic v2
* **ORM Framework:** SQLAlchemy
* **Database Engine:** SQLite / PostgreSQL Ready

---

## 📋 Relational Database Schema Highlights

### 1. `users` (Account Registry)
* Tracks user authentication mappings, credentials, and structural profile parameters.

### 2. `items` (Product Catalog)
* Stores product inventory identifiers, base catalog names, prices, and available stocks.

### 3. `orders` & `order_items` (Transactional Layers)
* Implements multi-table relations linking user receipts with order tracking, computing quantities purchased, item variations, and transactional historical states.