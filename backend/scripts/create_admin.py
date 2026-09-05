import getpass
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database.connection import SessionLocal
from app.models.user import User, UserRole, AccountStatus
from app.core.security import hash_password


def main():
    print("\n=== SIH Admin Account Creation ===\n")
    name = input("Admin name: ").strip()
    email = input("Admin email: ").strip().lower()
    password = getpass.getpass("Admin password: ")
    confirm_password = getpass.getpass("Confirm password: ")

    if not name or not email:
        print("Name and email are required.")
        return
    if len(password) < 8:
        print("Password must contain at least 8 characters.")
        return
    if password != confirm_password:
        print("Passwords do not match.")
        return

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print("An account with this email already exists.")
            return

        admin = User(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role=UserRole.ADMIN,
            account_status=AccountStatus.ACTIVE,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(f"\nAdmin account created successfully. ID: {admin.id}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
