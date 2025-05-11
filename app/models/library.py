from uuid import uuid4
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, Boolean, ForeignKey, JSONB, Date, Integer, Float, Text, ARRAY, Numeric, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from associations import film_contributors, person_contributors, album_contributors, hitlist_contributors
from ..extensions import db
from .utils.config import (
    ExtensionTypeEnum, AlbumTypeEnum, FilmTypeEnum, RelationshipTypeEnum, CrewTypeEnum
)
from .mixins import (
    EntityMixin, HiveMixin, LibraryMixin, ScrollItemMixin, FanMixin, MarkMixin, ModelMixin, WatchListMixin,
    PeriodMixin, ContributionMixin, OwnedMixin, CreatedMixin, PartnerLinksMixin, ReleaseMixin
)


if TYPE_CHECKING:
    from .scrolls import Scroll
    from .user import User
    from .journal import Magazine, Article, Report, Column
    from .community import Fan, Member, Subscriber, Reward
    from .calendar import Calendar, Ticket
    from .player import Bookmark, PlaybackSession, Subtitle
    from .commerce import Listing, Order, Market, Discount, CustomToken, Fund
    from .common import Verification, Preferences, Notification, Link


def generate_uuid():
    """
    Generates a randomly unique identifier (UUID).

    This function generates a new universally unique identifier (UUID) using
    the `uuid4()` function from Python's uuid library. Each call to the function
    produces a new random UUID, suitable for use in identifying objects
    uniquely in distributed systems or other scenarios requiring unique identification.

    :return: Randomly generated UUID as a string.
    :rtype: str
    """
    return str(uuid4())


class Library(db.Model, ModelMixin, EntityMixin):
    """
    Represents a Library entity within the database.

    This class serves as the model for storing and managing library-related
    data and associated relationships in the database. It encapsulates various
    relationships to other entities such as collections, notifications, preferences,
    and more. The class facilitates handling cascading behaviors and provides
    mechanisms to interact with related models effectively.

    :ivar local_libraries: Represents the relationship to other local libraries
        within this Library entity.
    :type local_libraries: list[Library]
    :ivar owner: Represents the owner of this library.
    :type owner: LibraryMixin
    :ivar wallet: Represents the wallet associated with the library.
    :type wallet: Wallet
    :ivar portfolio: Represents the portfolio associated with the library.
    :type portfolio: Portfolio
    :ivar collections: Represents the collections related to the library.
    :type collections: list[Collection]
    :ivar shops: Represents the shops associated with the library.
    :type shops: list[Shop]
    :ivar markets: Represents the markets associated with the library.
    :type markets: list[Market]
    :ivar watch_history: Represents the watch history associated with
        the library.
    :type watch_history: list[WatchHistory]
    :ivar playback_sessions: Represents the playback sessions linked to
        the library.
    :type playback_sessions: list[PlaybackSession]
    :ivar preferences: Represents the preferences tied to the library.
    :type preferences: list[Preferences]
    :ivar notifications: Represents the notifications received by the
        library.
    :type notifications: list[Notification]
    :ivar sent_notifications: Represents the notifications sent by the
        library.
    :type sent_notifications: list[Notification]
    :ivar fandoms: Represents the fandoms associated with the library.
    :type fandoms: list[Fan]
    :ivar subscriptions: Represents the subscribers associated with the
        library.
    :type subscriptions: list[Subscriber]
    :ivar memberships: Represents the memberships associated with the
        library.
    :type memberships: list[Member]
    """
    __tablename__ = 'libraries'
    local_libraries: Mapped[List["Library"]] = relationship("Library", back_populates="library", cascade="all, delete-orphan")
    owner: Mapped["LibraryMixin"] = relationship("LibraryMixin", back_populates="libraries", uselist=False)
    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="library", uselist=False, cascade="all, delete-orphan")
    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="library", uselist=False, cascade="all, delete-orphan")
    collections: Mapped[List["Collection"]] = relationship("Collection", back_populates="library", cascade="all, delete-orphan")
    shops: Mapped[List["Shop"]] = relationship("Shop", back_populates="library", cascade="all, delete-orphan")
    markets: Mapped[List["Market"]] = relationship("Market", back_populates="library", cascade="all, delete-orphan")
    watch_history: Mapped[List["WatchHistory"]] = relationship("WatchHistory", back_populates="library", cascade="all, delete-orphan")
    playback_sessions: Mapped[List["PlaybackSession"]] = relationship("PlaybackSession", back_populates="library", cascade="all, delete-orphan")
    preferences: Mapped[List["Preferences"]] = relationship("Preferences", back_populates="library", cascade="all, delete-orphan")
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="recipient", cascade="all, delete-orphan")
    sent_notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="sender", cascade="all, delete-orphan")
    fandoms: Mapped[List["Fan"]] = relationship("Fan", back_populates="library", cascade="all, delete-orphan")
    subscriptions: Mapped[List["Subscriber"]] = relationship("Subscriber", back_populates="library", cascade="all, delete-orphan")
    memberships: Mapped[List["Member"]] = relationship("Member", back_populates="library", cascade="all, delete-orphan")


class Collection(db.Model, ModelMixin):
    """
    Represents a collection of various media items in a library.

    This class is used to manage associations between a library (identified by
    `library_id`) and various media entities such as albums, films, and hitlists.
    It supports both "collected" (explicitly included) and "tracked" (followed for
    updates or monitoring purposes) media items. Relationships between this
    collection and its associated entities are maintained for querying and
    manipulation.

    :ivar library_id: Identifier of the library to which this collection belongs.
    :type library_id: UUID
    :ivar library: The library entity associated with this collection.
    :type library: Library
    :ivar collected_albums: List of albums that have been explicitly collected in
        this collection.
    :type collected_albums: List[Album]
    :ivar tracked_albums: List of albums being tracked in this collection.
    :type tracked_albums: List[Album]
    :ivar collected_films: List of films that have been explicitly collected in
        this collection.
    :type collected_films: List[Film]
    :ivar tracked_films: List of films being tracked in this collection.
    :type tracked_films: List[Film]
    :ivar collected_hitlists: List of hitlists that have been explicitly collected
        in this collection.
    :type collected_hitlists: List[Hitlist]
    :ivar tracked_hitlists: List of hitlists being tracked in this collection.
    :type tracked_hitlists: List[Hitlist]
    """
    __tablename__ = 'collections'
    library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("libraries.id"), nullable=False)
    library: Mapped["Library"] = relationship("library", back_populates="collections")
    collected_albums: Mapped[List["Album"]] = relationship("Album", back_populates="collectors")
    tracked_albums: Mapped[List["Album"]] = relationship("Album", back_populates="trackers")
    collected_films: Mapped[List["Film"]] = relationship("Film", back_populates="collectors")
    tracked_films: Mapped[List["Film"]] = relationship("Film", back_populates="trackers")
    collected_hitlists: Mapped[List["Hitlist"]] = relationship("Hitlist", back_populates="collectors")
    tracked_hitlists: Mapped[List["Hitlist"]] = relationship("Hitlist", back_populates="trackers")


class Portfolio(db.Model, ModelMixin):
    """
    Represents a portfolio entity within the database.

    The Portfolio class serves as a central entity that encapsulates various
    relationships and attributes associated with content creation, ownership,
    and distribution in the domain of media, entertainment, and products. It
    maps to the `portfolios` table in the database and collaborates with many
    other entities to represent the diverse associations and responsibilities
    of a portfolio.

    :ivar library_id: The unique identifier of the associated library.
    :type library_id: UUID
    :ivar library: The library associated with the portfolio.
    :type library: Library
    :ivar created_magazines: A list of magazines created by this portfolio as the founder.
    :type created_magazines: List[Magazine]
    :ivar authored_articles: A list of articles authored by this portfolio.
    :type authored_articles: List[Article]
    :ivar authored_reports: A list of reports authored by this portfolio.
    :type authored_reports: List[Report]
    :ivar maintained_columns: A list of columns maintained by this portfolio.
    :type maintained_columns: List[Column]
    :ivar reviewed_scrolls: A list of scrolls reviewed by this portfolio.
    :type reviewed_scrolls: List[Scroll]
    :ivar distributed_albums: A list of albums distributed by this portfolio.
    :type distributed_albums: List[Album]
    :ivar distributed_films: A list of films distributed by this portfolio.
    :type distributed_films: List[Film]
    :ivar nominations: A list of nominations associated with this portfolio as a nominee.
    :type nominations: List[Nomination]
    :ivar wins: A list of wins associated with this portfolio as a winner.
    :type wins: List[Win]
    :ivar created_people: A list of people entities created by this portfolio.
    :type created_people: List[Person]
    :ivar assets: A list of assets associated with this portfolio.
    :type assets: List[Asset]
    :ivar owned_magazines: A list of magazines owned by this portfolio.
    :type owned_magazines: List[Magazine]
    :ivar owned_albums: A list of albums owned by this portfolio.
    :type owned_albums: List[Album]
    :ivar owned_films: A list of films owned by this portfolio.
    :type owned_films: List[Film]
    :ivar owned_hitlists: A list of hitlists created by this portfolio.
    :type owned_hitlists: List[Hitlist]
    :ivar produced_films: A list of films produced by this portfolio.
    :type produced_films: List[Film]
    :ivar orders: A list of orders associated with this portfolio as a buyer.
    :type orders: List[Order]
    :ivar customtokens: A list of custom tokens created by this portfolio.
    :type customtokens: List[CustomToken]
    :ivar created_tickets: A list of tickets created by this portfolio.
    :type created_tickets: List[Ticket]
    :ivar bought_tickets: A list of tickets bought by this portfolio.
    :type bought_tickets: List[Ticket]
    :ivar verifications: A list of verifications conducted by this portfolio.
    :type verifications: List[Verification]
    """
    __tablename__ = "portfolios"
    library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("libraries.id"), nullable=False)
    library: Mapped["Library"] = relationship("Library", back_populates="portfolio")
    created_magazines: Mapped[List["Magazine"]] = relationship("Magazine", back_populates="founders") # founder
    authored_articles: Mapped[List["Article"]] = relationship("Article", back_populates="authors") # writer
    authored_reports: Mapped[List["Report"]] = relationship("Report", back_populates="authors") # analyst
    maintained_columns: Mapped[List["Column"]] = relationship("Column", back_populates="maintainers")
    reviewed_scrolls: Mapped[List["Scroll"]] = relationship("Scroll", back_populates="reviewer")
    distributed_albums: Mapped[List["Album"]] = relationship("Album", back_populates="distributors")
    distributed_films: Mapped[List["Film"]] = relationship("Film", back_populates="distributors")
    nominations: Mapped[List["Nomination"]] = relationship('Nomination', back_populates='nominees')
    wins: Mapped[list["Win"]] = relationship('Win', back_populates='winners')
    created_people: Mapped[List["Person"]] = relationship("Person", back_populates="creators")
    assets: Mapped[List["Asset"]] = relationship("Asset", back_populates="portfolio")
    owned_magazines: Mapped[List["Magazine"]] = relationship("Magazine", back_populates="owners") # owner
    owned_albums: Mapped[List["Album"]] = relationship("Album", back_populates="studios")
    owned_films: Mapped[List["Film"]] = relationship("Film", back_populates="studios")
    owned_hitlists: Mapped[List["Hitlist"]] = relationship("Hitlist", back_populates="creators")
    produced_films: Mapped[List["Film"]] = relationship("Film", back_populates="production_portfolios")
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="buyer_portfolio")
    customtokens: Mapped[List["CustomToken"]] = relationship("CustomToken", back_populates="creator_portfolio")
    created_tickets: Mapped[List["Ticket"]] = relationship("Ticket", back_populates="creator_portfolio")
    bought_tickets: Mapped[List["Ticket"]] = relationship("Ticket", back_populates="buying_portfolios")
    verifications: Mapped[List["Verification"]] = relationship("Verification", back_populates="verifiers")



class WatchHistory(db.Model, ModelMixin):
    """
    Representation of a user's watch history, tracking viewing details for library films.

    This class is responsible for maintaining the relationship between a film and its
    watch history details, such as viewing progress, watch count, last watched
    timestamp, and associated bookmarks. It serves as an integral part of the database
    model for tracking user activity and film engagement within a library.

    :ivar library_id: Unique identifier linking the watch history entry to a specific
        library.
    :type library_id: UUID
    :ivar library: Represents the library associated with this watch history entry.
    :type library: Library
    :ivar film_id: Unique identifier linking the watch history entry to a specific
        film.
    :type film_id: UUID
    :ivar film: Represents the film associated with this watch history entry.
    :type film: Film
    :ivar watch_count: The number of times the film has been watched.
    :type watch_count: int
    :ivar current_position: The most recent playback position of the film in seconds.
    :type current_position: float
    :ivar last_watched: The timestamp indicating when the user last accessed the film.
    :type last_watched: datetime
    :ivar bookmarks: A list of bookmarks associated with this watch history entry.
    :type bookmarks: List[Bookmark]
    """
    __tablename__ = "watch_histories"
    library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("libraries.id"), nullable=False)
    library: Mapped["Library"] = relationship("Library", back_populates="watch_history")
    film_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("films.id"), nullable=False)
    film: Mapped["Film"] = relationship("Film", back_populates="watch_histories")
    watch_count: Mapped[int] = mapped_column(Integer, default=0)
    current_position: Mapped[float] = mapped_column(Float, default=0.0) # seconds
    last_watched: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)
    bookmarks: Mapped[List["Bookmark"]] = relationship("Bookmark", back_populates="watch_history")


class Film(db.Model, ModelMixin, EntityMixin, ContributionMixin, ScrollItemMixin, MarkMixin, FanMixin, ReleaseMixin):
    """
    Represents a film entity with various aspects, relationships, and attributes.

    This class is used to define a film entity in the database, encapsulating its
    essential properties and relationships with other entities such as subtitles,
    watch histories, files, streaming links, and other related entities. It serves
    as the central model for handling film-related data and functionalities.

    :ivar runtime: The duration of the film in minutes, if available.
    :type runtime: Optional[int]
    :ivar tagline: The promotional tagline for the film, if specified.
    :type tagline: Optional[str]
    :ivar film_type: The type or category of the film, represented by an enumeration.
    :type film_type: FilmTypeEnum
    :ivar subtitles: The list of subtitles available for the film.
    :type subtitles: Optional[List["Subtitle"]]
    :ivar watch_histories: A list of watch history entries associated with the film.
    :type watch_histories: List["WatchHistory"]
    :ivar files: A list of file entries associated with the film, such as video files.
    :type files: List["File"]
    :ivar streaming_links: The list of streaming links where the film can be viewed.
    :type streaming_links: Optional[List[Link]]
    :ivar trailer_links: The list of trailer links associated with the film.
    :type trailer_links: Optional[List[Link]]
    :ivar nominations: A list of nominations the film has received.
    :type nominations: List["Nomination"]
    :ivar wins: A list of awards or wins achieved by the film.
    :type wins: List["Win"]
    :ivar boxoffice: The box office information associated with the film.
    :type boxoffice: BoxOffice
    :ivar production_companies: A list of production companies involved in making the film.
    :type production_companies: List["ProductionCompany"]
    :ivar production_portfolios: A list of portfolios that have produced this film.
    :type production_portfolios: List["Portfolio"]
    :ivar studios: A list of studios involved in the creation of the film.
    :type studios: List["Studio"]
    :ivar albums: A list of albums related to the film's soundtrack.
    :type albums: List["Album"]
    :ivar collectors: A list of collections where the film is marked as collected.
    :type collectors: List["Collection"]
    :ivar trackers: A list of collections tracking the film.
    :type trackers: List["Collection"]
    :ivar distributors: A list of portfolios acting as distributors for the film.
    :type distributors: List["Portfolio"]
    :ivar characters: A list of characters featured in the film.
    :type characters: List["Character"]
    :ivar gigs: A list of gigs or events related to the film.
    :type gigs: List["Gig"]
    :ivar inspirations: A list of inspirations behind the film.
    :type inspirations: List["Inspiration"]
    """
    __tablename__ = "films"
    __contribution_table__ = film_contributors
    __contribution_back_populates__ = "film_contributions"
    # Film aspects
    runtime: Mapped[Optional[int]] = mapped_column(Integer)
    tagline: Mapped[Optional[str]] = mapped_column(String)
    film_type: Mapped[FilmTypeEnum] = relationship(SQLAlchemyEnum(FilmTypeEnum), nullable=False)
    # Relationships
    subtitles: Mapped[Optional[List["Subtitle"]]] = relationship("Subtitle", back_populates="film")
    watch_histories: Mapped[List["WatchHistory"]] = relationship("WatchHistory", back_populates="film")
    files: Mapped[List["File"]] = relationship("File", back_populates="film")
    streaming_links: Mapped[Optional[List[Link]]] = mapped_column("Link")
    trailer_links: Mapped[Optional[List[Link]]] = mapped_column("Link")
    nominations: Mapped[List["Nomination"]] = relationship('Nomination', back_populates='film')
    wins: Mapped[List["Win"]] = relationship('Win', back_populates='film')
    boxoffice: Mapped["BoxOffice"] = relationship("BoxOffice", back_populates="film")
    production_companies: Mapped[List["ProductionCompany"]] = relationship("ProductionCompany", back_populates="films")
    production_portfolios: Mapped[List["Portfolio"]] = relationship("Portfolio", back_populates="produced_films")
    studios: Mapped[List["Studio"]] = relationship('Studio', back_populates='films')
    albums: Mapped[List["Album"]] = relationship('Album', back_populates='films')
    collectors: Mapped[List['Collection']] = relationship('Collection', back_populates='collected_films')
    trackers: Mapped[List['Collection']] = relationship('Collection', back_populates='tracked_films')
    distributors: Mapped[List['Portfolio']] = relationship('Portfolio', back_populates="distributed_films")
    characters: Mapped[List["Character"]] = relationship("Character", back_populates="films")
    gigs: Mapped[List["Gig"]] = relationship("Gig", back_populates="films")
    inspirations: Mapped[List["Inspiration"]] = relationship("Inspiration", back_populates="films")


class Album(
    db.Model, ModelMixin, WatchListMixin, EntityMixin, ContributionMixin, ScrollItemMixin, MarkMixin, FanMixin,
    ReleaseMixin
):
    """
    Represents an Album entity with various relationships and mixins for additional functionalities.

    This class is used to manage albums, their attributes, and relationships with
    various other entities such as films, collections, distributors, studios, and
    inspirations. Additionally, it leverages multiple mixins for extended
    capabilities related to contributions, watch lists, fan tracking, releases,
    and more.

    :ivar album_type: Specifies the type of the album.
    :type album_type: AlbumTypeEnum
    :ivar films: List of films associated with the album.
    :type films: List[Film]
    :ivar collectors: List of collections that have collected the album.
    :type collectors: List[Collection]
    :ivar trackers: List of collections that track the album.
    :type trackers: List[Collection]
    :ivar distributors: List of portfolios or distributors assigned to the album.
    :type distributors: List[Portfolio]
    :ivar boxoffice: Contains box office data related to the album, if available.
    :type boxoffice: Optional[BoxOffice]
    :ivar studios: List of studios linked to the album.
    :type studios: List[Studio]
    :ivar inspirations: List of inspirations associated with the album.
    :type inspirations: List[Inspiration]
    """
    __tablename__ = 'albums'
    __contribution_table = album_contributors
    __contribution_back_populates = "album_contributions"
    album_type: Mapped[AlbumTypeEnum] = relationship(SQLAlchemyEnum(AlbumTypeEnum), nullable=False)
    films: Mapped[List["Film"]] = relationship('Film', back_populates='albums')
    collectors: Mapped[List['Collection']] = relationship('Collection', back_populates='collected_albums')
    trackers: Mapped[List['Collection']] = relationship('Collection', back_populates='tracked_albums')
    distributors: Mapped[List['Portfolio']] = relationship('Portfolio', back_populates="distributed_albums")
    boxoffice: Mapped[Optional["BoxOffice"]] = relationship("BoxOffice", back_populates="album")
    studios: Mapped[List["Studio"]] = relationship('Studio', back_populates='albums')
    inspirations: Mapped[List["Inspiration"]] = relationship("Inspiration", back_populates="albums")


class Hitlist(db.Model, ModelMixin, WatchListMixin, EntityMixin):
    """
    Representation of a Hitlist entity in the database.

    The Hitlist class extends multiple mixins to provide functionality
    related to database modeling, watchlist features, and general entity
    behavior. It represents a table in the database that stores information
    about hitlists, which can be related to collections and films.

    Attributes provide access to associated collections and films that are
    linked to the hitlist.

    :ivar collectors: The list of collections that include this hitlist as
        a collected item.
    :type collectors: List[Collection]
    :ivar trackers: The list of collections that track this hitlist.
    :type trackers: List[Collection]
    :ivar films: The list of films related to this hitlist.
    :type films: List[Film]
    """
    __tablename__ = 'hitlists'
    __contribution_table = hitlist_contributors
    __contribution_back_populates = "hitlist_contributions"
    collectors: Mapped[List['Collection']] = relationship('Collection', back_populates='collected_hitlists')
    trackers: Mapped[List['Collection']] = relationship('Collection', back_populates='tracked_hitlists')
    films: Mapped[List["Film"]] = relationship('Film', back_populates='hitlists')


class Person(db.Model, ModelMixin, EntityMixin, ContributionMixin, FanMixin, MarkMixin):
    """
    Represents a person entity in the database, providing properties for identifying information,
    biographical details, and relational connections.

    This class is designed to handle detailed information on a person, including names, aliases,
    dates of birth and death, biography text, relationships, and professional summaries, while
    also supporting contributor tracking and relational connections to other entities like careers
    and portfolios. It includes features for integration with user contributions, claiming individuals,
    and linking records to users.

    :ivar first_name: The first name of the person.
    :ivar last_name: The last name of the person.
    :ivar full_name: The full name of the person, combining first and last names.
    :ivar aliases: A list of alternate names or aliases for the person.
    :ivar date_of_birth: The birthdate of the person.
    :ivar date_of_death: The death date of the person, if applicable.
    :ivar bio: A biography or description providing additional details about the person.
    :ivar is_linked: Indicates if the person's record is linked to another entity or not.
    :ivar claimed_by_id: The ID of the user who claimed this person.
    :ivar claimed_by: The user object associated with the ID of the person who claimed this record.
    :ivar profession_summary: A brief summary describing the person's profession.
    :ivar contributors: A list of users who contributed to the person's record.
    :ivar careers: A list of careers associated with the person.
    :ivar relationships: A list of relationships associated with the person.
    :ivar creators: A list of portfolios that include this person as a created entity.
    """
    __tablename__ = 'people'
    __contribution_table__ = person_contributors
    __contribution_back_populates__ = "person_contributions"
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String)
    aliases: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    date_of_birth: Mapped[Optional[datetime]] = mapped_column(Date)
    date_of_death: Mapped[Optional[datetime]] = mapped_column(Date, default=None)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    is_linked: Mapped[bool] = mapped_column(Boolean, default=False)
    claimed_by_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('users.id'))
    claimed_by: Mapped[Optional["User"]] = relationship('User', back_populates='claimed_person')
    profession_summary: Mapped[Optional[str]] = mapped_column(String)
    contributors: Mapped[List["User"]] = relationship('User', back_populates='contributions')
    careers: Mapped[List["Career"]] = relationship('Career', back_populates='person')
    relationships: Mapped[List["Relationship"]] = relationship('Relationship', back_populates='person')
    creators: Mapped[List["Portfolio"]] = relationship('Portfolio', back_populates='created_people')


class Career(db.Model, ModelMixin, EntityMixin):
    """
    Represents a Career entity associated with a person, containing information
    about related characters and gigs.

    This class is part of the database ORM model and defines the structure of
    the career table. It establishes relationships with other tables such as
    people, characters, and gigs.

    :ivar person_id: The unique identifier of the person this career is
        associated with.
    :type person_id: UUID
    :ivar person: The person object associated with this career.
    :type person: Person
    :ivar characters: A list of characters associated with this career, or
        None if there are no characters. The relationship is cascade delete.
    :type characters: Optional[List[Character]]
    :ivar gigs: A list of gigs associated with this career, or None if
        there are no gigs. The relationship is cascade delete.
    :type gigs: Optional[List[Gig]]
    """
    __tablename__ = "careers"
    person_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=False)
    person: Mapped["Person"] = relationship("Person", back_populates="careers")
    characters: Mapped[Optional[List["Character"]]] = relationship("Character", back_populates="career", cascade="all, delete-orphan")
    gigs: Mapped[Optional[List["Gig"]]] = relationship("Gig", back_populates="career", cascade="all, delete-orphan")


class Gig(db.Model, ModelMixin, PeriodMixin):
    """
    Represents a gig entity in the database.

    This class is used to model and manage information related to gigs. A gig
    represents a specific professional engagement, detailing aspects like
    career association, type of crew involvement, and related films. It also
    provides fields to track additional metadata like notes and episode
    associations.

    :ivar career_id: Foreign key linking the gig to a specific career.
    :type career_id: UUID
    :ivar crew_type: The type of crew role associated with the gig.
    :type crew_type: CrewTypeEnum
    :ivar episodes: List of UUIDs representing episodes associated with the gig,
        or None if there are no episodes.
    :type episodes: List[UUID] | None
    :ivar notes: Additional notes or comments about the gig, if any.
    :type notes: str | None
    :ivar is_primary_credit: Indicates whether this gig is considered a primary
        credit for the career.
    :type is_primary_credit: bool
    :ivar career: The Career object associated with the gig.
    :type career: Career
    :ivar films: The Film objects linked to the gig.
    :type films: Film
    """
    __tablename__ = "gigs"
    career_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("careers.id"), nullable=False)
    crew_type: Mapped[CrewTypeEnum] = mapped_column(SQLAlchemyEnum(CrewTypeEnum), nullable=False)
    episodes: Mapped[List["Film"] | None] = mapped_column(ARRAY(UUID(as_uuid=True)), default=list)
    notes: Mapped[str | None] = mapped_column(db.Text, nullable=True)
    is_primary_credit: Mapped[bool] = mapped_column(db.Boolean, default=False)
    career: Mapped["Career"] = relationship("Career", back_populates="gigs")
    films: Mapped["Film"] = relationship("Film", back_populates="gigs")


class Character(db.Model, ModelMixin, EntityMixin, PeriodMixin):
    """
    Represents a Character entity in the database.

    This class models a character with attributes for aliases, career associations,
    participation dates, film appearances, and other related details. It includes
    relationships to careers and films to establish interlinked data.

    :ivar aliases: A list of alternate names or aliases for the character.
    :type aliases: list[str]
    :ivar career_id: The unique identifier of the associated career.
    :type career_id: UUID.
    :ivar start_date: The date when the character's career or activity started.
    :type start_date: datetime or None
    :ivar end_date: The date when the character's career or activity ended.
    :type end_date: datetime or None
    :ivar episodes: A list of films or episodes this character appeared in.
    :type episodes: list[Film] or None
    :ivar notes: Optional notes or additional information about the character.
    :type notes: str or None
    :ivar career: The Career entity associated with the character.
    :type career: Career
    :ivar films: The films associated with this character.
    :type films: Film
    """
    __tablename__ = "characters"
    aliases: Mapped[list[str]] = mapped_column(ARRAY(db.String), default=list)
    career_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("careers.id"), nullable=False)
    start_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    episodes: Mapped[List["Film"] | None] = mapped_column(ARRAY(UUID(as_uuid=True)), default=list)
    notes: Mapped[str | None] = mapped_column(db.Text, nullable=True)
    career: Mapped["Career"] = relationship("Career", back_populates="characters")
    films: Mapped["Film"] = relationship("Film", back_populates="characters")


class Relationship(db.Model, ModelMixin):
    """
    Represents a relationship between two people with details about the type and duration.

    This class models a relationship in a database, where two people are related to each other in
    a specified way (e.g., family, colleague, acquaintance). It includes references to the related
    people, the type of the relationship, and optional start and end dates to define the duration
    of the relationship. This model uses SQLAlchemy for ORM mapping.

    :ivar __tablename__: The name of the database table for the Relationship model.
    :type __tablename__: str
    :ivar person_id: The unique identifier (UUID) of the person associated with this relationship.
    :type person_id: UUID
    :ivar related_person_id: The unique identifier (UUID) of the related person in this relationship.
    :type related_person_id: UUID
    :ivar relationship_type: The type of relationship between the two people (e.g., family, colleague).
    :type relationship_type: RelationshipTypeEnum
    :ivar start_date: The optional start date of the relationship.
    :type start_date: datetime | None
    :ivar end_date: The optional end date of the relationship.
    :type end_date: datetime | None
    :ivar person: The ORM relationship to the associated person.
    :type person: Person
    :ivar related_person: The ORM relationship to the related person.
    :type related_person: Person
    """
    __tablename__ = "relationships"
    person_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=False)
    related_person_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=False)
    relationship_type: Mapped[RelationshipTypeEnum] = mapped_column(SQLAlchemyEnum(RelationshipTypeEnum), nullable=False)
    start_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    person = relationship("Person", foreign_keys=[person_id], back_populates="relationships")
    related_person = relationship("Person", foreign_keys=[related_person_id], back_populates="relationships")


class Shop(db.Model, ModelMixin, EntityMixin, HiveMixin):
    """
    Represents a shop entity used in the application's database model.

    This class defines a shop within the system, linking associated libraries
    and merchandise. It serves as the model for shops in a relational database,
    providing relationships to entities such as `Library` and `Merchandise`.
    The shop is a key part in the data structure, integrating various
    application functionalities and dependencies.

    :ivar library: Represents the library associated with the shop. A shop has
        a one-to-one or one-to-many relationship with a `Library`.
    :type library: Mapped[Library]
    :ivar merchandise: Represents the list of merchandise items associated with
        the shop. This establishes a one-to-many relationship with
        `Merchandise`.
    :type merchandise: Mapped[List[Merchandise]]
    """
    __tablename__ = "shops"
    library: Mapped["Library"] = relationship("Library", back_populates="shops")
    merchandise: Mapped[List["Merchandise"]] = relationship("Merchandise", back_populates="shop")


class Asset(db.Model, ModelMixin, EntityMixin, CreatedMixin, OwnedMixin):
    """
    Represents an Asset entity in the system, which links a portfolio, a token, and merchandise with an associated
    amount. This class encapsulates the relationships and key properties for each asset, facilitating operations
    on assets in the system.

    Stores the necessary information for mapping an asset to other entities such as portfolios, tokens, and
    merchandise, along with metadata for database operations.

    :ivar portfolio_id: The unique identifier of the related portfolio.
    :type portfolio_id: UUID
    :ivar token_id: The unique identifier of the related token.
    :type token_id: UUID
    :ivar merchandise_id: The unique identifier of the related merchandise.
    :type merchandise_id: UUID
    :ivar amount: The quantity of the asset, defaulting to 0.0.
    :type amount: float
    :ivar customtoken: Relationship to the linked custom token entity.
    :type customtoken: CustomToken
    :ivar portfolio: Relationship to the linked portfolio entity.
    :type portfolio: Portfolio
    :ivar merchandise: Relationship to the linked merchandise entity.
    :type merchandise: Merchandise
    """
    __tablename__ = "assets"
    portfolio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("portfolios.id"), nullable=False)
    token_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("customtokens.id"), nullable=False)
    merchandise_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("merchandises.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    customtoken: Mapped["CustomToken"] = relationship("CustomToken", back_populates="asset")
    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="assets")
    merchandise: Mapped["Merchandise"] = relationship("Merchandise", back_populates="asset")


class Merchandise(db.Model, ModelMixin, EntityMixin):
    """
    Represents a merchandise entity within the database.

    This class is designed to model the merchandise available in a shop context, including pricing, inventory
    details, and relationships to other entities such as assets, shops, listings, and discounts. It integrates
    with SQLAlchemy ORM for database interaction and provides a way to organize and manage merchandise-related
    data efficiently.

    :ivar asset_id: The unique identifier of the related asset.
    :type asset_id: UUID
    :ivar shop_id: The unique identifier of the related shop.
    :type shop_id: UUID
    :ivar price: The price of the merchandise. Defaults to 0.0.
    :type price: float
    :ivar inventory_count: The current inventory count for the merchandise. Defaults to 0.
    :type inventory_count: int
    :ivar inventory_limit: The maximum allowed inventory for the merchandise. Defaults to 0.
    :type inventory_limit: int
    :ivar asset: Relationship to the related Asset entity. Represents the asset associated with this
        merchandise.
    :type asset: Asset
    :ivar shop: Relationship to the related Shop entity. Represents the shop offering this merchandise.
    :type shop: Shop
    :ivar listings: Relationship to the Listing entities. Represents the listings where the merchandise
        is advertised or sold.
    :type listings: list[List["Listing"]]
    :ivar discounts: Relationship to the Discount entities. Represents the discounts available for this
        merchandise.
    :type discounts: list[List["Discount"]]
    """
    __tablename__ = "merchandises"
    asset_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("assets.id"), nullable=False)
    shop_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("shops.id"), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    inventory_count: Mapped[int] = mapped_column(Integer, default=0)
    inventory_limit: Mapped[int] = mapped_column(Integer, default=0)
    asset: Mapped["Asset"] = relationship("Asset", back_populates="merchandise")
    shop: Mapped["Shop"] = relationship("Shop", back_populates="merchandise")
    listings: Mapped[List["Listing"]] = relationship("Listing", back_populates="merchandise")
    discounts: Mapped[List["Discount"]] = relationship("Discount", back_populates="merchandise")


class Wallet(db.Model, ModelMixin, EntityMixin):
    """
    Represents a wallet entity in the database.

    The Wallet class is used to model a wallet which is associated with a library
    in the database. It contains relationships to the library it belongs to, as
    well as to the funds that it manages.

    :ivar library_id: The unique identifier of the library that this wallet
        belongs to.
    :type library_id: UUID
    :ivar library: The library entity that this wallet is associated with.
    :type library: Library
    :ivar funds: The collection of funds managed by this wallet.
    :type funds: Fund
    """
    __tablename__ = "wallets"
    library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("libraries.id"), nullable=False)
    library: Mapped["Library"] = relationship(back_populates="wallet")
    funds: Mapped["Fund"] = relationship("Fund", back_populates="wallet")


class Accolade(db.Model, ModelMixin):
    """
    Represents an accolade in the application.

    This class is used as a database model for storing information about accolades.
    An accolade is a significant recognition or award that can be associated with
    other entities in the application such as a calendar or a collection of wins.

    :ivar title: The title of the accolade. This is a non-nullable string that serves
        as the primary descriptor of the accolade.
    :type title: str
    :ivar calendar: The calendar associated with the accolade. Represents a relationship
        with the Calendar entity where the calendar acts as the owner of the accolade.
    :type calendar: Calendar
    :ivar wins: A list of wins associated with the accolade. Represents a relationship
        with the Win entity where accolades can have multiple wins.
    :type wins: list[Win]
    """
    __tablename__ = "accolades"
    title: Mapped[str] = mapped_column(String, nullable=False)
    calendar: Mapped["Calendar"] = relationship(back_populates="owner")
    wins: Mapped[list["Win"]] = relationship('Win', back_populates='accolade')


class Partners(db.Model, ModelMixin):
    """
    Represents a collection of partner entities related to various platforms, distribution,
    and production for media and entertainment.

    This class is a database model using SQLAlchemy, designed to manage information about
    partners such as streaming platforms, distributors, studios, and more. It defines relationships
    to other entities in the database and serves as a central linkage for associated data.

    :ivar streaming_platforms: Represents the list of related streaming platforms.
    :type streaming_platforms: List[StreamingPlatform]
    :ivar peers_platforms: Represents the list of related peer platforms.
    :type peers_platforms: List[PeersPlatform]
    :ivar social_platforms: Represents the list of related social media platforms.
    :type social_platforms: List[SocialPlatform]
    :ivar websites: Represents the list of associated websites.
    :type websites: List[Website]
    :ivar distributors: Represents the list of associated distributors.
    :type distributors: List[Distributor]
    :ivar theatres: Represents the list of associated theaters.
    :type theatres: List[Theatre]
    :ivar the_box_office_id: Foreign key identifier linking to a corresponding box office entity.
    :type the_box_office_id: UUID
    :ivar the_box_office: Represents the associated box office entity.
    :type the_box_office: TheBoxOffice
    :ivar studios: Represents the list of associated studios.
    :type studios: List[Studio]
    :ivar production_companies: Represents the list of associated production companies.
    :type production_companies: List[ProductionCompany]
    """
    __tablename__ = "partners"
    streaming_platforms: Mapped[List["StreamingPlatform"]] = relationship("StreamingPlatform")
    peers_platforms: Mapped[List["PeersPlatform"]] = relationship("PeersPlatform")
    social_platforms: Mapped[List["SocialPlatform"]] = relationship("SocialPlatform")
    websites: Mapped[List["Website"]] = relationship("Website")
    distributors: Mapped[List["Distributor"]] = relationship("Distributor")
    theatres: Mapped[List["Theatre"]] = relationship("Theatre")
    the_box_office_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("theboxoffices.id"), nullable=True)
    the_box_office: Mapped["TheBoxOffice"] = relationship("TheBoxOffice")
    studios: Mapped[List["Studio"]] = relationship("Studio")
    production_companies: Mapped[List["ProductionCompany"]] = relationship("ProductionCompany")


class ProductionCompany(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    """
    Represents a production company entity within the database.

    This class defines a production company, which includes its relationships
    with films it has produced. It is designed to interact with the database
    using SQLAlchemy ORM and integrate model mixins for additional functionality.

    :ivar films: List of films associated with this production company.
    :type films: List[Film]
    """
    __tablename__ = "production_companies"
    films: Mapped[List["Film"]] = relationship("Film", back_populates="production_companies")


class Studio(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    """
    Handles the definition and representation of a Studio, including its relationships
    to associated Films and Albums within a database model.

    The Studio class serves as part of an ORM system and represents entities capable
    of managing relationships to specific sets of Film and Album objects. It includes
    mixins for extended functionality and is mapped to a relational database table
    via SQLAlchemy.

    :ivar films: List of associated Film objects linked to the Studio.
    :type films: List[Film]
    :ivar albums: List of associated Album objects linked to the Studio.
    :type albums: List[Album]
    """
    __tablename__ = "studios"
    films: Mapped[List["Film"]] = relationship("Film", back_populates="studios")
    albums: Mapped[List["Album"]] = relationship("Album", back_populates="studios")


class StreamingPlatform(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    """
    Represents a streaming platform entity within the system.

    This class is used for managing streaming platform entities, including
    storage, retrieval, and manipulation of streaming platform data. It combines
    functionality from several mixins to enhance its capabilities such as database
    integration, entity operations, and partner links management.

    :ivar id: Unique identifier of the streaming platform.
    :type id: int
    :ivar name: Name of the streaming platform.
    :type name: str
    :ivar description: Brief description of the streaming platform.
    :type description: str
    :ivar is_active: Flag indicating whether the streaming platform is active.
    :type is_active: bool
    """
    __tablename__ = "streaming_platforms"


class PeersPlatform(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    """
    Represents the PeersPlatform model in the database.

    This class defines the structure for the `peers_platforms` table in the database. It contains
    attributes describing a specific peer platform and includes additional mixins for functionality
    like entity management, partner links, and model convenience methods.
    """
    __tablename__ = "peers_platforms"


class SocialPlatform(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    """
    Represents a social platform entity in the database.

    This class defines the structure and behavior of a social platform entity, including
    attributes used to store and manage data related to social platforms. It is integrated
    with database modeling and additional mixins to enhance its functionality.

    :ivar id: Unique identifier for the social platform.
    :type id: int
    :ivar name: Name of the social platform.
    :type name: str
    """
    __tablename__ = "social_platforms"


class Website(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    """
    Represents a website entity within the database model.

    This class is an extension of several mixins and acts as the primary model for
    storing and managing website-related data. It defines the structure and behavior
    of website database objects through the use of SQLAlchemy and other mixins.
    """
    __tablename__ = "websites"


class Distributor(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    """
    Represents a distributor entity in the system.

    This class is a database model that defines the structure and attributes
    of a distributor. It includes mixins that provide extended functionality
    such as model behavior, entity-specific features, and partner link
    management. It is mapped to the "distributors" table in the database.
    """
    __tablename__ = "distributors"


class Theatre(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    """
    Represents a theater entity within the application.

    This class provides a detailed representation of a theater entity stored
    in the application database. It inherits functionality from multiple
    mixins to include database operations, entity behaviors, and relationships
    with partner links.

    It serves as the primary model to interact with and manage theaters' data,
    including attributes and behavior that define a theater entity.
    """
    __tablename__ = "theatres"


class TheBoxOffice(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    """
    Represents a central entity for managing box offices within the system.

    This class is used to define and interact with a collection of box offices.
    It integrates functionalities provided by ModelMixin, EntityMixin, and
    PartnerLinksMixin to handle database operations and entity management
    specific to the application. The `boxoffices` relationship links the
    TheBoxOffice entity to one or more BoxOffice entities.

    :ivar boxoffices: A list of associated BoxOffice instances linked to this
                     TheBoxOffice entity via a relationship.
    :type boxoffices: List[BoxOffice]
    """
    __tablename__ = "theboxoffices"
    boxoffices: Mapped[List["BoxOffice"]] = relationship("BoxOffice", back_populates="theboxoffice")


class BoxOffice(db.Model, ModelMixin, EntityMixin):
    """
    Represents the BoxOffice entity, encompassing financial details of films and related relationships.

    The BoxOffice class is a database model used to store information about the financial
    statistics of films, including budget and revenue, while maintaining relationships with
    other entities such as films, albums, and theboxoffice. This class provides mechanisms
    for linking and managing related objects in the database.

    :ivar film_id: Unique identifier linking the box office record to a specific film.
    :type film_id: UUID
    :ivar film: Relationship object mapping the box office to its associated film.
    :type film: Film
    :ivar album_id: Unique identifier linking the box office record to a specific album.
    :type album_id: UUID
    :ivar album: Relationship object mapping the box office to its associated album.
    :type album: Album
    :ivar budget: Stores the financial budget allocated for the film, with high precision.
    :type budget: float
    :ivar revenue: Stores the revenue amount generated by the film, with high precision.
    :type revenue: float
    :ivar theboxoffice_id: Unique identifier linking the box office record to a parent
        entity called theboxoffice.
    :type theboxoffice_id: UUID
    :ivar theboxoffice: Relationship object mapping the box office to its associated
        theboxoffice entity.
    :type theboxoffice: TheBoxOffice
    """
    __tablename__ = "boxoffices"
    film_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("films.id"), nullable=False)
    film: Mapped["Film"] = relationship("Film", back_populates="boxoffice")
    album_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("albums.id"), nullable=False)
    album: Mapped["Album"] = relationship("Album", back_populates="boxoffice")
    budget: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    revenue: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    theboxoffice_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("theboxoffices.id"), nullable=False)
    theboxoffice: Mapped["TheBoxOffice"] = relationship("TheBoxOffice", back_populates="boxoffices")


class AwardType(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    """
    Represents the AwardType class.

    This class is a model for the award_types table. It provides the
    structure and behavior for award type entries, including various
    mixins for additional functionalities. Used as part of the database
    models to represent and handle award types effectively.
    """
    __tablename__ = "award_types"


class Award(db.Model, ModelMixin, EntityMixin):
    """
    Represents an award entity in the database.

    This class maps to the "awards" table in the database and is used for
    managing award-related data. It inherits from both `db.Model`, which
    provides the core ORM functionality, and `ModelMixin`, `EntityMixin`
    to leverage additional behaviors or utilities. The class serves as a
    data model to represent awards and provides the necessary structure
    and logic for interacting with award records in the database.
    """
    __tablename__ = "awards"


class Win(db.Model, ModelMixin, EntityMixin, PeriodMixin):
    """
    Represents a `Win` model that stores information about awards, accolades, and other achievements
    associated with various entities such as films, albums, people, and hitlists.

    This class is designed to map database records to objects in the application using an ORM
    (Object-Relational Mapping) framework. It extends several mixins for shared behavior, providing
    methods and properties that facilitate handling of periods, entities, and other model-specific
    functionalities. The model includes associations to related entities such as rewards, awards, accolades,
    films, albums, hitlists, and people, as well as the portfolios of winners.

    The `Win` model is used to represent instances of awards granted to entities for their achievements.

    :ivar reward_id: Identifier of the associated reward.
    :type reward_id: Optional[UUID]
    :ivar reward: Relationship to the `Reward` entity.
    :type reward: Reward
    :ivar award_id: Identifier of the associated award.
    :type award_id: Optional[UUID]
    :ivar award: Relationship to the `Award` entity.
    :type award: Award
    :ivar accolade_id: Identifier of the associated accolade.
    :type accolade_id: Optional[UUID]
    :ivar accolade: Relationship to the `Accolade` entity.
    :type accolade: Accolade
    :ivar film_id: Identifier of the associated film.
    :type film_id: Optional[UUID]
    :ivar film: Relationship to the `Film` entity.
    :type film: Film
    :ivar album_id: Identifier of the associated album.
    :type album_id: Optional[UUID]
    :ivar album: Relationship to the `Album` entity.
    :type album: Album
    :ivar hitlist_id: Identifier of the associated hitlist.
    :type hitlist_id: Optional[UUID]
    :ivar hitlist: Relationship to the `Hitlist` entity.
    :type hitlist: Hitlist
    :ivar person_id: Identifier of the associated person.
    :type person_id: Optional[UUID]
    :ivar person: Relationship to the `Person` entity.
    :type person: Person
    :ivar winners: List of portfolios representing the winners associated with the `Win`.
    :type winners: List[Portfolio]
    """
    __tablename__ = "wins"
    reward_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("rewards.id"), nullable=True)
    reward: Mapped["Reward"] = relationship("Reward", back_populates="wins")
    award_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("awards.id"), nullable=True)
    award: Mapped["Award"] = relationship("Award", back_populates="nominations")
    accolade_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("accolades.id"), nullable=True)
    accolade: Mapped["Accolade"] = relationship("Accolade", back_populates="wins")
    film_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("films.id"), nullable=True)
    film: Mapped["Film"] = relationship("Film", back_populates="wins")
    album_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("albums.id"), nullable=True)
    album: Mapped["Album"] = relationship("Album", back_populates="wins")
    hitlist_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("hitlists.id"), nullable=True)
    hitlist: Mapped["Hitlist"] = relationship("Hitlist", back_populates="wins")
    person_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=True)
    person: Mapped["Person"] = relationship("Person", back_populates="wins")
    winners: Mapped[List["Portfolio"]] = relationship(back_populates="wins")


class Nomination(db.Model, ModelMixin, EntityMixin):
    """
    Represents a nomination for an award or accolade.

    This class defines the relationships between a nomination and its associated
    entities such as rewards, awards, accolades, films, albums, hitlists,
    people, and nominees. It is designed to interact with an underlying
    database schema, providing the mapping and relationships necessary for
    handling nominations in the application. The class uses SQLAlchemy
    to define these mappings and establish the relationships.

    :ivar reward_id: The identifier of the associated reward.
    :type reward_id: Optional[UUID]
    :ivar reward: The associated reward instance.
    :type reward: Reward
    :ivar award_id: The identifier of the associated award.
    :type award_id: Optional[UUID]
    :ivar award: The associated award instance.
    :type award: Award
    :ivar accolade_id: The identifier of the associated accolade.
    :type accolade_id: Optional[UUID]
    :ivar accolade: The associated accolade instance.
    :type accolade: Accolade
    :ivar film_id: The identifier of the associated film.
    :type film_id: Optional[UUID]
    :ivar film: The associated film instance.
    :type film: Film
    :ivar album_id: The identifier of the associated album.
    :type album_id: Optional[UUID]
    :ivar album: The associated album instance.
    :type album: Album
    :ivar hitlist_id: The identifier of the associated hitlist.
    :type hitlist_id: Optional[UUID]
    :ivar hitlist: The associated hitlist instance.
    :type hitlist: Hitlist
    :ivar person_id: The identifier of the associated person.
    :type person_id: Optional[UUID]
    :ivar person: The associated person instance.
    :type person: Person
    :ivar nominees: A list of portfolios representing nominees for the nomination.
    :type nominees: List[Portfolio]
    """
    __tablename__ = "nominations"
    reward_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("rewards.id"), nullable=True)
    reward: Mapped["Reward"] = relationship("Reward", back_populates="wins")
    award_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("awards.id"), nullable=True)
    award: Mapped["Award"] = relationship("Award", back_populates="nominations")
    accolade_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("accolades.id"), nullable=True)
    accolade: Mapped["Accolade"] = relationship("Accolade", back_populates="wins")
    film_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("films.id"), nullable=True)
    film: Mapped["Film"] = relationship("Film", back_populates="wins")
    album_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("albums.id"), nullable=True)
    album: Mapped["Album"] = relationship("Album", back_populates="wins")
    hitlist_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("hitlists.id"), nullable=True)
    hitlist: Mapped["Hitlist"] = relationship("Hitlist", back_populates="wins")
    person_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=True)
    person: Mapped["Person"] = relationship("Person", back_populates="wins")
    nominees: Mapped[List["Portfolio"]] = relationship(back_populates="nominations")


class Inspiration(db.Model, ModelMixin, EntityMixin):
    """
    Represents an inspiration entity in the database.

    This class defines the relationship and structure for the Inspiration entity, which serves
    to link various inspiration sources, such as films and albums, in a relational database
    schema. The entity includes properties that define relationships with other tables/models
    and attributes corresponding to database columns.

    :ivar films: A list of related Film objects associated with this inspiration.
    :type films: List[Film]
    :ivar albums: A list of related Album objects associated with this inspiration.
    :type albums: List[Album]
    :ivar inspiration_source_id: The unique identifier for the related inspiration source.
    :type inspiration_source_id: UUID
    :ivar inspiration_source: The related inspiration source object linked to this inspiration.
    :type inspiration_source: InspirationSource
    """
    __tablename__ = "inspirations"
    films: Mapped[List["Film"]] = relationship("Film", back_populates="inspirations")
    albums: Mapped[List["Album"]] = relationship("Album", back_populates="inspirations")
    inspiration_source_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("inspiration_sources.id"), nullable=False)
    inspiration_source: Mapped["InspirationSource"] = relationship("InspirationSource", back_populates="inspirations")


class InspirationSource(db.Model, ModelMixin, EntityMixin):
    """
    Represents a source of inspiration.

    This class models an inspiration source which can be linked to multiple
    inspirations. It establishes a relationship where an inspiration source can
    be associated with various inspirations through a bidirectional mapping.

    :ivar inspirations: List of associated inspirations linked to this
        inspiration source. Represents a one-to-many relationship between the
        inspiration source and inspirations.
    :type inspirations: List[Inspiration]
    """
    __tablename__ = "inspiration_sources"
    inspirations: Mapped[List["Inspiration"]] = relationship("Inspiration", back_populates="inspiration_source")


class Release(db.Model, ModelMixin, EntityMixin):
    """
    Represents a release within the database schema.

    This class defines the structure and behavior of a release entity in the
    database. It manages how release data is stored, retrieved, and manipulated,
    and serves as a central model for handling all interactions related to a
    release. It inherits functionality from `db.Model`, `ModelMixin`, and
    `EntityMixin` to provide the basic features of database modeling, such as
    querying and persisting data, as well as additional utilities from the mixins.

    :ivar __tablename__: Name of the database table associated with this model.
    :type __tablename__: str
    """
    __tablename__ = "releases"


class LocalLibrary(db.Model, ModelMixin):
    """
    Representation of a local library in the database.

    This class serves as a model for a local library, storing information about
    its associated library, directories, and the file path to the local library.
    It is used as part of the database schema and includes relationships with
    other tables like Library and Directory.

    :ivar library_id: Unique identifier of the associated library.
    :type library_id: UUID
    :ivar library: Relationship to the associated Library instance.
    :type library: Library
    :ivar directories: List of related Directory instances.
    :type directories: List[Directory]
    :ivar path: File path that represents the local library's location.
    :type path: str
    """
    __tablename__ = "local_libraries"
    library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("libraries.id"))
    library: Mapped["Library"] = relationship("Library", back_populates="local_libraries")
    directories: Mapped[List["Directory"]] = relationship("Directory", back_populates="local_library")
    path: Mapped[str] = mapped_column(String, nullable=False)


class Directory(db.Model, ModelMixin):
    """
    Represents a directory in the database model.

    The Directory class is a database model that defines the structure of
    a directory object and its relationships within the database. It is
    used to represent directories associated with a local library, containing
    a collection of files and having a specific path.

    :ivar local_library_id: The UUID of the associated local library.
    :type local_library_id: UUID
    :ivar local_library: The associated instance of the Library model.
    :type local_library: Library
    :ivar files: A list of File objects associated with this directory.
    :type files: List[File]
    :ivar path: The filesystem path of the directory.
    :type path: str
    """
    __tablename__ = "directories"
    local_library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("local_libraries.library_id"))
    local_library: Mapped["Library"] = relationship("Library", back_populates="directories")
    files: Mapped[List["File"]] = relationship("File", back_populates="directory")
    path: Mapped[str] = mapped_column(String, nullable=False)


class File(db.Model, ModelMixin):
    """
    Represents a file entity in the database.

    This class defines the structure and relationships for the `files` table. It stores
    information about files, such as their attributes, associated directories, tags, and
    optional relationships to films. It supports integration with SQLAlchemy ORM for database
    operations.

    :ivar filepath: The file path of the file.
    :type filepath: str
    :ivar filename: The name of the file.
    :type filename: str
    :ivar file_title: The title of the file.
    :type file_title: str
    :ivar file_year: The year associated with the file.
    :type file_year: Optional[int]
    :ivar file_resolution: The resolution of the file (e.g., 1080p).
    :type file_resolution: Optional[str]
    :ivar file_extension: The extension type of the file.
    :type file_extension: ExtensionTypeEnum
    :ivar file_codec: The codec used in the file.
    :type file_codec: Optional[str]
    :ivar file_bitrate: The bitrate of the file, in bits per second.
    :type file_bitrate: Optional[int]
    :ivar size: The size of the file in bytes.
    :type size: int
    :ivar directory_id: The ID of the directory containing the file.
    :type directory_id: UUID
    :ivar file_tag_set_id: The ID of the file's associated tag set.
    :type file_tag_set_id: UUID
    :ivar directory: The directory object associated with the file.
    :type directory: Directory
    :ivar file_tag_set: The tag set object associated with the file.
    :type file_tag_set: FileTagSet
    :ivar is_film: Indicates whether the file is classified as a film.
    :type is_film: bool
    :ivar is_subtitle: Indicates whether the file is a subtitle file.
    :type is_subtitle: bool
    :ivar is_media: Indicates whether the file is a media file.
    :type is_media: bool
    :ivar film_id: The ID of the associated film, if applicable.
    :type film_id: Optional[UUID]
    :ivar film: The film object associated with the file, if applicable.
    :type film: Film
    """
    __tablename__ = "files"
    filepath: Mapped[str] = mapped_column(String, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    file_title: Mapped[str] = mapped_column(String, nullable=False)
    file_year: Mapped[Optional[int]] = mapped_column(Integer)
    file_resolution: Mapped[Optional[str]] = mapped_column(String)
    file_extension: Mapped[ExtensionTypeEnum] = mapped_column(SQLAlchemyEnum(ExtensionTypeEnum), nullable=False)
    file_codec: Mapped[Optional[str]] = mapped_column(String)
    file_bitrate: Mapped[Optional[int]] = mapped_column(Integer)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    directory_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("directories.id"))
    file_tag_set_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("file_tag_sets.id"))
    directory: Mapped["Directory"] = relationship("Directory", back_populates="files")
    file_tag_set: Mapped["FileTagSet"] = relationship("FileTagSet", back_populates="file")
    is_film: Mapped[bool] = mapped_column(Boolean, default=False)
    is_subtitle: Mapped[bool] = mapped_column(Boolean, default=False)
    is_media: Mapped[bool] = mapped_column(Boolean, default=False)
    film_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("films.id"))
    film: Mapped["Film"] = relationship("Film", back_populates="files")


class FileTagSet(db.Model, ModelMixin):
    """
    Represents a set of metadata tags associated with a file.

    This class models a tagging system for files in a media directory.
    It supports relationships with files, directories, albums, and
    studios, while also maintaining categorized sets of tags such as
    root tags, type tags, categories, and genres.

    :ivar file_id: Unique identifier of the associated file.
    :type file_id: UUID
    :ivar film_directory_id: Unique identifier of the associated film directory.
    :type film_directory_id: UUID
    :ivar file: Relationship to the associated File entity.
    :type file: File
    :ivar film_directory: Relationship to the associated Directory entity.
    :type film_directory: Directory
    :ivar root_tags: List of root-level tags for categorizing the file.
    :type root_tags: list[str]
    :ivar type_tags: List of tags pertaining to the type of the file.
    :type type_tags: list[str]
    :ivar cate_genres: List of categories or genres associated with the file.
    :type cate_genres: list[str]
    :ivar album_tags: List of related Album entities (optional).
    :type album_tags: Optional[List[Album]]
    :ivar studio_tags: List of related Studio entities (optional).
    :type studio_tags: Optional[List[Studio]]
    """
    __tablename__ = "file_tag_sets"
    file_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("files.id"))
    film_directory_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("directories.id"))
    file: Mapped["File"] = relationship("File", back_populates="file_tag_set")
    film_directory: Mapped["Directory"] = relationship("Directory", foreign_keys=[film_directory_id])
    root_tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    type_tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    cate_genres: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    album_tags: Mapped[Optional[List[Album]]] = relationship("Album")
    studio_tags: Mapped[Optional[List[Studio]]] = relationship("Studio")
