"""Global test fixtures for all domains."""

import pytest
from database.session import SessionDep
from sqlmodel import Session, SQLModel, create_engine


@pytest.fixture(name="engine")
def engine_fixture():
    """Create a new database engine for testing.

    This fixture has session scope, meaning it's created once for the entire test session.
    """
    # Create engine
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        echo=False,  # Set to True for SQL debugging
    )
    # Create all tables
    SQLModel.metadata.create_all(engine)
    yield engine
    # Drop all tables after tests
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine):
    """Create a new database session for testing."""
    with Session(engine) as session:
        yield session
        session.rollback()


@pytest.fixture
def db_session(session) -> SessionDep:
    """Create a test database session with automatic rollback."""
    return session
