# Manufacturing Inventory Management System

## Case Study Submission

Candidate: Shashank Pravinbhai Chauhan  
Submitted To: NTT Data Company  
Purpose: Interview / Job Selection Round  

---

## 1. Project Overview

This project is a full-stack Manufacturing Inventory Management System built using a microservices architecture.

The system enables manufacturing organizations to:

- Manage raw materials and finished goods
- Perform full CRUD operations
- Monitor stock levels
- Configure threshold limits
- Detect low stock conditions
- View real-time inventory summaries

The architecture is modular, scalable, and designed following REST principles.

---

## 2. Architecture

The application follows a microservices-based architecture:

React Frontend  
        |  
        v  
API Gateway (Port 5000)  
        |  
        |-------------------------  
        |                        |  
        v                        v  
Inventory Service (5001)    Alert Service (5002)  
        |  
        v  
MySQL Database  

### Services

1. Inventory Service  
   - Handles all CRUD operations  
   - Connects to MySQL database  
   - Provides inventory summary  

2. Alert Service  
   - Communicates with Inventory Service via REST  
   - Detects low stock items  
   - Provides alert endpoints  

3. API Gateway  
   - Single entry point for frontend  
   - Routes requests to respective services  
   - Enables centralized control and scalability  

---

## 3. Technology Stack

Frontend:
- React.js
- Axios
- CSS

Backend:
- Python
- Flask
- Flask-CORS
- Requests (for inter-service communication)

Database:
- MySQL

Architecture:
- Microservices pattern
- REST-based inter-service communication
- API Gateway pattern

---

## 4. Features Implemented

- Full CRUD operations
- Inventory summary dashboard
- Low stock detection based on configurable threshold
- RESTful API design
- Microservices separation
- Independent service deployment capability
- Clean modular backend structure

---

## 5. API Endpoints

### Inventory Service

| Method | Endpoint | Description |
|--------|----------|------------|
| GET | /inventory | Retrieve all inventory items |
| POST | /inventory | Add new inventory item |
| PUT | /inventory/{id} | Update inventory item |
| DELETE | /inventory/{id} | Delete inventory item |
| GET | /inventory/summary | Get inventory summary |

### Alert Service

| Method | Endpoint | Description |
|--------|----------|------------|
| GET | /alerts/low-stock | Retrieve low stock items |

---

## 6. How to Run Locally

Step 1: Start Inventory Service

cd inventory-service  
python app.py  

Runs on: http://127.0.0.1:5001

Step 2: Start Alert Service

cd alert-service  
python app.py  

Runs on: http://127.0.0.1:5002

Step 3: Start API Gateway

cd api-gateway  
python app.py  

Runs on: http://127.0.0.1:5000

Step 4: Start Frontend

cd frontend  
npm install  
npm start  

Runs on: http://localhost:3000

Frontend communicates only with API Gateway.

---

## 7. Design Decisions

- Implemented microservices architecture to ensure modularity and scalability.
- Used REST-based communication between services.
- Separated business responsibilities into distinct services.
- Introduced API Gateway for centralized routing.
- Maintained independent deployment capability for each service.

---

## 8. Future Enhancements

- Role-based authentication and authorization
- Email or SMS notification service
- Docker containerization
- CI/CD integration
- Cloud deployment
- Event-driven communication using message broker

---

## 9. Conclusion

This system fulfills all case study requirements:

- RESTful backend service
- CRUD operations
- Inventory summary interface
- Alert configuration using threshold logic
- Microservices architecture emphasis
- Proper documentation

The system is designed to be scalable, modular, and production-ready with minimal extension effort.

---

## Repository Link

Add deployed GitHub repository link here.
