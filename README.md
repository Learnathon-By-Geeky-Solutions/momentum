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
 - [**Project Structure**](#-project-structure)
 - [**Getting Started**](#getting-started)
 - [**API Documentation**](#-api-documentation)
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
  - JWT Token-based secure authentication
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

### Frontend 
- ***ReactJS:***  A JavaScript library for building fast, dynamic user interfaces with reusable components.
- ***NextJs:*** A React framework for server-side rendering and static site generation, optimizing performance and SEO.
- ***Typescript:***  A superset of JavaScript that adds static typing, improving code quality and error prevention.
- ***TailwindCSS:*** A utility-first CSS framework for rapid UI development with customizable design systems.
- ***ShadcnUi:*** A UI component library focused on accessibility and design, providing ready-to-use components.
- ***Tanstack Query:*** A data-fetching library that simplifies managing and syncing server data in React apps.
- ***Axios:*** A promise-based HTTP client for making API requests, handling responses, and managing errors.

### Backend
- ***FastAPI:*** A modern, fast web framework for building APIs with Python, based on standard Python type hints and asynchronous programming.
- ***SQLAlchemy:*** A powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python, enabling easy database interaction and management.
- ***PostgreSQL:*** An open-source, highly extensible relational database system, known for its reliability, data integrity, and support for complex queries.

### Authentication 
- ***JWT Tokens:*** JSON Web Tokens (JWT) are a compact, URL-safe way to represent claims between two parties. Used for secure user authentication and data exchange, JWTs are commonly used in API authentication systems.

### DevOps
- ***Docker:*** A platform that automates the deployment of applications inside lightweight, portable containers, ensuring consistency across environments.
- ***GitHub Actions:*** A CI/CD tool integrated with GitHub for automating workflows like testing, building, and deploying code directly from your repository.

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
**Prerequisites**
- Python 3.12.2+
- Node.js 20+
- PostgreSQL
- Docker (optional)

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

- Fork the repository.
- Create a new branch: git checkout -b feature/your-feature-name.
- Commit your changes: git commit -m 'Add your message'.
- Push to the branch: git push origin feature/your-feature-name.
- Open a pull request.



## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](./LICENSE) file for details.
