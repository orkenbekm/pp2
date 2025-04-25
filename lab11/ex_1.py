import psycopg2
from tabulate import tabulate

conn = psycopg2.connect(
    host="localhost", dbname="postgres", user="postgres", password="123321", port="5432"
)
cur = conn.cursor()

cur.execute(
    """
CREATE TABLE IF NOT EXISTS phonebook (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    phone VARCHAR(20)
)
"""
)
conn.commit()


def search_pattern(pattern):
    cur.execute(
        "SELECT * FROM phonebook WHERE username LIKE %s OR phone LIKE %s",
        (f"%{pattern}%", f"%{pattern}%"),
    )
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Username", "Phone"], tablefmt="grid"))


def insert_or_update_user(username, phone):
    cur.execute(
        """
    INSERT INTO phonebook (username, phone) 
    VALUES (%s, %s)
    ON CONFLICT (username) DO UPDATE
    SET phone = EXCLUDED.phone;
    """,
        (username, phone),
    )
    conn.commit()
    print(f"User {username} has been added or updated")


def insert_many_users(usernames, phones):
    incorrect_data = []
    for username, phone in zip(usernames, phones):
        if len(phone) != 10:
            incorrect_data.append((username, phone))
        else:
            cur.execute(
                "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
                (username, phone),
            )
            conn.commit()

    if incorrect_data:
        print("Incorrect data found:")
        for data in incorrect_data:
            print(f"Username: {data[0]}, Phone: {data[1]}")
    else:
        print("All users have been added")


def query_data_with_pagination(limit, offset):
    cur.execute("SELECT * FROM phonebook LIMIT %s OFFSET %s", (limit, offset))
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Username", "Phone"], tablefmt="grid"))


def delete_data(value):
    cur.execute("DELETE FROM phonebook WHERE username=%s OR phone=%s", (value, value))
    conn.commit()
    print(f"Data with {value} has been deleted")


def menu():
    while True:
        print("\n PHONEBOOK MENU:")
        print("1. Search by pattern")
        print("2. Insert or update user")
        print("3. Insert many users")
        print("4. View / Search with pagination")
        print("5. Delete data by username or phone")
        print("0. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            pattern = input("Enter a name or phone number pattern to search: ")
            search_pattern(pattern)
        elif choice == "2":
            username = input("Enter username: ")
            phone = input("Enter phone number: ")
            insert_or_update_user(username, phone)
        elif choice == "3":
            usernames = input("Enter usernames as comma-separated values: ").split(",")
            phones = input("Enter phone numbers as comma-separated values: ").split(",")
            insert_many_users(usernames, phones)
        elif choice == "4":
            limit = int(input("Enter limit: "))
            offset = int(input("Enter offset: "))
            query_data_with_pagination(limit, offset)
        elif choice == "5":
            value = input("Enter username or phone to delete: ")
            delete_data(value)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")

    cur.close()
    conn.close()
    print("Connection closed.")


menu()
