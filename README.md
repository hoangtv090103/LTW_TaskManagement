# LTW_TaskManagement

## Description

LTW_TaskManagement is a task management application built using Flask. It allows users to create, edit, delete, and manage tasks and projects. The application supports user authentication and provides a user-friendly interface for managing tasks and projects.

## Folder Structure
```plaintext
The repository has the following structure:
LTW_TaskManagement/
├── __pycache__/           # Compiled Python files
├── .gitignore             # Git ignore file
├── .idea/                 # IDE-specific files
├── app.py                 # Main entry point of the application
├── README.md              # Project description and instructions
├── requirements.txt       # List of dependencies
├── task_management/       # Main application code
│   ├── __init__.py        # Initializes the Flask application and its extensions
│   ├── db/                # Database files
│   ├── forms.py           # Defines the forms used in the application
│   ├── models.py          # Defines the database models
│   ├── project/           # Project-related views and templates
│   │   ├── __init__.py    # Initializes the project module
│   │   ├── forms.py       # Project-specific forms
│   │   ├── templates/     # Project-specific HTML templates
│   │   ├── views.py       # Defines the views for managing projects
│   ├── routes.py          # Defines the routes for the application
│   ├── static/            # Static files such as CSS, images, and JavaScript
│   ├── task/              # Task-related views and templates
│   ├── user/              # User-related views and templates
```
### Key Files and Directories

- [`app.py`]: The main entry point of the application.
- [`requirements.txt`]: Lists the dependencies required to run the application.
- [`task_management/`]: Contains the main application code.
  - [`__init__.py`]: Initializes the Flask application and its extensions.
  - [`db/`]: Contains the database files.
  - [`forms.py`]: Defines the forms used in the application.
  - [`models.py`]: Defines the database models.
  - [`project/`]: Contains the project-related views and templates.
    - [`views.py`]: Defines the views for managing projects.
  - [`routes.py`]: Defines the routes for the application.
  - `static/`: Contains static files such as CSS, images, and JavaScript.
  - [`task/`]: Contains the task-related views and templates.
  - [`user/`]: Contains the user-related views and templates.
