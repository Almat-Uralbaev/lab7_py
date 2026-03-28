import csv
from connect import get_connection



def insert_from_csv(file_path):
    conn = get_connection()
    cur = conn.cursor()

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row['name'], row['phone'])
            )

    conn.commit()
    cur.close()
    conn.close()


def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


def update_contact(old_name, new_name=None, new_phone=None):
    conn = get_connection()
    cur = conn.cursor()

    if new_name:
        cur.execute(
            "UPDATE phonebook SET name=%s WHERE name=%s",
            (new_name, old_name)
        )

    if new_phone:
        cur.execute(
            "UPDATE phonebook SET phone=%s WHERE name=%s",
            (new_phone, old_name)
        )

    conn.commit()
    cur.close()
    conn.close()


def search_contacts(name=None, phone_prefix=None):
    conn = get_connection()
    cur = conn.cursor()

    if name:
        cur.execute(
            "SELECT * FROM phonebook WHERE name ILIKE %s",
            ('%' + name + '%',)
        )
    elif phone_prefix:
        cur.execute(
            "SELECT * FROM phonebook WHERE phone LIKE %s",
            (phone_prefix + '%',)
        )
    else:
        cur.execute("SELECT * FROM phonebook")

    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


def delete_contact(value):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE name=%s OR phone=%s",
        (value, value)
    )

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    while True:
        print("\n1. Import CSV")
        print("2. Add contact")
        print("3. Update contact")
        print("4. Search")
        print("5. Delete")
        print("6. Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_from_csv("contacts.csv")

        elif choice == "2":
            insert_from_console()

        elif choice == "3":
            name = input("Old name: ")
            new_name = input("New name (or leave empty): ")
            new_phone = input("New phone (or leave empty): ")

            update_contact(
                name,
                new_name if new_name else None,
                new_phone if new_phone else None
            )

        elif choice == "4":
            name = input("Search name (or empty): ")
            prefix = input("Phone prefix (or empty): ")

            results = search_contacts(
                name if name else None,
                prefix if prefix else None
            )

            for r in results:
                print(r)

        elif choice == "5":
            value = input("Enter name or phone to delete: ")
            delete_contact(value)

        elif choice == "6":
            break