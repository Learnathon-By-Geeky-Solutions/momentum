# 🧶 Handicraft

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-blue?style=for-the-badge&logo=postgresql&logoColor=blue&labelColor=black)](https://www.postgresql.org/)
[![ShadCn](https://img.shields.io/badge/Shadcn%2FUi%20-%20black?style=for-the-badge&logo=shadcnui)](https://ui.shadcn.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Next.Js](https://img.shields.io/badge/Next.js-black?style=for-the-badge&logo=%23000000)](https://nextjs.org/docs)
[![Github Action](https://img.shields.io/badge/Github%20Actions%20-%20black?style=for-the-badge&logo=githubactions&logoColor=blue&labelColor=white&color=black)](https://github.com/features/actions)
[![Typescript](https://img.shields.io/badge/Typescript%20-%20black?style=for-the-badge&logo=Typescript)]()

![Architecture Diagram](images/banner.jpg)

<h2 align="center">🌾 From Rural Hands to Global Hearts 🌍</h2>

<p align="center">
  <b>Handicraft</b> is a purpose-driven e-commerce platform that connects rural artisans directly with global customers — empowering local creators and delivering authentic, handcrafted goods with transparency and trust.
</p>

# 🔍 What is Handicraft?

<p align="center">
  <img src="images/logo.jpg" alt="Handicraft Logo" width="20%" />
</p>

**Handicraft** is a purpose-driven e-commerce platform that bridges the gap between **rural artisans** and **global customers**.  
By removing middlemen, we ensure that the true creators — the talented hands behind each product — receive fair recognition and value for their craftsmanship.

With a focus on:

- 🌍 **Transparency**
- 🎨 **Authenticity**
- 🤝 **Community Empowerment**

Handicraft creates a sustainable ecosystem where **tradition meets technology**.  
Whether you're a customer seeking unique, handmade goods or a rural producer looking for a wider market, **Handicraft** is your trusted digital marketplace.

## 📖 Table of Contents

 - [**Team Members**](#-team-members)
 - [**Product Tour**](#-product-tour)
 - [**Features**](#-features)
 - [**🛠 Project Design Overview**](#-project-design-overview)
    - [**🏛 System Architecture**](#1-system-architecture)
    - [**🛠 Technical Architecture**](#2--technical-architecture)
    - [**🗃 Database Design (ERd)**](#3--database-design-erd)
 - [**Tech Stacks**](#tech-stacks)
    - [**Frontend Tech Stack**](#%EF%B8%8F-frontend-tech-stack)
    - [**Backend Tech Stack**](#-backend-tech-stack)
    - [**Authentication Tech Stack**](#-authentication-tech-stack)
    - [**Devops Infrastructure**](#-devops--infrastructure)
 - [**Project Structure**](#-project-structure)
 - [**Getting Started**](#getting-started)
 - [**API Documentation**](#-api-documentation)
    - [**🛰️ Live API Docs**](#-live-api-docs)
 - [**Environment Variables**](#-environment-variables)
 - [**Running Tests**](#-running-tests)
 - [**Deployment with Docker**](#-deployment-with-docker)
 - [**Contributing**](#-contributing)
 - [**License**](#-license)


## 👥 Team Members

- [![Static Badge](https://img.shields.io/badge/Jamil%20Ahmed%20-Team%20Leader%20-%20red?style=for-the-badge&logo=github&logoColor=white&labelColor=black&color=Red)](https://github.com/JamilAhmed00)
- [![Member - 2](https://img.shields.io/badge/Emdadul%20Islam%20-%20black?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mdadul)

- [![Member - 3](https://img.shields.io/badge/Shajjad%20Gani%20Shovon-%20black?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ShajjadGani)


## 👨🏻‍🏫 Mentor: 

- [![Mentor](https://img.shields.io/badge/MD.%20Arif%20Istiake%20Sunny%20-%20Mentor%20-%20red?style=for-the-badge&logo=github&logoColor=white&labelColor=black)](https://github.com/Sunny1509006)


## 🎥 Product Tour

[![Project-Demo](https://img.shields.io/badge/Demo-Handicraft-Green?style=for-the-badge&color=%23FFA500&)](https://learnathon-by-geeky-solutions.github.io/momentum/)


## ✨ Features

### 🧑‍🎨 Artisan Features

- ***Post Creation:*** Ability to create and manage product listings.

- ***Brand Creation:*** Create and manage their own brand profile.

- ***Profile Creation:*** Set up and personalize an artisan profile.

- ***Price Comparison:*** View prices of similar products to stay competitive in the market.

### 👨‍💻 Customer Features
- ***Profile Creation:*** Create and manage their customer profile.
- ***Product/Posts Viewing:*** Browse products or artisan posts.
- ***Order and Purchase:*** Place orders and make purchases directly through the platform.

### 🛠️ Admin Features
- ***Monitor Platform Activities:*** Track and oversee all activities of customers and artisans.
- ***Vulnerability Prevention:*** Ensure the platform's security and smooth functioning by identifying and fixing potential issues.
- ***Content Moderation:*** Review and approve posts from artisans and customers to ensure quality and compliance with platform standards.


# 🛠 Project Design Overview
## 1. System Architecture

![Architecture Diagram](images/System_Architecture.png)

### Overview
- **User Interaction**:
  - Users can sign up and log in either as **Artisans** or **Customers**.
- **Front-End**:
  - Handles user authentication, artisan/customer dashboards, admin panel, product listings, search, filters, and responsive design.
- **Back-End**:
  - Manages authentication, profiles, product CRUD, brand creation, order management, admin monitoring, and semantic analysis.
- **Security**:
  - Secure API access using **JWT Tokens**.
- **Validation**:
  - Input and output data validated via **Pydantic Models**.
- **Database**:
  - Stores users, products, brands, orders, billing information, and chats.
- **Storage**:
  - Handles image and logo uploads using **MinIO** storage service.


## 2. 🛠 Technical Architecture

![Architecture Diagram](images/System_design.png)

### 🖥 Front-End
- **Frameworks**: React.js, Next.js
- **Language**: TypeScript
- **UI Libraries**: TailwindCSS, ShadcnUI
- **State Management**: Tanstack Query
- **API Communication**: Axios
- **Features**:
  - User authentication and authorization
  - Artisan and Customer dashboards
  - Product listing, filtering, searching
  - Admin monitoring panel
  - Fully responsive and optimized for various devices

### ⚙️ Back-End
- **Framework**: FastAPI (Python)
- **Authentication**:
  - OAuth 2.0, JWT Token-based secure authentication
- **Data Validation**:
  - Pydantic models for request/response validation
- **Core Modules**:
  - User & Profile Management
  - Product Management (CRUD)
  - Brand Management
  - Order Processing
  - Admin Monitoring & Semantic Analysis

---

### 🛢 Database
- **Type**: PostgreSQL
- **Managed Entities**:
  - Users, Brands, Products, Orders, Bills

---

### 🗄 Storage
- **Object Storage**: MinIO
- **Used For**:
  - Product images
  - Brand logos
  - Other media uploads

---

### 🔐 Security
- JWT (JSON Web Tokens) for secure authentication
- Password hashing and validation
- Role-based access control for Admin, Artisan, and Customer users

---

### 🧠 Additional Features
- **Semantic analysis** module for intelligent data handling.
- Admin tools for monitoring product and user activities.


## 3. 🗃 Database Design (ERD)

![Architecture Diagram](images/ERD.png)

### 📋 Overview

- **User Table**:
  - Stores user information like username, email, password, phone, and address.
  - Supports third-party login via Google (google_id).
  - Tracks user roles (artisan, customer, admin) and account verification status.
  
- **Brand Table**:
  - Each brand is linked to a user (artisan).
  - Stores brand name, description, logo, and creation date.

- **Product Table**:
  - Each product is linked to a brand.
  - Stores product details such as name, images, videos, category, description, pricing, order size/quantity, and approval status.
  
- **Order Table**:
  - Represents orders placed by users (customers).
  - Tracks order status and creation date.

- **OrderTeam Table**:
  - Links an order with multiple products.
  - Stores product-specific details within an order: size, quantity, phone number, and delivery address.

- **Bill Table**:
  - Linked to orders for billing management.
  - Stores transaction details: amount, payment method, transaction ID, billing status, and creation date.

## Tech Stacks

## 🖥️ Frontend Tech Stack

Our frontend is built using modern, powerful, and scalable technologies designed for performance, maintainability, and great user experience.

| Technology | Description |
|------------|-------------|
| ![ReactJS](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=white&style=flat-square) | **ReactJS:** A JavaScript library for building fast, dynamic user interfaces with reusable components. |
| ![Next.js](https://img.shields.io/badge/Next.js-000000?logo=next.js&logoColor=white&style=flat-square) | **Next.js:** A React framework for server-side rendering and static site generation, optimizing performance and SEO. |
| ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white&style=flat-square) | **TypeScript:** A superset of JavaScript that adds static typing, improving code quality and error prevention. |
| ![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwindcss&logoColor=white&style=flat-square) | **TailwindCSS:** A utility-first CSS framework for rapid UI development with customizable design systems. |
| ![ShadcnUI](https://img.shields.io/badge/Shadcn_UI-000000?logo=vercel&logoColor=white&style=flat-square) | **ShadcnUI:** A UI component library focused on accessibility and design, providing ready-to-use components. |
| ![TanStack Query](https://img.shields.io/badge/TanStack_Query-FF4154?logo=reactquery&logoColor=white&style=flat-square) | **TanStack Query:** A data-fetching library that simplifies managing and syncing server data in React apps. |
| ![Axios](https://img.shields.io/badge/Axios-5A29E4?logo=axios&logoColor=white&style=flat-square) | **Axios:** A promise-based HTTP client for making API requests, handling responses, and managing errors. |

## 🧩 Backend Tech Stack

The backend is built using robust Python-based tools and a powerful relational database to ensure speed, scalability, and maintainability.

| Technology | Description |
|------------|-------------|
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white&style=flat-square) | **FastAPI:** A modern, fast web framework for building APIs with Python, based on standard Python type hints and asynchronous programming. |
| ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-CA1F27?logo=python&logoColor=white&style=flat-square) | **SQLAlchemy:** A powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python, enabling easy database interaction and management. |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white&style=flat-square) | **PostgreSQL:** An open-source, highly extensible relational database system, known for its reliability, data integrity, and support for complex queries. |


## 🔐 Authentication Tech Stack

We use modern and secure methods to authenticate users and handle data exchange in our application.

| Technology | Description |
|------------|-------------|
| ![JWT](https://img.shields.io/badge/JWT-000000?logo=json-web-tokens&logoColor=white&style=flat-square) | **JWT Tokens:** JSON Web Tokens (JWT) are a compact, URL-safe way to represent claims between two parties. Used for secure user authentication and data exchange, JWTs are commonly used in API authentication systems. |
| ![OAuth 2.0](https://img.shields.io/badge/OAuth_2.0-6A6A6A?logo=oauth&logoColor=white&style=flat-square) | **OAuth 2.0:** A widely-used open standard for access delegation, commonly used for secure user authentication and authorization, allowing users to grant access to their resources without sharing their credentials. |


## 🚀 DevOps & Infrastructure

Our project is built and deployed using a modern DevOps stack, enabling continuous delivery, high availability, and efficient debugging in production.

| Tool | Description |
|------|-------------|
| ![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white&style=flat-square) | Distributed version control system for source code management. |
| ![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white&style=flat-square) | Code hosting, issue tracking, and collaborative development platform. |
| ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?logo=githubactions&logoColor=white&style=flat-square) | CI/CD pipeline used to build, test, and deploy code automatically. |
| ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&style=flat-square) | Containerization platform to build, ship, and run apps anywhere. |
| ![Caddy](https://img.shields.io/badge/Caddy-3788D8?logo=caddy&logoColor=white&style=flat-square) | Modern web server with automatic HTTPS, used as a reverse proxy. |
| ![Cloudflare](https://img.shields.io/badge/Cloudflare-F38020?logo=cloudflare&logoColor=white&style=flat-square) | CDN and DNS services with security features like DDoS protection. |
| ![DigitalOcean](https://img.shields.io/badge/DigitalOcean-0080FF?logo=digitalocean&logoColor=white&style=flat-square) | Cloud infrastructure provider hosting our production environment. |
| ![Sentry](https://img.shields.io/badge/Sentry-362D59?logo=sentry&logoColor=white&style=flat-square) | Real-time error tracking and monitoring to help debug production issues. |
| ![Locust](https://img.shields.io/badge/Locust-000000?logo=python&logoColor=white&style=flat-square) | Open-source load testing tool used to measure performance and scalability. |

---


## 📁 Project Structure

```bash
  momentum/
    ├── .git/
    ├── .github/
    ├── .vscode/
    ├── .pytest_cache/
    ├── frontend/                   # Next.js Frontend Application
    │   ├── app/
    │   ├── components/
    │   ├── constant/
    │   ├── hooks/
    │   ├── lib/
    │   ├── provider/
    │   ├── public/
    │   ├── .next/
    │   ├── node_modules/
    │   ├── package.json
    │   ├── tailwind.config.ts
    │   └── various config files
    │
    ├── backend/                    # Python Backend Application
    │   ├── app/
    │   ├── tests/
    │   ├── alembic/                # Database migrations
    │   ├── venv/
    │   ├── requirements.txt
    │   ├── docker-compose.yml
    │   ├── Dockerfile
    │   └── various config files
    │
    ├── docs/
    ├── images/
    ├── daily-activity/
    ├── README.md
    └── LICENSE
```


## Getting Started
## 🧰 Requirements

To run this project locally or in production, ensure the following tools are installed:

| Tool | Version |
|------|---------|
| ![Python](https://img.shields.io/badge/Python-3.12.2%2B-3776AB?logo=python&logoColor=white&style=flat-square) | Python 3.12.2 or higher |
| ![Node.js](https://img.shields.io/badge/Node.js-20%2B-339933?logo=node.js&logoColor=white&style=flat-square) | Node.js 20 or higher |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-4169E1?logo=postgresql&logoColor=white&style=flat-square) | PostgreSQL (latest recommended) |
| ![Docker](https://img.shields.io/badge/Docker-Latest-2496ED?logo=docker&logoColor=white&style=flat-square) | Docker (latest stable) |


**Backend Setup**
```bash
  cd backend
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  uvicorn app.main:app --reload
```
**Frontend Setup**
```bash
  cd frontend
  npm install
  npm start
```
**🐳 Docker Setup**
```bash
docker compose build
docker compose up -d
docker compose down
```

## 📘 API Documentation

This section provides access to the full API documentation for the Handicraft platform. You can explore all available endpoints, request/response formats, authentication methods, and more.

### 🔗 Live API Docs

[![Swagger UI Docs](https://img.shields.io/badge/API-Swagger_UI-blue?logo=swagger)](https://api.handi-craft.xyz/docs#/)
[![ReDoc API Reference](https://img.shields.io/badge/API-ReDoc_Reference-orange?logo=readthedocs)](https://api.handi-craft.xyz/redoc)

- **Swagger UI** – Interactive API playground where you can try out endpoints and see responses in real-time.
- **ReDoc Reference** – Clean, structured, and searchable API reference documentation powered by ReDoc.

For any issues or questions regarding the API, please contact the development team or open an issue in the repository.


## 🔐 Environment Variables

Create a .env file in both backend/ and frontend/ directories with the following variables:

**Backend (.env)**
```env
  DATABASE_URL=postgresql://user:password@localhost:5432/momentum_db
  SECRET_KEY=your_secret_key
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=30
```
**Frontend (.env)**
```env
  REACT_APP_API_URL=http://localhost:8000
```


## 🧪 Running Tests

To run tests, run the following command

**Backend Tests**
```bash
  cd backend
  pytest
```

**Frontend Tests**
```bash
  cd frontend
  npm test
```


## 📦 Deployment with Docker

To deploy the application using Docker:

```bash
  docker-compose up --build

```
## 🤝 Contributing

We welcome contributions from the community! Follow these steps to contribute:

| Step | Command |
|------|---------|
| ![Fork](https://img.shields.io/badge/🔱-Fork_Repository-blue?style=flat-square) | Fork the repository to your GitHub account. |
| ![Branch](https://img.shields.io/badge/🌿-Create_New_Branch-green?style=flat-square) | `git checkout -b feature/your-feature-name` |
| ![Commit](https://img.shields.io/badge/💾-Commit_Changes-9cf?style=flat-square) | `git commit -m 'Add your message'` |
| ![Push](https://img.shields.io/badge/📤-Push_Branch-orange?style=flat-square) | `git push origin feature/your-feature-name` |
| ![PR](https://img.shields.io/badge/🚀-Open_Pull_Request-purple?style=flat-square) | Submit a pull request for review. |

> 🧠 **Tip:** Make sure to follow the coding standards and check for any open issues before starting work.

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](./LICENSE) file for details.
