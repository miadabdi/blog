"""
One-time admin bootstrap: creates or promotes an admin user.

Run inside the app container:
    docker compose exec -e ADMIN_EMAIL=... -e ADMIN_PASSWORD=... app python scripts/create_admin.py
"""

import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlmodel import select  # noqa: E402

from src.auth.auth import AuthService
from src.auth.models import User
from src.auth.repository import UserRepository
from src.common.db import SessionLocal
from src.common.user_role import UserRole

# register all models so User's relationships can resolve
import src.post.models  # noqa: F401, E402
import src.project.models  # noqa: F401, E402


async def main() -> None:
    email = os.environ["ADMIN_EMAIL"]
    password = os.environ["ADMIN_PASSWORD"]

    auth = AuthService(UserRepository())
    hashed = await auth.get_password_hash(password)

    async with SessionLocal() as session:
        existing = (
            await session.exec(select(User).where(User.email == email))
        ).first()
        if existing:
            existing.role = UserRole.ADMIN
            existing.hashed_password = hashed
            session.add(existing)
            print(f"promoted existing user {email} to ADMIN")
        else:
            session.add(
                User(
                    email=email,
                    fname="Admin",
                    lname="User",
                    role=UserRole.ADMIN,
                    hashed_password=hashed,
                )
            )
            print(f"created ADMIN user {email}")
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
