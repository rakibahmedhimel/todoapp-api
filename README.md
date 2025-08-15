# ToDoApp API

This is a RESTful API built using Python, FastAPI, and SQLAlchemy for managing tasks in a to-do application. It allows users to create, read, update, and delete tasks (CRUD operations). The application also features user authentication and integrates with a MySQL database.

## Features
- **User Authentication**: Secure sign-up and login using JWT (JSON Web Tokens).
- **Task Management**: Users can create, update, and delete tasks.
- **Task Filtering**: Tasks can be filtered by status, priority, and due date.
- **Database**: Uses MySQL to store user and task information, with Alembic for database migrations.
- **Error Handling**: Proper error responses for invalid inputs and failed operations.
- **Voice Feedback**: Interactive feedback system integrated for specific operations (like success or failure of task creation).

## Technologies Used
- **FastAPI**: Web framework for building the API.
- **SQLAlchemy**: ORM for database interaction.
- **MySQL**: Database for storing user and task data.
- **Alembic**: Database migration tool for SQLAlchemy.
- **Pydantic**: Data validation for request bodies and responses.
- **JWT**: Token-based authentication for secure login and user management.
- **Pytest**: Testing framework for unit and integration tests.


## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/todoapp-api.git
   
2. **Install dependencies:**
Create a virtual environment and install the required libraries:
  cd todoapp-api
  python -m venv venv
  source venv/bin/activate  # On Windows use venv\Scripts\activate
  pip install -r requirements.txt

3. **Database Setup:**
Create a MySQL database named todoapplicationdatabase or update the SQLALCHEMY_DATABASE_URL in alembic.ini to reflect your MySQL credentials.
Run migrations to set up the database schema:
  alembic upgrade head

4. **Run the API:**
Start the FastAPI application:
  uvicorn main:app --reload
The API will be available at http://127.0.0.1:8000.

5. **Testing:**
You can run tests using pytest:
 pytest
