from database.db import create_db_and_tables, engine
from database.models import Technology, User
from database.technology_seed_data import TECHNOLOGY_SEED_DATA
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


async def seed_database():
    async with AsyncSession(engine) as session:
        # Fetch existing technology names
        result = await session.exec(select(Technology))
        users_result = await session.exec(select(User))
        all_users = users_result.all()
        if not all_users:
            print("No users found in the database. Cannot seed technologies.")
            return

        technologies_to_add = []
        users_processed_count = 0

        for user in all_users:
            users_processed_count += 1
            # Fetch existing technology names for the current user
            existing_tech_result = await session.exec(
                select(Technology.name).where(Technology.user_id == user.id)
            )
            existing_user_tech_names = {name for name in existing_tech_result.all()}

            # Determine which technologies are new for this user
            for tech_data in TECHNOLOGY_SEED_DATA:
                if tech_data["name"] not in existing_user_tech_names:
                    # Create a new Technology instance associated with the current user
                    new_tech = Technology(**tech_data, user_id=user.id)
                    technologies_to_add.append(new_tech)

        # Add all the new technologies for all users in a single transaction
        if technologies_to_add:
            session.add_all(technologies_to_add)
            await session.commit()
            print(
                f"Added {len(technologies_to_add)} new technology entries "
                f"across {users_processed_count} users."
            )
        else:
            print("Technologies already seeded for all users.")


# Run the seeder
if __name__ == "__main__":
    import asyncio

    asyncio.run(create_db_and_tables())
    asyncio.run(seed_database())
