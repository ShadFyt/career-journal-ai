from database.db import engine
from database.models import JournalEntry, Project, Technology
from starlette_admin.contrib.sqla import Admin, ModelView

admin = Admin(engine, title="Journal Entry Assistant")

admin.add_view(
    ModelView(
        Technology,
        identity="technology",
        name="Technologies",
        label="Technologies",
    ),
)
admin.add_view(
    ModelView(Project, identity="project", name="Projects", label="Projects")
)
admin.add_view(
    ModelView(
        JournalEntry,
        identity="journal-entry",
        name="Journal Entries",
        label="Journal Entries",
    )
)
