# Web-Task-Manager API
## Project Description
This project is a RESTful API for managing a simple ToDo list application, built with FastAPI. The application allows users to register, authenticate, and manage their tasks through a set of endpoints. Each user can create, update, delete, and retrieve tasks, as well as filter tasks based on status or mark them as completed. The API is secured with JWT-based authentication, ensuring that only authorized users can access the API.

The backend is powered by PostgreSQL for data storage, and the project includes Docker support for easy setup and deployment.

## Features
1. User Management:
    - user registration and authorization;
    - JWT-based authentication and authorization. 
2. Task Management:
    - CRUD operations for tasks (Create, Read, Update, Delete);
    - tasks are associated with users (owners).
3. Task Status:
    - tasks have statuses: "New", "In Progress", and "Completed";
    - endpoints to mark tasks as completed and filter tasks by status.
4. Pagination:
    - task lists are paginated for better performance.
5. Security:
    - only authenticated users can access the API and manage their own tasks.
6. Database:
    - uses PostgreSQL to store user and task data.
7. Testing:
    - unit tests for API endpoints.
8. Docker:
    - dockerized application for easy deployment.

## Installation and Setup
### Prerequisites
Make sure you have the following tools installed on your machine:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation 
1. Clone the repository to your local machine:
```bash
git clone https://github.com/sstanqq/web-task-manager.git
```
2. Navigate to the project directory:
```bash
cd web-task-manager
```
3. Configure the ```.env-non-dev``` environment file. This file is not included in the repository for security reasons. An example file is provided as ```.env-non-dev.example```

Copy the example file and configure it:
```bash
cp .env-non-dev.example .env-non-dev
```
Then open ```.env-non-dev``` and fill in the required environment variables(e.g., database connection, secret keys, etc.)

4. Build and run the containers:
```bash
docker-compose up --build
```
5. After the containers are up and running, the FastAPI server will be available at ```http://localhost:7777```.

### Environment Variables
The ```.env-non-dev``` file contains important configuration settings required for running the application within Docker containers. 

Example structure for ```.env-non-dev```:
```makefile
# Database connection settings
DB_HOST=db               
DB_PORT=5435          
DB_USER=postgres     
DB_PASS=postgres 
DB_NAME=postgres

# PostgreSQL settings
POSTGRES_DB=postgres          
POSTGRES_USER=postgres  
POSTGRES_PASSWORD=postgres 

# Application secret key (for JWT)
SECRET_KEY=9523975d376b81b3294f836ab538f84ccca25665b9188e850fb1313c6d53f42f

```
**Note:**
- The ```DB_PORT``` is set to ```5435```, which is the port configured for the database in the ```docker-compose.yaml``` file. There is usually no need to change this unless you modify the Docker setup.
- If you want to quickly run the application, you can leave the fields as they are in the example above.

## API Documentation
FastAPI automatically generates interactive API documentation. After the containers are up, you can access it via: 
- **Swagger UI**: http://localhost:7777/docs - detailed API documentation;
- **ReDoc**: http://localhost:7777/redoc - alternative API documentation.

## Example Requests
### User Authentication 
#### 1. Register User 
**Request:**
```bash
curl -X POST http://localhost:7777/auth/register \
-H "Content-Type: application/json" \
-d '{
    "first_name": "John",
    "last_name": "Doe",
    "username": "johndoe",
    "password": "securepassword"
}'
```
**Response:**
```json
{
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "username": "johndoe",
}
```

#### 2. Login User 
**Request:**
```bash
curl -X POST http://localhost:7777/auth/login \
-H "Content-Type: application/x-www-form-urlencoded" \
--data "username=johndoe&password=securepassword"
```
**Response:**
```json
{
    "access_token": "your_access_token_here",
    "token_type": "bearer"
}
```

### Task Management
#### 3. Get all Tasks

**Request:**
```bash
curl -X GET "http://localhost:7777/tasks?page=1&limit=10" \
-H "Authorization: Bearer your_access_token_here"
```
**Response:**
```json
[
    {
        "id": 1,
        "title": "Task 1",
        "description": "Description of Task 1",
        "status": "New",
        "user_id": 1
    },
    {
        "id": 2,
        "title": "Task 2",
        "description": "Description of Task 2",
        "status": "In Progress",
        "user_id": 1
    }
]
```

**Request:**
```bash
curl -X GET "http://localhost:7777/tasks?page=1&limit=10&status=Completed" \
-H "Authorization: Bearer your_access_token_here"
```
**Response:**
```json
[
    {
        "id": 1,
        "title": "Task 1",
        "description": "Description of Task 1",
        "status": "Completed",
        "user_id": 1
    }
]
```

#### 4. Get User Tasks 
**Request:**
```bash
curl -X GET "http://localhost:7777/tasks/user/1" \
-H "Authorization: Bearer your_access_token_here"
```
**Response:**
```json
[
    {
        "id": 1,
        "title": "User Task 1",
        "description": "Description of User Task 1",
        "status": "New",
        "user_id": 1
    },
    {
        "id": 2,
        "title": "User Task 2",
        "description": "Description of User Task 2",
        "status": "In Progress",
        "user_id": 1
    }
]
```

#### 5. Create Task 
**Request:**
```bash
curl -X POST http://localhost:7777/tasks \
-H "Content-Type: application/json" \
-H "Authorization: Bearer your_access_token_here" \
-d '{
    "title": "New Task",
    "description": "Description of the new task",
    "status": "New"
}'
```
**Response:**
```json
{
    "id": 3,
    "title": "New Task",
    "description": "Description of the new task",
    "status": "New",
    "user_id": 1
}
```

#### 6. Update Task 
**Request:**
```bash
curl -X PUT http://localhost:7777/tasks/1 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer your_access_token_here" \
-d '{
    "title": "Updated Task Title",
    "description": "Updated task description",
    "status": "In Progress"
}'
```
**Response:**
```json
{
    "id": 1,
    "title": "Updated Task Title",
    "description": "Updated task description",
    "status": "In Progress",
    "user_id": 1
}
```

#### 7. Delete Task 
**Request:**
```bash
curl -X DELETE http://localhost:7777/tasks/1 \
-H "Authorization: Bearer your_access_token_here"
```
**Response:**
```json
{
    "detail": "Task successfully deleted"
}
```

#### 8. Complete Task 
**Request:**
```bash
curl -X PATCH http://localhost:7777/tasks/1/complete \
-H "Authorization: Bearer your_access_token_here"
```
**Response:**
```json
{
    "id": 1,
    "title": "Task 1",
    "description": "Description of Task 1",
    "status": "Completed",
    "user_id": 1
}
```

## Testing 
If you want to run the tests locally, you can execute the following command:
```bash
python -m pytest tests/
```