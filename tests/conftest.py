import pytest
from app import create_app
from app.extensions import db
from sqlalchemy_utils import database_exists, create_database, drop_database


@pytest.fixture(scope="session")
def app():
    """
    Fixture to set up and tear down the Flask application for testing purposes. This fixture
    creates an app instance with specific configurations for testing by enabling the
    'testing' mode and setting up a test database. It ensures that the database tables are
    created before the tests are run and properly cleaned up afterward.
    """
    app = create_app(testing=True) # assumes a 'testing=True' config option is added to create_app()
    # Create the database tables for tests
    with app.app_context():
        db.create_all()
        yield app # this is where the testing happens!
        db.drop_all() # cleanup after the test


@pytest.fixture(scope="function")
def session(app):
    """
    Provides a pytest fixture to manage a database session for testing purposes. This fixture ensures
    that each test runs with its own isolated database transaction, which is rolled back after the
    test completes. This prevents database changes made during one test from affecting other tests.

    :param app: A Flask application instance where the database session is attached.
    :return: A database session (`db.session`) that is rolled back after test execution.
    """
    with app.app_context():
        db.session.begin_nested() # begin a nested transaction
        yield db.session # this is where tests get to interact with the database
        db.session.rollback() # roll back the transaction to undo db changes for the next test

