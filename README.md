# Play-Based Kindy Centre Management System

A web-based kindergarten management system developed using the Django framework to support the daily operations of a play-based kindergarten.

The system provides role-based access for **Administrators, Teachers, and Parents**, allowing each user type to access features relevant to their responsibilities.

This project was originally developed as a university semester project and has since been deployed online using Render and PostgreSQL.

## Live Demo

The system is currently deployed online:

https://play-based-kindy-centre-system.onrender.com

> The application is hosted on a free Render instance, so the first load may take a short while if the service has been inactive.

## Main Features

### Parent

- Create and manage parent account
- Register toddler information
- Choose schedules and activities
- Make and view payments
- Submit feedback
- View relevant toddler information

### Teacher

- Teacher dashboard
- Manage schedules and activities
- Record toddler attendance
- Manage toddler performance
- View and manage feedback

### Administrator

- Administrator dashboard
- Manage user registrations
- Manage toddler information
- Manage payment records
- Manage feedback
- Monitor system information

## Technologies Used

### Backend
- Python
- Django

### Frontend
- HTML
- CSS
- JavaScript
- Bootstrap

### Database
- SQLite (local development)
- PostgreSQL (production)

### Deployment
- Render
- Gunicorn
- WhiteNoise

### Development Tools
- Visual Studio Code
- Git
- GitHub

## System Architecture

The application follows Django's Model-View-Template (MVT) architecture.

The production version uses PostgreSQL for persistent data storage, while static files are served using WhiteNoise and the Django application is served using Gunicorn.

## User Roles

The system implements three primary user roles:

**Administrator**  
Responsible for managing registrations, toddler information, payments, feedback and administrative functions.

**Teacher**  
Responsible for managing schedules, activities, attendance, performance and feedback.

**Parent**  
Can register toddlers, choose activities and schedules, make payments and provide feedback.

## Demo Accounts

Demo accounts are available for testing the application.

For security reasons, administrator credentials are not publicly provided.

### Parent Demo

Username: admin_demo_2026

Password: childrenisourfuture

### Parent Demo

Username: parent_demo_2026

Password: childrenisourfuture

### Teacher Demo

Username: teacher_demo_2026

Password: childrenisourfuture

## Project Status

- Local development completed
- Role-based authentication implemented
- Parent module implemented
- Teacher module implemented
- Administrator module implemented
- PostgreSQL production database configured
- Application deployed online
- Live demo available

## Project Demonstration

A full system demonstration video is available here:

🎥 [Watch the Full System Demonstration](https://youtu.be/NmrZnb_2b90)

## Academic Project

This project was developed as part of a university software development project.

The project involved requirements analysis, system design, database design, implementation, testing and documentation.

## Security

Sensitive configuration values such as the Django secret key, database credentials and email credentials are managed using environment variables and are not stored in this repository.

The production database is separate from the original local development database.

## Author

Amanda James