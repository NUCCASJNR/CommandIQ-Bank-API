# CommandIQ-Bank-API


___Welcome to the Event-Sourced CQRS Banking System,
a modern backend architecture designed for scalability, 
flexibility, and real-time financial data processing.
This system leverages Event Sourcing and Command Query Responsibility Segregation (CQRS)
to provide a robust foundation for managing user accounts, transactions,
and financial data.___


- **Create a virtual environment**
  - ```python
    python3 -m venv env_name
    ```

- **Activate the virtual environment***
  - ```python
    source env_name/bin/activate
    ```
- **Install the project requirements**
  - ```python
    pip install -r requirements.txt
    ```

- **Setup The MySql database**
  - ```sql
    cat setup_mysql_dev.sql | sudo mysql -p
    ```
- **Set the environment variables, You can just copy it and paste it in your .env file**
  - ```bash
    BANK_USER='bank_user'
    BANK_DB='bank_db'
    BANK_HOST='localhost'
    BANK_PWD='bank_pwd'
    SECRET_KEY='Your django secret key'
    ELASTIC_EMAIL_KEY="Your Elastic email API key"
    ```
    
- **Create tables**
  - ```python
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

# API Endpoint Documentation

## Authentication-related Views

### User Registration

#### Endpoint Details

- **View:** user_registration_view
- **URL:** /auth/register/
- **Method:** POST
- **Description:** Registers a new user.

### This endpoint is used to sign up a new user. The request should be sent as an HTTP POST to the specified URL. The request body should be of form-data type and include the following parameters:
- **email (text)**: The email address of the user.
- **username (text)**: The desired username for the user. 
- **password (text)**: The password for the user account. 
- **last_name (text)**: The last name of the user. 
- **first_name (text)**: The first name of the user.

#### The response to the request will have a status code of 201, indicating that the request was successful. The response will include the following fields:
- **message**: A message indicating the result of the signup process. 
- **username**: The username of the newly signed up user. 
- **email**: The email address of the newly signed up user.



