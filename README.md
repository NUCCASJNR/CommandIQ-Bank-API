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
    
