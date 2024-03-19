import psycopg

# setting up database connection parameters
DB_NAME = "a3"
USER = "postgres"
HOST = "localhost"
PASSWORD = "student"

# establishing a connection to the database
def establish_connection():
    try:
        connection = psycopg.connect(
            dbname=DB_NAME, user=USER, host=HOST, password=PASSWORD
        )
    except psycopg.OperationalError as e:
        print(f"failed to connect to the database: {e}")
        exit(1)
    return connection

# retrieving and displaying all records from the students table
def retrieve_all_students():
    try:
        with establish_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM students")
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
    except psycopg.DatabaseError as e:
        print(f"error while accessing the database: {e}")

# adding a new student record to the students table
def insert_new_student():
    first_name = input("Enter the student's first name: ")
    last_name = input("Enter the student's last name: ")
    email = input("Enter the student's email: ")
    enrollment_date = input("Enter the student's enrollment date (YYYY-MM-DD): ")
    try:
        with establish_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)",
                    (first_name, last_name, email, enrollment_date),
                )
                print(f"added {first_name} {last_name} to the students table")
                connection.commit()
    except psycopg.DatabaseError as e:
        print(f"error while accessing the database: {e}")

# updating the email address of a student
def modify_student_email():
    student_id = input("Enter the student's id: ")
    new_email = input("Enter the student's new email: ")
    try:
        with establish_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE students SET email = %s WHERE student_id = %s",
                    (new_email, student_id),
                )
                print(f"updated email for student {student_id} to {new_email}")
                connection.commit()
    except psycopg.DatabaseError as e:
        print(f"error while accessing the database: {e}")

# deleting a student record
def remove_student():
    student_id = input("Enter the student's id: ")
    try:
        with establish_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
                print(f"deleted student {student_id}")
                connection.commit()
    except psycopg.DatabaseError as e:
        print(f"error while accessing the database: {e}")

# displaying the main menu and getting the user's choice
def display_menu():
    menu = [
        {"option": "1", "message": "Retrieve all students", "action": retrieve_all_students},
        {"option": "2", "message": "Insert a new student", "action": insert_new_student},
        {"option": "3", "message": "Modify a student's email", "action": modify_student_email},
        {"option": "4", "message": "Remove a student", "action": remove_student},
    ]

    for item in menu:
        print(f"{item['option']}. {item['message']}")

    user_choice = input("Enter your choice: ")
    print("\n")

    for item in menu:
        if user_choice == item["option"]:
            item["action"]()
            break
    else:
        print("invalid choice")

# main function
if __name__ == "__main__":
    while True:
        display_menu()