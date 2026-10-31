from getpass import getpass

from app.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password


def reset_admin_password():
    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == "analyst@example.com"
        ).first()

        if not user:
            print("Admin account not found.")
            return

        password = getpass("Enter new admin password: ")
        confirm = getpass("Confirm new admin password: ")

        if not password:
            print("Password cannot be empty.")
            return

        if password != confirm:
            print("Passwords do not match.")
            return

        user.password_hash = hash_password(password)

        db.commit()

        print("Admin password updated successfully.")

    except Exception as error:
        db.rollback()
        print("Error:", error)

    finally:
        db.close()


if __name__ == "__main__":
    reset_admin_password()