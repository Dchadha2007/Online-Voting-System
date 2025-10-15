# Secure CLI Voting System 🗳️

http://googleusercontent.com/image_generation_content/0

A robust and secure command-line voting system built with Python and backed by a MySQL database. This application simulates a real-world electronic voting process, focusing on security, data integrity, and role-based access control.

---

## 🌟 Key Features

-   🔐 **Secure User Authentication**: Complete user registration and login system to ensure only registered voters can participate.
-   🤫 **Confidential Password Entry**: Uses the `pwinput` library to mask password entry, protecting user credentials from being seen on screen.
-   🗳️ **One-Vote Integrity**: Each user is permitted to cast only one vote, preventing duplicate voting and ensuring fair results.
-   👨‍💼 **Role-Based Access Control**: A separate, secure login for an **Admin** who has exclusive privileges to view election results.
-   📊 **Real-Time Results**: The admin panel can display up-to-the-minute voting statistics, including vote counts and percentage distribution for each party.
-   🗄️ **Persistent Data Storage**: All user data, voting status, and results are securely stored in a MySQL database, ensuring data is saved between sessions.

---

## 🛠️ Technologies Used

-   **Backend**: Python 3
-   **Database**: MySQL
-   **Key Python Libraries**:
    -   `mysql-connector-python`
    -   `pwinput`
    -   `python-dotenv`

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

You will need the following installed on your system:
-   Python 3.8 or higher
-   A running MySQL Server (either local or a cloud service like Aiven)

### Installation Steps

1.  **Clone the Repository**
    Open your terminal and clone the repository:
    ```bash
    git clone [https://github.com/Dchadha2007/Online-Voting-System.git](https://github.com/Dchadha2007/Online-Voting-System.git)
    cd Online-Voting-System
    ```

2.  **Install Dependencies**
    Install the required Python libraries using pip:
    ```bash
    pip install mysql-connector-python pwinput python-dotenv
    ```

3.  **Set Up Environment Variables**
    This project uses a `.env` file to securely manage database and admin credentials.
    -   Create a file named `.env` in the root directory of the project.
    -   Copy and paste the following content into the `.env` file and replace the values with your own credentials.

    ```
    # --- Database Credentials ---
    DB_HOST="your_database_host"
    DB_USER="your_database_username"
    DB_PASS="your_database_password"
    DB_PORT="your_database_port"
    DB_NAME="your_database_name"

    # --- Admin Credentials ---
    ADMIN_USER="your_admin_username"
    ADMIN_PASS="your_admin_password"
    ```

4.  **Run the Application**
    Execute the main script from your terminal:
    ```bash
    python voting.py
    ```
    The script will automatically create the necessary tables in your database when you run it for the first time.

---

## 📝 How to Use

Once the application is running, you will be presented with the main menu.

1.  **Register**: First-time users must register with a unique username and a password.
2.  **Login**: Registered users can log in to access the voting panel.
3.  **Vote**: After logging in, users can cast their vote for one of the listed parties.
4.  **View Results (Admin Only)**:
    -   Select this option and enter the admin credentials you set in your `.env` file.
    -   The admin can view detailed voting results and statistics.
5.  **Exit**: Securely exit the application.

---

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.
