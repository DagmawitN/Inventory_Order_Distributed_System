Inventory & Order Distributed System
Project Description

The Inventory & Order Distributed System is a backend-focused distributed application designed to demonstrate microservices-based system design and asynchronous inter-service communication using RabbitMQ. The system separates core business functionality into independent services that communicate through message queues rather than direct calls, ensuring loose coupling, scalability, and fault tolerance.

This project was developed as part of a Distributed Systems course to apply theoretical concepts such as service decomposition, event-driven communication, containerization, and failure handling in a practical implementation.

System Architecture Overview

The system is composed of multiple independent services, each deployed in its own Docker container and connected through a shared message broker.

Core Components
1. Inventory Service

Manages product inventory and stock levels

Listens for order-related events from RabbitMQ

Updates inventory based on incoming messages

Publishes stock confirmation or rejection events

Implemented using Django REST Framework

2. Order Service

Handles order creation and order state management

Publishes order creation events to RabbitMQ

Consumes inventory response events

Updates order status based on inventory availability

3. Message Broker (RabbitMQ)

Acts as the communication backbone between services

Enables asynchronous, event-driven communication

Decouples services to improve reliability and scalability

Provides message durability and buffering during service failures

Communication Model

Services do not communicate via direct HTTP calls

All inter-service communication is handled through RabbitMQ

Messages are exchanged using:

Direct exchanges

Durable queues

JSON message payloads

Example Message Flow

Client sends a request to create an order

Order Service publishes an ORDER_CREATED event

Inventory Service consumes the event and checks stock

Inventory Service publishes a stock response event

Order Service consumes the response and updates order status

This design ensures loose coupling and supports service independence.

Distributed Systems Concepts Demonstrated

Microservices architecture

Asynchronous messaging

Event-driven system design

Service isolation and independence

Fault tolerance through message queues

Containerized deployment

Network-based service discovery (Docker DNS)

Technology Stack

Programming Language: Python

Backend Framework: Django, Django REST Framework

Message Broker: RabbitMQ

Containerization: Docker, Docker Compose

Database: Relational database (PostgreSQL or configured alternative)

Communication: REST (client-facing) + RabbitMQ (service-to-service)

Project Structure

Inventory_Order_Distributed_System/
│
├── services/
│   ├── inventory-service/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── manage.py
│   │   ├── .env
│   │   └── inventory/
│   │
│   ├── order-service/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── manage.py
│   │   ├── .env
│   │   └── order/
│   │
│   └── user-notification/
│       ├── Dockerfile
│       ├── docker-compose.yml
│       ├── .env
│       └── core/
│
├── README.md
└── .gitignore
