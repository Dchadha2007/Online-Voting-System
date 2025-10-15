### Environment Setup

This project uses a `.env` file to manage sensitive credentials.

1.  Create a file named `.env` in the root directory.
2.  Add the following variables with your details:

    ```
    # For your database connection
    DB_HOST="your_database_host"
    DB_USER="your_username"
    DB_PASS="your_password"
    DB_PORT="your_port"
    DB_NAME="your_database_name"

    # For the application's admin account
    ADMIN_USER="your_desired_admin_username"
    ADMIN_PASS="your_desired_admin_password"
    
    ```