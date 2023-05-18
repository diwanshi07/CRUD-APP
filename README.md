# DjangoProject
# Project Name

## Introduction
Consider a store which has an inventory of boxes which are all cuboid(which have length, breadth and height). Each Cuboid has been added by a store employee who is associated as the creator of the box even if it is updated by any user later on. 

## Installation
1. Clone the repository:
  -> $ git clone https://github.com/your-username/your-project.git
2. Navigate to the project directory:
  -> cd your-project
3. Create a virtual environment (optional but recommended):
  -> $ python3 -m venv env
4. Activate the virtual environment:
   For Windows:
     $ env\Scripts\activate
   For macOS/Linux:
     $ source env/bin/activate
5. Install the project dependencies:
  -> $ pip install -r requirements.txt
6. Set up the database:
   -> Run commands
      export DATABASE_URL = <database_url>
      python manage.py migrate
7. Create a superuser (if applicable):
   -> $ python manage.py createsuperuser
8. Start the development server:
   -> $ python manage.py runserver
9.  Open your web browser and access the project at http://localhost:8000      




## Testing
This project includes automated tests to ensure its functionality and reliability. The following test cases cover different aspects of the project:

- **Test Case 1**: [Creation of Box]
  - [If invalid dimensions are provided the server will theow an error]

- **Test Case 2**: [filters for showing list]
  - [appropriate filters applicable on fetching the list of boxes]

- **Test Case 3**: [Deleting the box]
  - [Providing correct id for deleting the box]
  
- **Test Case 4**: [Updating the box]
  - [Providing correct id for updating the box details]
  
You can run the tests using the following command:
