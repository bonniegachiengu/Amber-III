import pytest
from app.models.user import User, UserFollow
from uuid import uuid4
from werkzeug.security import generate_password_hash


def test_user_creation(session) -> None:
    """
    Tests the creation and persistence of a User instance in the database session.
    This test ensures that the User object is correctly added to the session, committed,
    retrieved, and validated against its initial attributes. It also verifies that the
    retrieved instance contains the expected data, including values set as defaults.

    :param session: The database session is used for persisting and querying the User instance.
    :type session: Session
    :return: None
    :rtype: None
    """
    # Hashing the password for security reasons
    password_hash = generate_password_hash("password123")
    user = User(
        id=uuid4(),
        username="test_user",
        email="testuser@example.com",
        password_hash=password_hash,
        is_active=True,
        is_verified=True,
    )
    session.add(user)
    session.commit()

    fetched = User.query.filter_by(username="test_user").first()
    assert user.id is not None
    assert user.username == "test_user"
    assert user.email == "testuser@example.com"
    assert user.is_active is True  # verify default value
    assert user.is_verified is True
    assert fetched.id == user.id
    assert fetched.to_dict()["username"] == "test_user"


def test_user_email_unique(session) -> None:
    """
    Tests that the email field for User entities must be unique by attempting
    to add two users with the same email to the database. Ensures the system
    throws an exception when committing the second user with a duplicate
    email, verifying the constraint on uniqueness of the email field.

    :param session: The database session used to interact with the database during
        the test.
    :return: None
    """
    user1 = User(
        id=uuid4(),
        username="user1",
        email="unique@example.com",
        password_hash="hashed_password",
        is_active=True,
        is_verified=True,
    )
    user2 = User(
        id=uuid4(),
        username="user2",
        email="unique@example.com",  # Same email
        password_hash="hashed_password",
        is_active=True,
        is_verified=True,
    )
    session.add(user1)
    session.commit()

    with pytest.raises(Exception):  # Assuming sqlalchemy raises an exception on duplicate unique
        session.add(user2)
        session.commit()


def test_user_repr(session) -> None:
    """
    Tests the string representation of a User instance by asserting that the
    `repr` method outputs the expected value. It ensures that the user
    representation is properly formatted as per the `User` class
    implementation.

    :param session: Database session used for persisting the User instance
        during the test.
    :return: None
    """
    user = User(
        id=uuid4(),
        username="test_user",
        email="testuser@example.com",
        password_hash="hashed_password",
        is_active=True,
        is_verified=True,
    )
    session.add(user)
    session.commit()

    # Check the user repr explicitly
    assert repr(user) == "<User test_user>"


def test_user_follow(session) -> None:
    """
    Test the functionality of the user follow feature between two users.

    This function tests the proper creation, storage, and querying of a `UserFollow`
    relationship in the database. It ensures that a user (e.g., Alice) can follow another
    user (e.g., Bob), and that the reciprocal relationships are correctly reflected in
    the database.

    :param session: The database session used to perform operations.
    :type session: Session
    :return: None
    :rtype: None
    """
    u1 = User(id=uuid4(), username="alice", email="alice@example.com", password_hash="x")
    u2 = User(id=uuid4(), username="bob", email="bob@example.com", password_hash="y")
    session.add_all([u1, u2])
    session.commit()

    follow = UserFollow(follower_id=u1.id, followed_id=u2.id)
    session.add(follow)
    session.commit()

    # Assert that Alice is following Bob
    assert u1.following[0].followed.username == "bob"
    # Assert that Bob has Alice as a follower
    assert u2.followers[0].follower.username == "alice"

    # Check the inverse relationship: Alice follows Bob and Bob is followed by Alice
    assert u1.is_following(u2)  # Assumes `is_following()` checks the relationship
    assert u2.is_followed_by(u1)  # Similar check for the inverse
