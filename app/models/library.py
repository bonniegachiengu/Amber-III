from uuid import uuid4
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from enum import Enum

from sqlalchemy import String, Boolean, ForeignKey, JSON, Date, Integer, Float, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, relationships
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from .mixins import (
    EntityMixin, HiveMixin, CliqueMixin, ModeratorMixin, CreatorMixin, OwnerMixin, AuthorMixin, ContributionMixin,
    ContributorMixin, ModelMixin, WatchListMixin, PartnerMixin, AwardMixin, AwardTypeMixin
)


if TYPE_CHECKING:
    from .scrolls import Scroll
    from .user import User
    from .journal import Magazine, Article
    from .player import Bookmark, WatchHistory
    from .community import Reaction, Fandom
    from .calendar import Calendar
    from .commerce import Fund, Transaction, Exchange
    from .common import Genre, Language, Nationality, Country, Keyword, Theme, Tag, Period, WikiTemplate, DashboardTemplate


def generate_uuid():
    return str(uuid4())


class Library(db.Model, ModelMixin, ContributionMixin, EntityMixin):
    pass


class Collection(db.Model, ModelMixin, ContributionMixin):
    pass


class Portfolio(db.Model, ModelMixin, ContributionMixin):
    pass


class FilmType(Enum):

    MOVIE = "Movie"
    TV_EPISODE = "TV Episode"
    YOUTUBE_VIDEO = "YouTube Video"
    SHORT = "Short"


class Film(db.Model, ModelMixin, ContributionMixin, EntityMixin):

    __tablename__ = 'films'
    # Core Fields
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    title: Mapped[str] = mapped_column(String, nullable=False)
    original_title: Mapped[Optional[str]] = mapped_column(String)
    release_date: Mapped[Optional[datetime]] = mapped_column(Date)
    runtime: Mapped[Optional[int]] = mapped_column(Integer)
    synopsis: Mapped[Optional[str]] = mapped_column(Text)
    poster_url: Mapped[Optional[str]] = mapped_column(String)
    backdrop_url: Mapped[Optional[str]] = mapped_column(String)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    available_locally: Mapped[bool] = mapped_column(Boolean, default=False)
    streaming_links: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    trailer_url: Mapped[Optional[str]] = mapped_column(String)
    watch_count: Mapped[int] = mapped_column(Integer, default=0)
    average_progress: Mapped[float] = mapped_column(Float, default=0.0)
    popularity_score: Mapped[float] = mapped_column(Float, default=0.0)
    scroll_stats: Mapped[Optional[dict]] = mapped_column(JSON, default={})
    viewer_tags: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    contributed_by_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('users.id'))
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    contributor_amber_points: Mapped[float] = mapped_column(Float, default=0.0)
    submission_status: Mapped[str] = mapped_column(String, default='Draft')
    edit_history: Mapped[Optional[list[UUID]]] = mapped_column(ARRAY(UUID(as_uuid=True)))
    # External data
    imdb_id: Mapped[Optional[str]] = mapped_column(String)
    tmdb_id: Mapped[Optional[int]] = mapped_column(Integer)
    imdb_rating: Mapped[Optional[float]] = mapped_column(Float)
    imdb_votes: Mapped[Optional[int]] = mapped_column(Integer)
    tmdb_rating: Mapped[Optional[float]] = mapped_column(Float)
    tmdb_votes: Mapped[Optional[int]] = mapped_column(Integer)
    rotten_tomatoes_rating: Mapped[Optional[float]] = mapped_column(Float)
    metascore: Mapped[Optional[int]] = mapped_column(Integer)
    awards: Mapped[Optional[str]] = mapped_column(String)
    content_rating: Mapped[Optional[str]] = mapped_column(String)
    budget: Mapped[Optional[int]] = mapped_column(Integer)
    revenue: Mapped[Optional[int]] = mapped_column(Integer)
    tagline: Mapped[Optional[str]] = mapped_column(String)
    box_office: Mapped[Optional[str]] = mapped_column(String)
    production_companies: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    spoken_languages: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    country_of_origin: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    imdb_data: Mapped[Optional[dict]] = mapped_column(JSON)
    tmdb_data: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # Relationships # TODO: Review the Backrefs after creating models
    contributors: Mapped[List["User"]] = relationship('User', backref='contributions')
    tags: Mapped[List["Tag"]] = relationship('Tag', backref='films')
    genres: Mapped[List["Genre"]] = relationship('Genre', backref='films')
    themes: Mapped[List["Theme"]] = relationship('Theme', backref='films')
    keywords: Mapped[List["Keyword"]] = relationship('Keyword', backref='films')
    studios: Mapped[List["Studio"]] = relationship('Studio', backref='films')
    languages: Mapped[List["Language"]] = relationship('Language', backref='films')
    countries: Mapped[List["Country"]] = relationship('Country', backref='films')
    periods: Mapped[List["Period"]] = relationship('Period', backref='films')
    careers: Mapped[List["Career"]] = relationship("Career", back_populates="film", cascade="all, delete-orphan")
    albums: Mapped[List["Album"]] = relationship('Album', backref='films')
    calendar: Mapped[Optional["Calendar"]] = relationship('Calendar', back_populates='film', uselist=False)
    wiki: Mapped[Optional["WikiTemplate"]] = relationship('Wiki', back_populates='film', uselist=False)
    dashboard: Mapped[Optional["DashboardTemplate"]] = relationship('Dashboard', back_populates='film', uselist=False)

    def __repr__(self):
        return f"<Film {self.title} ({self.release_date})>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "original_title": self.original_title,
            "release_date": self.release_date.isoformat() if self.release_date else None,
            "runtime": self.runtime,
            "synopsis": self.synopsis,
            "poster_url": self.poster_url,
            "backdrop_url": self.backdrop_url,
            "is_verified": self.is_verified,
            "available_locally": self.available_locally,
            "streaming_links": self.streaming_links,
            "trailer_url": self.trailer_url,
            "watch_count": self.watch_count,
            "average_progress": self.average_progress,
            "popularity_score": self.popularity_score,
            "scroll_stats": self.scroll_stats,
            "viewer_tags": self.viewer_tags,
            "contributed_by_id": str(self.contributed_by_id) if self.contributed_by_id else None,
            "contributor_score": self.contributor_score,
            "submission_status": self.submission_status,
            "edit_history": [str(eid) for eid in self.edit_history] if self.edit_history else [],
            "imdb_id": self.imdb_id,
            "tmdb_id": self.tmdb_id,
            "imdb_rating": self.imdb_rating,
            "imdb_votes": self.imdb_votes,
            "tmdb_rating": self.tmdb_rating,
            "tmdb_votes": self.tmdb_votes,
            "metascore": self.metascore,
            "awards": self.awards,
            "content_rating": self.content_rating,
            "budget": self.budget,
            "revenue": self.revenue,
            "tagline": self.tagline,
            "box_office": self.box_office,
            "production_companies": self.production_companies,
            "spoken_languages": self.spoken_languages,
            "country_of_origin": self.country_of_origin,
            "imdb_data": self.imdb_data,
            "tmdb_data": self.tmdb_data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Album(db.Model, ModelMixin, ContributionMixin, WatchListMixin, EntityMixin):
    __tablename__ = 'albums'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # Other fields ...

    # Relationships
    films: Mapped[List["Film"]] = relationship('Film', backref='albums')

    def __repr__(self):
        return f"<Album {self.title}>"


class Hitlist(db.Model, ModelMixin, ContributionMixin, WatchListMixin, EntityMixin):
    pass


class Person(db.Model, ModelMixin, ContributionMixin, EntityMixin):

    __tablename__ = 'people'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String)
    date_of_birth: Mapped[Optional[datetime]] = mapped_column(Date)
    date_of_death: Mapped[Optional[datetime]] = mapped_column(Date, default=None)
    avatar_url: Mapped[Optional[str]] = mapped_column(String)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    nationality: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_linked: Mapped[bool] = mapped_column(Boolean, default=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    profession_summary: Mapped[Optional[str]] = mapped_column(String)
    # TODO: Review the Backrefs after creating models
    contributors: Mapped[List["User"]] = relationship('User', backref='contributions')
    careers: Mapped[List["Career"]] = relationship('Career', back_populates='person')
    relationships: Mapped[List["Relationship"]] = relationship('Relationship', back_populates='person')
    characters: Mapped[List["Character"]] = relationship('Character', back_populates='person')
    fandoms: Mapped[List["Fandom"]] = relationship('Fandom', back_populates='members')
    calendar: Mapped[Optional["Calendar"]] = relationship('Calendar', back_populates='person', uselist=False)
    wiki: Mapped[Optional["WikiTemplate"]] = relationship('Wiki', back_populates='person', uselist=False)
    dashboard: Mapped[Optional["DashboardTemplate"]] = relationship('Dashboard', back_populates='person', uselist=False)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Person {self.full_name or f'{self.first_name} {self.last_name}'} {self.profession_summary}>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "date_of_death": self.date_of_death.isoformat() if self.date_of_death else None,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "nationality": self.nationality,
            "is_verified": self.is_verified,
            "is_linked": self.is_linked,
            "confidence_score": self.confidence_score,
            "profession_summary": self.profession_summary,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Career(db.Model, ModelMixin, ContributionMixin, EntityMixin):
    __tablename__ = "careers"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    person_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=False)
    # Relationships
    person: Mapped["Person"] = relationship("Person", back_populates="careers")
    characters: Mapped[List["Character"]] = relationship("Character", back_populates="career", cascade="all, delete-orphan")
    gigs: Mapped[List["Gig"]] = relationship("Gig", back_populates="career", cascade="all, delete-orphan")
    wiki: Mapped[Optional["WikiTemplate"]] = relationship('Wiki', back_populates='career', uselist=False)


    def __repr__(self):
        return f"<Career {self.id} for Person {self.person_id}>"

    def to_dict(self):
        return {
        }


class Gig(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a professional engagement or job (Gig) associated with a film and a career.

    This class provides a database representation of a job or role undertaken for a specific
    film by a person represented by a career. The Gig has attributes describing details such
    as the title of the job, the dates it started and ended, and additional context like
    notes or episode count (if relevant). It also establishes relationships with the
    Film and Career models.

    :ivar id: Unique identifier for the gig.
    :type id: UUID
    :ivar film_id: Identifier of the film related to this gig.
    :type film_id: UUID
    :ivar career_id: Identifier of the career related to this gig.
    :type career_id: UUID
    :ivar job_title: The role or job title associated with the gig.
    :type job_title: str
    :ivar start_date: The date the gig started. May be None if not specified.
    :type start_date: date or None
    :ivar end_date: The date the gig ended. May be None if not specified.
    :type end_date: date or None
    :ivar episodes: Number of episodes associated with the gig, relevant for episodic productions. May be None.
    :type episodes: int or None
    :ivar notes: Additional notes or comments about the gig. May be None.
    :type notes: str or None
    :ivar is_primary_credit: Boolean indicating whether this gig is a primary credit.
    :type is_primary_credit: bool
    """
    __tablename__ = "gigs"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    film_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("films.id"), nullable=False)
    career_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("careers.id"), nullable=False)
    job_title: Mapped[str] = mapped_column(db.String(128), nullable=False)
    start_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    episodes: Mapped[int | None] = mapped_column(db.Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(db.Text, nullable=True)
    is_primary_credit: Mapped[bool] = mapped_column(db.Boolean, default=False)
    # TODO: Review these relationships
    career = relationship("Career", back_populates="gigs")
    film = relationship("Film", back_populates="gigs")

    def __repr__(self):
        return f"<Gig {self.job_title} in Film {self.film_id} by Career {self.career_id}>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "film_id": str(self.film_id),
            "career_id": str(self.career_id),
            "job_title": self.job_title,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "episodes": self.episodes,
            "notes": self.notes,
            "is_primary_credit": self.is_primary_credit
        }


class Character(db.Model, ModelMixin, ContributionMixin, EntityMixin):
    """
    Represents a character in a film, their associated attributes, and relations.

    The Character class models key information about characters in films, including
    their name, aliases, and associations with careers and films. This class also
    handles optional data such as descriptions, episodes featuring the character,
    and relevant dates of activity. Relationships to Career and Film models allow
    for mapping between entities.

    :ivar id: The unique identifier of the character.
    :type id: UUID
    :ivar name: The name of the character.
    :type name: str
    :ivar aliases: A list of alternate names or aliases for the character.
    :type aliases: list[str]
    :ivar description: An optional textual description of the character.
    :type description: str | None
    :ivar film_id: The foreign key referencing the film the character belongs to.
    :type film_id: UUID
    :ivar career_id: The foreign key referencing the character's associated career.
    :type career_id: UUID
    :ivar start_date: Optional start date of the character's relevant activity or role.
    :type start_date: datetime | None
    :ivar end_date: Optional end date of the character's relevant activity or role.
    :type end_date: datetime | None
    :ivar episodes: Optional count of episodes featuring the character.
    :type episodes: int | None
    :ivar notes: Optional additional notes about the character.
    :type notes: str | None
    :ivar career: The related Career entity.
    :ivar film: The related Film entity.
    """
    __tablename__ = "characters"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(db.String(128), nullable=False)
    aliases: Mapped[list[str]] = mapped_column(ARRAY(db.String), default=list)
    description: Mapped[str | None] = mapped_column(db.Text, nullable=True)
    film_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("films.id"), nullable=False)
    career_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("careers.id"), nullable=False)
    start_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    episodes: Mapped[int | None] = mapped_column(db.Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(db.Text, nullable=True)
    # TODO: Review these relationships
    career = relationship("Career", back_populates="characters")
    film = relationship("Film", back_populates="characters")

    def __repr__(self):
        return f"<Character {self.name} in Film {self.film_id} by Career {self.career_id}>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "aliases": self.aliases,
            "description": self.description,
            "film_id": str(self.film_id),
            "career_id": str(self.career_id),
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "episodes": self.episodes,
            "notes": self.notes
        }


class Studio(db.Model, ModelMixin, ContributionMixin, EntityMixin):
    pass


class RelationshipType(Enum):
    """
    Enumeration for representing various types of relationships.

    This class provides a standardized set of values to classify different
    types of relationships within a domain model or relational data
    structures. It enables clear and consistent representation across
    applications that operate on relationship identification or analysis.
    """
    SIBLING = "Sibling"
    PARENT = "Parent"
    CHILD = "Child"
    STEP_PARENT = "Step-Parent"
    STEP_SIBLING = "Step-Sibling"
    COUSIN = "Cousin"
    SPOUSE = "Spouse"
    EX_SPOUSE = "Ex-Spouse"
    UNCLE = "Uncle"
    AUNT = "Aunt"
    NEPHEW = "Nephew"
    NIECE = "Niece"
    GRANDPARENT = "Grandparent"
    GRANDCHILD = "Grandchild"
    GREAT_GRANDPARENT = "Great-Grandparent"
    GREAT_GRANDCHILD = "Great-Grandchild"
    PARTNER = "Partner"


class Relationship(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a relationship between two people, including details about the nature
    of the relationship and its duration.

    This class is used to model relationships in a database, specifying the individuals
    involved, the type of relationship, and optional start and end dates. The relationships
    are established between two Person entities and are associated with `RelationshipType`.

    :ivar id: The unique identifier for the relationship.
    :type id: UUID
    :ivar person_id: The unique identifier of the first person in the relationship.
    :type person_id: UUID
    :ivar related_person_id: The unique identifier of the second person in the relationship.
    :type related_person_id: UUID
    :ivar relationship_type: The type of relationship between the two persons.
    :type relationship_type: RelationshipType
    :ivar start_date: Optional date indicating when the relationship began.
    :type start_date: datetime | None
    :ivar end_date: Optional date indicating when the relationship ended.
    :type end_date: datetime | None
    """
    __tablename__ = "relationships"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    person_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=False)
    related_person_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=False)
    relationship_type: Mapped[RelationshipType] = mapped_column(db.Enum(RelationshipType), nullable=False)
    start_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    # TODO: Review these relationships
    person = relationship("Person", foreign_keys=[person_id], back_populates="relationships")
    related_person = relationship("Person", foreign_keys=[related_person_id], back_populates="relationships")

    def __repr__(self):
        return f"<Relationship {self.relationship_type.value} between {self.person_id} and {self.related_person_id}>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "person_id": str(self.person_id),
            "related_person_id": str(self.related_person_id),
            "relationship_type": self.relationship_type.value,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None
        }


class Shop(db.Model, ModelMixin, ContributionMixin, EntityMixin, HiveMixin):
    pass


class Assets(db.Model, ModelMixin, ContributionMixin, EntityMixin):
    pass


class Merchandise(db.Model, ModelMixin, ContributionMixin):
    pass


class Wallet(db.Model, ModelMixin, ContributionMixin, EntityMixin):
    pass


class Stock(db.Model, ModelMixin, ContributionMixin):
    pass


class Accolade(db.Model, ModelMixin, ContributionMixin):
    pass


class Condition(db.Model, ModelMixin, ContributionMixin):
    pass


class Win(db.Model, ModelMixin, ContributionMixin):
    pass


class Timeline(db.Model, ModelMixin, ContributionMixin):
    pass


class Filmography(db.Model, ModelMixin, ContributionMixin):
    pass


class StreamingPlatform(db.Model, ModelMixin, ContributionMixin, EntityMixin, PartnerMixin):
    pass


class PeersPlatform(db.Model, ModelMixin, ContributionMixin, EntityMixin, PartnerMixin):
    pass


class SocialPlatform(db.Model, ModelMixin, ContributionMixin, EntityMixin, PartnerMixin):
    pass


class Website(db.Model, ModelMixin, ContributionMixin, EntityMixin, PartnerMixin):
    pass


class AwardType(db.Model, ModelMixin, ContributionMixin, EntityMixin, AwardTypeMixin):
    pass


class Award(db.Model, ModelMixin, ContributionMixin, EntityMixin, AwardMixin):
    pass


class Nomination(db.Model, ModelMixin, ContributionMixin, EntityMixin, AwardMixin):
    pass


class BoxOffice(db.Model, ModelMixin, ContributionMixin):
    pass


class TheBoxOffice(db.Model, ModelMixin, ContributionMixin, EntityMixin, PartnerMixin):
    pass


class Distributor(db.Model, ModelMixin, ContributionMixin, EntityMixin, PartnerMixin):
    pass


class Inspiration(db.Model, ModelMixin, ContributionMixin):
    pass


class InspirationSource(db.Model, ModelMixin, ContributionMixin, EntityMixin):
    pass


class Theatre(db.Model, ModelMixin, ContributionMixin, EntityMixin, PartnerMixin):
    pass


class Release(db.Model, ModelMixin, ContributionMixin):
    pass


class Ticket(db.Model, ModelMixin, ContributionMixin):
    pass
