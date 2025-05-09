from sqlalchemy import Table, Column, ForeignKey

from ..extensions import db

# Association table for films and contributors
film_contributors = Table(
    "film_contributors",
    db.metadata,
    Column("film_id", ForeignKey("films.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for persons and contributors
person_contributors = Table(
    "person_contributors",
    db.metadata,
    Column("person_id", ForeignKey("persons.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)
