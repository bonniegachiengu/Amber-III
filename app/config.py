import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Configuration class for the application.

    This class contains various configuration settings required for the application to function
    properly, including database configurations, pool options, and security settings. It is designed
    to provide centralized management of these configurations.

    :ivar SQLALCHEMY_DATABASE_URI: URI for connecting to the SQLAlchemy database.
    :type SQLALCHEMY_DATABASE_URI: str
    :ivar SQLALCHEMY_TRACK_MODIFICATIONS: Flag to enable or disable tracking modifications in SQLAlchemy.
    :type SQLALCHEMY_TRACK_MODIFICATIONS: bool
    :ivar SQLALCHEMY_ECHO: Flag to enable or disable logging of SQLAlchemy SQL statements.
    :type SQLALCHEMY_ECHO: bool
    :ivar SQLALCHEMY_ENGINE_OPTIONS: Options for configuring the SQLAlchemy engine, such as pool behavior.
    :type SQLALCHEMY_ENGINE_OPTIONS: dict
    :ivar SQLALCHEMY_POOL_TIMEOUT: Timeout value for database connection pooling in seconds.
    :type SQLALCHEMY_POOL_TIMEOUT: int
    :ivar SECRET_KEY: Secret key used for security-related operations like session signing.
    :type SECRET_KEY: str
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "pool_size": 10,
        "max_overflow": 20,
    }
    SQLALCHEMY_POOL_TIMEOUT = 20
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # Add any other general configurations here


class TestingConfig(Config):
    """
    Configuration class for testing environments.

    This class defines the configuration settings tailored for testing purposes.
    It includes settings such as enabling testing mode, using an in-memory
    database, and disabling database modification tracking. The class can also
    include other testing-specific configurations as required, for aspects like
    security, caching, or logging.

    :ivar SQLALCHEMY_DATABASE_URI: URI for the temporary in-memory SQLite database
        used during testing.
    :type SQLALCHEMY_DATABASE_URI: str
    :ivar TESTING: Boolean flag indicating if the application is running in testing
        mode.
    :type TESTING: bool
    :ivar SQLALCHEMY_TRACK_MODIFICATIONS: Boolean flag indicating whether to track
        modifications to objects in SQLAlchemy.
    :type SQLALCHEMY_TRACK_MODIFICATIONS: bool
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")  # Use test database URI
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "pool_size": 10,
        "max_overflow": 20,
    }
    SQLALCHEMY_POOL_TIMEOUT = 20
