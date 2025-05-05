import pytest
from datetime import date
from uuid import uuid4
from app.models.library import Film, Genre, Person
from app.models.user import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def sample_user(session) -> User:
    """
    Fixture that creates and returns a sample user in the database.

    This function creates a user with preset values for `username`,
    `email`, and `password_hash`. The user is then added to the provided
    session and committed to the database to be available for further
    tests. Once created, the user object is returned for use in the test.

    :param session: The database session to add the sample user to.
    :type session: Session
    :return: The sample user object added to the session.
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
def sample_genres(session) -> list[Genre]:
    """
    Creates and commits sample genres into the database session for testing. The
    genres include "Drama" and "Sci-Fi". This fixture is used to provide preloaded
    genres for tests that require them.

    :param session: Database session for adding and committing the sample genres
    :return: List of created Genre objects
    :rtype: list[Genre]
    """
    genres = [Genre(name="Drama"), Genre(name="Sci-Fi")]
    session.add_all(genres)
    session.commit()
    return genres


@pytest.fixture
def sample_persons(session) -> dict[str, Person]:
    """
    Fixture to create and add sample `Person` instances to the provided session. The
    persons created include a director, writer, actor, and producer, each initialized
    with appropriate names and roles. These instances are added to the session and
    committed to facilitate use in testing scenarios.

    :param session: The SQLAlchemy database session object used for persisting and
                    committing sample `Person` objects.
    :return: A dictionary mapping roles (e.g., 'director', 'writer', etc.) to their
             corresponding `Person` instances.
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


def test_film_model_full_integration(sample_user: User, sample_genres, sample_persons: list[Genre], session) -> None:
    """
    Tests the comprehensive integration of the Film model including its attributes, relationships, and interactions with
    the database. The test verifies that a film instance can be accurately created, persisted, and queried, ensuring all
    fields and relationships are correctly integrated. Additionally, the test validates the consistency and correctness
    of data upon re-fetching the model and its dictionary output representation.

    :param sample_user: A user instance representing the person who contributed the film.
    :type sample_user: User
    :param sample_genres: Genre instances associated with the film.
    :type sample_genres: list[Genre]
    :param sample_persons: A dictionary containing persons (e.g., director, writer, actor, producer) related to the film.
    :type sample_persons: dict
    :param session: A database session object to manage transactions during the test.
    :type session: Session
    :return: None
    """
    film = Film(
        title="Inception 2",
        original_title="Inception II",
        release_date=date(2025, 7, 16),
        runtime=152,
        synopsis="A mind-bending sequel.",
        poster_url="https://image.tmorg/t/p/poster.jpg",
        backdrop_url="https://image.tmorg/t/p/backdrop.jpg",
        is_verified=True,
        available_locally=True,
        streaming_links=["https://netflix.com/inception2"],
        trailer_url="https://youtube.com/trailer",
        watch_count=1000,
        average_progress=85.2,
        popularity_score=9.5,
        scroll_stats={"Drama": 88, "Sci-Fi": 92},
        viewer_tags=["trippy", "thriller"],
        contributed_by=sample_user,
        contributor_score=4.8,
        submission_status="Published",
        edit_history=[uuid4()],
        imdb_id="tt9999999",
        tmdb_id=987654,
        imdb_rating=8.9,
        imdb_votes=230000,
        tmdb_rating=9.0,
        tmdb_votes=210000,
        metascore=82,
        awards="Nominated for 3 Oscars",
        content_rating="PG-13",
        budget=200000000,
        revenue=850000000,
        tagline="Dream deeper.",
        box_office="$850,000,000",
        production_companies=["Syncopy", "Warner Bros."],
        spoken_languages=["English", "Japanese"],
        country_of_origin=["USA", "UK"],
        imdb_data={"genre": ["Sci-Fi", "Thriller"]},
        tmdb_data={"genre_ids": [878, 53]}
    )
    film.genres = sample_genres
    film.directors = [sample_persons["director"]]
    film.writers = [sample_persons["writer"]]
    film.cast = [sample_persons["actor"]]
    film.producers = [sample_persons["producer"]]

    session.add(film)
    session.commit()

    # Reload and assert
    fetched = Film.query.filter_by(title="Inception 2").first()
    assert fetched is not None
    assert fetched.runtime == 152
    assert fetched.imdb_rating == 8.9
    assert fetched.contributed_by.username == "test_user"
    assert "Dream deeper." in fetched.tagline
    assert len(fetched.genres) == 2
    assert len(fetched.cast) == 1
    assert fetched.cast[0].name == "Emily Blunt"
    assert "Warner Bros." in fetched.production_companies

    # Check dictionary output
    film_dict = fetched.to_dict()
    assert film_dict["title"] == "Inception 2"
    assert film_dict["poster_url"].startswith("https")
    assert "Sci-Fi" in film_dict["viewer_tags"]
    assert film_dict["imdb_data"]["genre"][0] == "Sci-Fi"
