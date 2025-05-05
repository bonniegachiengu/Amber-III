import pytest
from datetime import date
from app.models.library import Person
from app.models.user import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def sample_user(session) -> User:
    """
    This pytest fixture creates a sample user and persists it in the database session.
    The user's password is hashed using a password hashing function, and the user object
    is added to the session and committed. The fixture then returns the created user instance.

    :param session: Database session used to add and commit the user object.
    :type session: Session
    :return: The user object that was created and added to the session.
    :rtype: User
    """
    password_hash = generate_password_hash("password123")
    user = User(
        username="test_user",
        email="test@example.com",
        password_hash=password_hash
    )
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def sample_persons(session) -> dict[str, Person]:
    """
    Creates and commits a set of `Person` objects with different roles to the database
    session and returns them as a dictionary.

    The function adds multiple `Person` instances to the database session. The persons
    represent roles, including director, writer, actor, and producer. After committing
    the session, a dictionary that maps roles to the respective `Person` objects is returned.

    :param session: The database session where the `Person` objects will be added and committed.
    :type session: sqlalchemy.orm.Session
    :return: A dictionary where the keys are role names (strings) and the values are
             corresponding `Person` objects.
    :rtype: dict[str, Person]
    """
    director = Person(name="Jane Doe", role="Director")
    writer = Person(name="John Smith", role="Writer")
    actor = Person(name="Emily Blunt", role="Actor")
    producer = Person(name="Lisa Ray", role="Producer")
    session.add_all([director, writer, actor, producer])
    session.commit()
    return {
        "director": director,
        "writer": writer,
        "actor": actor,
        "producer": producer
    }


def test_person_model_full_lifecycle(session, sample_user):
    """
    Tests the full lifecycle operations of the Person model within the database. The test includes
    validating data creation, retrieval, and deletion in the database, along with testing the
    ```__repr__``` and ```to_dict``` methods of the Person model.

    The test ensures the following:
    - A Person instance is created with valid input data and saved successfully to the database.
    - The Person instance can be retrieved from the database with all fields matching the input data.
    - The ```__repr__``` method provides a meaningful string representation.
    - The ```to_dict``` method converts the model instance to a dictionary accurately and includes all
      relevant fields with correct types.
    - The Person instance is deleted from the database without errors.

    :param session: An SQLAlchemy database session is used for interacting with the database.
                    It provides transaction control and query execution.
    :param sample_user: A sample User instance to associate with the contributor_id field of the
                        Person instance.
    :return: None
    """
    person = Person(
        first_name="Jane",
        last_name="Doe",
        full_name="Jane Doe",
        date_of_birth=date(1985, 6, 15),
        avatar_url="http://example.com/avatar.jpg",
        bio="A versatile actress and producer.",
        nationality=["American", "British"],
        is_verified=True,
        is_linked=True,
        confidence_score=0.92,
        contributor_id=sample_user.id,
        profession_summary="Actor, Producer"
    )

    session.add(person)
    session.commit()

    # Fetch from DB
    retrieved = Person.query.get(person.id)
    assert retrieved is not None
    assert retrieved.first_name == "Jane"
    assert retrieved.last_name == "Doe"
    assert retrieved.full_name == "Jane Doe"
    assert retrieved.date_of_birth == date(1985, 6, 15)
    assert retrieved.avatar_url == "http://example.com/avatar.jpg"
    assert retrieved.bio == "A versatile actress and producer."
    assert "American" in retrieved.nationality
    assert retrieved.is_verified is True
    assert retrieved.is_linked is True
    assert abs(retrieved.confidence_score - 0.92) < 0.01
    assert retrieved.contributor_id == sample_user.id
    assert retrieved.profession_summary == "Actor, Producer"

    # Test __repr__
    assert "Jane Doe" in repr(retrieved)

    # Test to_dict
    person_dict = retrieved.to_dict()
    assert isinstance(person_dict["id"], str)
    assert person_dict["first_name"] == "Jane"
    assert person_dict["last_name"] == "Doe"
    assert person_dict["full_name"] == "Jane Doe"
    assert person_dict["date_of_birth"] == "1985-06-15"
    assert person_dict["avatar_url"] == "http://example.com/avatar.jpg"
    assert person_dict["bio"] == "A versatile actress and producer."
    assert "American" in person_dict["nationality"]
    assert person_dict["is_verified"] is True
    assert person_dict["is_linked"] is True
    assert abs(person_dict["confidence_score"] - 0.92) < 0.01
    assert person_dict["contributor_id"] == str(sample_user.id)

    session.delete(retrieved)
    session.commit()
