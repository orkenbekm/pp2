import psycopg2
import csv
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

cur.execute("ALTER SEQUENCE phonebook_id_seq RESTART WITH 1")
conn.commit()


def insert_manual():
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    cur.execute(
        "INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (name, phone)
    )
    conn.commit()
    print("Added")


def insert_csv():
    path = input("Enter the path to the CSV file: ")
    try:
        with open(path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2:
                    cur.execute(
                        "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
                        (row[0], row[1]),
                    )
            conn.commit()
            print("Added from CSV")
    except Exception as error:
        print("Error:", error)


def update_entry():
    old_name = input("Enter the name of the user to update: ")
    new_name = input("New name: ")
    new_phone = input("New phone: ")
    cur.execute(
        "UPDATE phonebook SET username=%s, phone=%s WHERE username=%s",
        (new_name, new_phone, old_name),
    )
    conn.commit()
    print("Updated")


def delete_entry():
    value = input("Enter username or phone to delete: ")
    cur.execute("DELETE FROM phonebook WHERE username=%s OR phone=%s", (value, value))
    conn.commit()
    print("Deleted")


def query_data():
    filter_value = input(
        "Enter username or phone to search (press enter to view all): "
    )
    if filter_value:
        cur.execute(
            "SELECT * FROM phonebook WHERE username=%s OR phone=%s",
            (filter_value, filter_value),
        )
    else:
        cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Username", "Phone"], tablefmt="grid"))


def clear_and_reset():
    agreement = input("Are you sure you want to clear table and reset ID? (yes/no): ")
    if agreement.lower() == "yes":
        cur.execute("DELETE FROM phonebook")
        cur.execute("ALTER SEQUENCE phonebook_id_seq RESTART WITH 1")
        conn.commit()
        print("All data cleared and ID reset")
    else:
        print("Cancelled")


def menu():
    while True:
        print("\n PHONEBOOK MENU:")
        print("1. Add manually")
        print("2. Add from CSV")
        print("3. Update entry")
        print("4. Delete entry")
        print("5. View / Search")
        print("6. Clear Table and reset ID")
        print("0. Exit")

        choice = input("Choose an option: ")
        if choice == "1":
            insert_manual()
        elif choice == "2":
            insert_csv()
        elif choice == "3":
            update_entry()
        elif choice == "4":
            delete_entry()
        elif choice == "5":
            query_data()
        elif choice == "0":
            break
        elif choice == "6":
            clear_and_reset()
        else:
            print("Invalid. Try again.")

    cur.close()
    conn.close()
    print("Connection")


menu()
