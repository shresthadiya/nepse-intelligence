from getpass import getpass

from app.database import SessionLocal
from app.models import User
from app.core.security import hash_password


def create_user(db, username, email, password, role):
    existing_user = db.query(User).filter(
        (User.email == email) |
        (User.username == username)
    ).first()

    if existing_user:
        print(
            f"User already exists: {existing_user.username} "
            f"(role: {existing_user.role})"
        )
        return

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        role=role,
        is_active=True
    )

    db.add(user)
    db.commit()

    print(f"Created {role} account: {username}")


def seed_users():
    db = SessionLocal()

    try:
        print("Create Admin and Analyst accounts")
        print("----------------------------------")

        admin_password = getpass("Enter Admin password: ")
        analyst_password = getpass("Enter Analyst password: ")

        if not admin_password or not analyst_password:
            print("Passwords cannot be empty.")
            return

        create_user(
            db=db,
            username="admin",
            email="admin@example.com",
            password=admin_password,
            role="admin"
        )

        create_user(
            db=db,
            username="analyst",
            email="analyst@example.com",
            password=analyst_password,
            role="analyst"
        )

        print("\nUser seeding completed.")

    except Exception as error:
        db.rollback()
        print(f"Error creating users: {error}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_users()
