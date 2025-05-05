import pytest
from datetime import date
from app.models.library import Film, Career, Gig, Character, Person, Relationship, RelationshipType


@pytest.fixture
def sample_film(session) -> Film:
    """
    Fixture function that creates and persists a sample `Film` instance in the
    database for testing purposes. The function initializes a `Film` object
    with pre-defined attributes, adds it to the database session, commits
    the transaction, and returns the created `Film` instance.

    :param session: Database session object used to persist the `Film` instance.
    :type session: Session
    :return: A `Film` object that has been added to the database.
    :rtype: Film
    """
    film = Film(title="Test Film", release_year=2024)
    session.add(film)
    session.commit()
    return film


@pytest.fixture
def sample_career(session, sample_persons) -> Career:
    """
    Fixture that provides a sample `Career` instance for testing purposes. This
    fixture uses a provided session and a sample person instance to create
    and return a `Career` object. The `Career` instance is added to the
    database session and committed before being returned.

    :param session: A database session fixture used to interact with the
        database.
    :param sample_persons: A dictionary mapping roles to sample `Person` instances.
        Example: `{"actor": Person, "director": Person}`.
    :return: A `Career` instance associated with the sample person.
    :rtype: Career
    """
    person = sample_persons["actor"]
    career = Career(person_id=person.id)
    session.add(career)
    session.commit()
    return career


def test_career_model(session, sample_persons) -> None:
    """
    Tests the Career model's creation, retrieval, and deletion process in the database. This
    function ensures that a Career object can be correctly added to the session, committed,
    retrieved, converted into a dictionary, and deleted from the database. The test validates
    the integrity of the object fields and the output of its string representation.

    :param session: Database session fixture used to simulate the transactional interaction
                    with the database during the test.
    :param sample_persons: Fixture that provides sample persons data. It includes a dictionary
                           mapping descriptive identifiers to person objects for testing purposes.
    :return: None
    """
    person = sample_persons["writer"]
    career = Career(person_id=person.id)

    session.add(career)
    session.commit()

    retrieved = Career.query.get(career.id)
    assert retrieved is not None
    assert retrieved.person_id == person.id
    assert "Career" in repr(retrieved)

    career_dict = retrieved.to_dict()
    assert career_dict["person_id"] == str(person.id)

    session.delete(retrieved)
    session.commit()


def test_gig_model(session, sample_film, sample_career) -> None:
    """
    Tests the creation, retrieval, validation, and deletion of a `Gig` model instance within a database session.
    Ensures that the `Gig` model behaves as expected by verifying its attributes and functionality, such as converting
    to dictionary representation and proper string representation.

    :param session: The SQLAlchemy database session used to perform operations with the `Gig` model.
    :type session: sqlalchemy.orm.scoping.scoped_session
    :param sample_film: A sample `Film` instance that is associated with the gig.
    :type sample_film: Film
    :param sample_career: A sample `Career` instance that is associated with the gig.
    :type sample_career: Career
    :return: None
    """
    gig = Gig(
        film_id=sample_film.id,
        career_id=sample_career.id,
        job_title="Director",
        start_date=date(2023, 1, 1),
        end_date=date(2023, 12, 31),
        episodes=1,
        notes="Main director",
        is_primary_credit=True
    )
    session.add(gig)
    session.commit()

    retrieved = Gig.query.get(gig.id)
    assert retrieved is not None
    assert retrieved.job_title == "Director"
    assert retrieved.film_id == sample_film.id
    assert retrieved.career_id == sample_career.id
    assert retrieved.episodes == 1
    assert retrieved.is_primary_credit is True

    assert "Gig" in repr(retrieved)
    gig_dict = retrieved.to_dict()
    assert gig_dict["job_title"] == "Director"

    session.delete(retrieved)
    session.commit()


def test_character_model(session, sample_film, sample_career) -> None:
    """
    Tests the Character model by creating a new character instance, adding it to the
    session, retrieving it, validating its attributes, converting it to a dictionary,
    and finally removing it from the database.

    This test ensures CRUD operations are functioning properly for the Character
    model, and that the object representation and dictionary conversion maintain
    data integrity.

    :param session: SQLAlchemy session object used for database operations.
    :param sample_film: Sample film instance related to the character being tested.
    :param sample_career: Sample career instance related to the character being tested.
    :return: None
    """
    character = Character(
        name="John Hero",
        description="Protagonist of the story.",
        film_id=sample_film.id,
        career_id=sample_career.id,
        start_date=date(2023, 3, 1),
        end_date=date(2023, 9, 1),
        episodes=10,
        notes="Iconic role."
    )
    session.add(character)
    session.commit()

    retrieved = Character.query.get(character.id)
    assert retrieved is not None
    assert retrieved.name == "John Hero"
    assert retrieved.film_id == sample_film.id
    assert retrieved.career_id == sample_career.id
    assert retrieved.episodes == 10

    assert "Character" in repr(retrieved)
    char_dict = retrieved.to_dict()
    assert char_dict["name"] == "John Hero"
    assert char_dict["description"] == "Protagonist of the story."

    session.delete(retrieved)
    session.commit()


@pytest.fixture
def relationship_persons(session) -> dict[str, Person]:
    """
    Fixture to create and persist two related `Person` objects in the database session.
    This setup is used to establish a relationship between two `Person` entities
    for testing purposes.

    The fixture adds `person_a` and `person_b` to the session, commits
    the session, and then returns a dictionary containing references
    to the created `Person` objects.

    :param session: Database session used to add and commit `Person` objects.
    :type session: Session
    :return: A dictionary with keys "person" and "related" mapping
             to the created `Person` objects.
    :rtype: dict[str, Person]
    """
    person_a = Person(full_name="Alice Johnson")
    person_b = Person(full_name="Bob Johnson")
    session.add_all([person_a, person_b])
    session.commit()
    return {
        "person": person_a,
        "related": person_b
    }


def test_relationship_model_full_lifecycle(session, relationship_persons):
    """
    Tests the full lifecycle of a relationship model within a database session, ensuring
    correct instantiation, persistence, retrieval, dictionary serialization, and deletion
    of relationship records.

    This function performs the following steps:
    1. Instantiates a `Relationship` object, linking two persons through a specific
       relationship type with provided start and end dates.
    2. Commits the new relationship instance to the database.
    3. Retrieves the relationship object by its ID and validates its properties.
    4. Tests the `__repr__` representation of the retrieved object.
    5. Serializes the object to a dictionary and ensures the correct structure
       and values are returned.
    6. Deletes the relationship instance and ensures it no longer exists in the database.

    :param session: Database session object used to interact with the persistence layer.
    :type session: Session
    :param relationship_persons: Dictionary containing two persons: "person" and "related",
        which represent the two entities involved in the relationship. "person" is the primary
        person, while "related" is the related person.
    :type relationship_persons: dict
    :return: None
    :rtype: None
    """
    alice = relationship_persons["person"]
    bob = relationship_persons["related"]
    relationship = Relationship(
        person_id=alice.id,
        related_person_id=bob.id,
        relationship_type=RelationshipType.SIBLING,
        start_date=date(2000, 1, 1),
        end_date=None
    )
    session.add(relationship)
    session.commit()
    # Fetch from DB
    retrieved = Relationship.query.get(relationship.id)
    assert retrieved is not None
    assert retrieved.person_id == alice.id
    assert retrieved.related_person_id == bob.id
    assert retrieved.relationship_type == RelationshipType.SIBLING
    assert retrieved.start_date == date(2000, 1, 1)
    assert retrieved.end_date is None
    # Backref: check alice.relationships includes the relationship
    assert relationship in alice.relationships
    # Backref: check bob.related_to_me includes the relationship
    assert relationship in bob.related_to_me
    # __repr__
    assert "Sibling" in repr(retrieved)
    # to_dict
    rel_dict = retrieved.to_dict()
    assert rel_dict["person_id"] == str(alice.id)
    assert rel_dict["related_person_id"] == str(bob.id)
    assert rel_dict["relationship_type"] == "Sibling"
    assert rel_dict["start_date"] == "2000-01-01"
    assert rel_dict["end_date"] is None
    # Delete
    session.delete(retrieved)
    session.commit()

    assert Relationship.query.get(relationship.id) is None
