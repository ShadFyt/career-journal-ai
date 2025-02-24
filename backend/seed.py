from database.db import create_db_and_tables, engine
from database.models import Technology
from database.technology_seed_data import TECHNOLOGY_SEED_DATA
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


async def seed_database():
    async with AsyncSession(engine) as session:
        # Fetch existing technology names
        result = await session.exec(select(Technology))
        existing_names = {tech.name for tech in result.all()}

        # Filter out technologies that already exist
        new_technologies = [
            Technology(**data)
            for data in TECHNOLOGY_SEED_DATA
            if data["name"] not in existing_names
        ]

        if new_technologies:
            session.add_all(new_technologies)
            await session.commit()
            print(f"Added {len(new_technologies)} new technologies.")
        else:
            print("Database already seeded.")


# Run the seeder
if __name__ == "__main__":
    import asyncio

    asyncio.run(create_db_and_tables())
    asyncio.run(seed_database())
