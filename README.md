# ToDoExtended

A Django-based advanced Todo application with enhanced features.

## Features

- User authentication and registration
- Task creation, update, and deletion
- Task filtering and searching
- User profiles with privacy settings
- Extended task management capabilities beyond basic todo apps

## Technologies Used

- Python 3
- Django Framework
- SQLite (default database)

## Installation

1. Clone the repository:

git clone https://github.com/Domino0D/ToDoExtended.git
cd ToDoExtended

2. Create and activate a virtual environment:

python -m venv env
source env/bin/activate # Linux/macOS
env\Scripts\activate # Windows

3. Install dependencies:

pip install -r requirements.txt

4. Apply migrations:

python manage.py migrate

5. Create a superuser:

python manage.py createsuperuser

6. Run the development server:

python manage.py runserver

7. Access the app at `http://127.0.0.1:8000/`

## Usage

- Register and log in to manage your tasks.
- Create, edit, delete, and filter tasks.
- Manage your profile and privacy settings.
- Use the search functionality to find tasks or users.


## Contributing

Contributions are welcome! Please fork the repo and submit pull requests.
