# Task Management API

## Overview
The **Task Management API** provides a platform where users can manage tasks, track their progress, and ensure they meet deadlines. Users can create, update, retrieve, and delete tasks, while also managing their authentication through token-based authentication. 

## Features
- **User Registration**: Users can register by providing a username, email, and password.
- **User Login**: Upon successful login, users are provided with a token to authenticate their subsequent requests.
- **User Logout**: Users can log out by invalidating their authentication token.
- **Task Management**: Users can perform CRUD (Create, Retrieve, Update, Delete) operations on tasks.
- **Authentication**: Token-based authentication is used for securing the API.

## Endpoints

### Authentication
- **Register**: `/api/users/` (POST) - Register a new user.
- **Login**: `/api/users/login/` (POST) - Authenticate a user and return an authentication token.
- **Logout**: `/api/users/logout/` (POST) - Log out a user and invalidate the token.

### Task Management
- **Create Task**: `/api/tasks/` (POST) - Create a new task.
- **Retrieve Task**: `/api/tasks/<id>/` (GET) - Get the details of a specific task.
- **Update Task**: `/api/tasks/<id>/` (PUT) - Update an existing task.
- **Delete Task**: `/api/tasks/<id>/` (DELETE) - Delete a task.
- **List Tasks**: `/api/tasks/` (GET) - Retrieve a list of all tasks.

### Example Request (Login)
```bash
POST /api/users/login/
Content-Type: application/json
{
    "email": "user@example.com",
    "password": "your_password"
}
