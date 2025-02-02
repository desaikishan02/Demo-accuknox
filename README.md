# Demo-accuknox

This project is a Django application with user authentication, friend request functionality, and more. It is containerized using Docker for easy deployment.
- Postman collection is added in to project's root folder.

## Features
User Login/Signup
- Login: Users can log in using their email (case insensitive) and password.
- Signup: Users can sign up with their email only. No OTP verification is required, but the email must be in a valid format.
- Authentication: All APIs except for signup and login require user authentication.
- Freiend Request: Send request, Accept Request, Reject Request, List friends, List pending request

## Prerequisites

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```
2. **Start Project**
   - Using docker
     
       ```bash
       docker-compose up --build
       ```

    - Start Directly
     
       ```bash
       pip install -r requirements.txt
       python manage.py makemigrations
       python manage.py migrate
       python manage.py runserver
       ```
