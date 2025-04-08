import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user_management.database import Base, get_db  

# Set up the test database URL
SQLALCHEMY_TEST_DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost/handicraft"

# Set up the engine and session for testing
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the test database
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Creates a new database session for each test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()  
        db.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Provides a TestClient instance with the test database."""
    from fastapi.testclient import TestClient
    from user_management.main import app  # Adjust with your app import
    app.dependency_overrides[get_db] = lambda: db_session
    return TestClient(app)
