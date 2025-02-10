from sqlmodel import Session, select
from database.models import Technology
from database.technology_seed_data import TECHNOLOGY_SEED_DATA
from database.db import engine


def seed_database():
    with Session(engine) as session:
        # Fetch existing technology names
        existing_names = {tech.name for tech in session.exec(select(Technology)).all()}

        # Filter out technologies that already exist
        new_technologies = [
            Technology(**data)
            for data in TECHNOLOGY_SEED_DATA
            if data["name"] not in existing_names
        ]

        if new_technologies:
            session.add_all(new_technologies)
            session.commit()
            print(f"Added {len(new_technologies)} new technologies.")
        else:
            print("Database already seeded.")


# Run the seeder
if __name__ == "__main__":
    seed_database()
