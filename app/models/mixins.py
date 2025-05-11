import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSONB, Integer, Float, Text, ARRAY, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.schema import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr, backref

from ..extensions import db
from utils.config import (
    ContentTypeEnum, CliqueTypeEnum, VisibilityEnum, ArticleReportStatusEnum, HiveTypeEnum, SubmissionStatusEnum
)

if TYPE_CHECKING:
    from .user import User
    from .scrolls import Scroll, ScrollEntry
    from .library import Library, Film, Asset
    from .journal import Analyst
    from .community import Thread, Tier, Creator, Founder, Owner, Moderator, Fandom
    from .commerce import AmberToken
    from .calendar import Calendar
    from .common import (
        WikiTemplate, DashboardTemplate, Tag, Keyword, Language, Country, Nationality, Era, Anchor, Theme, Genre,
        Field, Verification, Link, DataSet, Icon, Logo, Image, Avatar, Poster, Video, Figure
    )


def generate_uuid():
    """
    Generate a universally unique identifier (UUID).

    This function generates and returns a string representation of a new UUID
    (version 4). It creates a randomly generated identifier guaranteed to be unique.

    :return: A string representation of the generated UUID.
    :rtype: str
    """
    return str(uuid.uuid4())


class ModelMixin:
    """
    Represents a mixin for database models, providing common attributes and relationships.

    The class serves as a mixin to define shared attributes for database models, such as IDs,
    timestamps, audit attributes (created_by and deleted_by), and relationships with other
    models. It is designed to facilitate consistency across different database tables where
    these attributes are commonly required.

    :ivar id: The unique identifier for the model instance.
    :type id: uuid.UUID
    :ivar created_at: The timestamp for when the model instance was created. Defaults to
        the current datetime.
    :type created_at: datetime
    :ivar created_by: The identifier of the user or entity who created the model instance.
    :type created_by: uuid.UUID
    :ivar updated_at: The timestamp for when the model instance was last updated. Updated
        automatically on changes; defaults to the current datetime.
    :type updated_at: datetime
    :ivar deleted_at: The timestamp for when the model instance was deleted. Defaults to
        None, indicating the instance has not been deleted.
    :type deleted_at: Optional[datetime]
    :ivar deleted_by: The identifier of the user or entity who deleted the model instance.
        Defaults to None.
    :type deleted_by: uuid.UUID
    :ivar wiki_templates: A list of related `WikiTemplate` objects, representing the
        associated wiki templates. Defaults to None.
    :type wiki_templates: Optional[List[WikiTemplate]]
    :ivar dashboard_templates: A list of related `DashboardTemplate` objects, representing
        the associated dashboard templates. Defaults to None.
    :type dashboard_templates: Optional[List[DashboardTemplate]]
    :ivar fields: A list of related `Field` objects, representing additional fields
        linked to the model instance. Defaults to None.
    :type fields: Optional[List[Field]]
    :ivar confidence_score: The confidence score associated with the instance. Defaults
        to 0.0. Maybe None if not applicable.
    :type confidence_score: Optional[float]
    :ivar confidence_score_report: A dictionary containing detailed information about
        confidence scores or reports related to the instance. Defaults to an empty
        dictionary.
    :type confidence_score_report: dict
    """
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), default=None, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    deleted_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), default=None)
    wiki_templates: Mapped[Optional[List["WikiTemplate"]]] = relationship(back_populates="model")
    dashboard_templates: Mapped[Optional[List["DashboardTemplate"]]] = relationship(back_populates="model")
    fields: Mapped[Optional[List["Field"]]] = relationship("Field", back_populates="model")
    confidence_score: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    confidence_score_report: Mapped[dict] = mapped_column(JSONB, default={})


class EntityMixin:
    """
    Represents a common mixin to provide shared attributes and relationships for entities.

    This mixin is intended to be used as a base class for models that share similar
    attributes, relationships, and behavior. It includes fields for basic metadata,
    such as verification and activation status, as well as support for associated media,
    settings, and relationships with other entities.

    :ivar name: The name of the entity.
    :type name: str
    :ivar description: A brief textual description of the entity.
    :type description: Optional[str]
    :ivar slug: A unique slug identifier for the entity.
    :type slug: str
    :ivar is_active: Indicates whether the entity is active.
    :type is_active: bool
    :ivar is_verified: Indicates whether the entity is verified.
    :type is_verified: bool
    :ivar is_deleted: Indicates whether the entity is marked as deleted.
    :type is_deleted: bool
    :ivar settings: Additional settings or configuration for the entity, stored as a key-value structure.
    :type settings: Optional[dict]
    :ivar calendar_id: The UUID of the associated calendar object.
    :type calendar_id: uuid.UUID
    :ivar calendar: The associated calendar entity related to the entity.
    :type calendar: Calendar
    :ivar verification_id: The UUID of the associated verification object.
    :type verification_id: uuid.UUID
    :ivar verification: The associated verification entity related to the entity.
    :type verification: Verification
    :ivar images: A list of related Image objects for the entity.
    :type images: Optional[List[Image]]
    :ivar icons: A list of related Icon objects for the entity.
    :type icons: Optional[List[Icon]]
    :ivar avatars: A list of related Avatar objects for the entity.
    :type avatars: Optional[List[Avatar]]
    :ivar posters: A list of related Poster objects for the entity.
    :type posters: Optional[List[Poster]]
    :ivar videos: A list of related Video objects for the entity.
    :type videos: Optional[List[Video]]
    :ivar figures: A list of related Figure objects for the entity.
    :type figures: Optional[List[Figure]]
    :ivar links: A list of related Link objects for the entity.
    :type links: Optional[List[Link]]
    :ivar logos: A list of related Logo objects for the entity.
    :type logos: Optional[List[Logo]]
    :ivar backdrops: A list of related Image objects used as backdrops for the entity.
    :type backdrops: Optional[List[Image]]
    """
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    settings: Mapped[Optional[dict]] = mapped_column(JSONB, default={})
    calendar_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("calendars.id"), default=None, nullable=False)
    calendar: Mapped["Calendar"] = relationship(back_populates="entities", uselist=False)
    verification_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("verifications.id"), default=None, nullable=False)
    verification: Mapped["Verification"] = relationship(back_populates="Entity", uselist=False)
    images: Mapped[Optional[List["Image"]]] = relationship("Image", back_populates="use_cases")
    icons: Mapped[Optional[List["Icon"]]] = relationship("Icon", back_populates="use_cases")
    avatars: Mapped[Optional[List["Avatar"]]] = relationship("Avatar", back_populates="use_cases")
    posters: Mapped[Optional[List["Poster"]]] = relationship("Poster", back_populates="use_cases")
    videos: Mapped[Optional[List["Video"]]] = relationship("Video", back_populates="use_cases")
    figures: Mapped[Optional[List["Figure"]]] = relationship("Figure", back_populates="use_cases")
    links: Mapped[Optional[List["Link"]]] = relationship("Link", back_populates="use_cases")
    logos: Mapped[Optional[List["Logo"]]] = relationship("Logo", back_populates="use_cases")
    backdrops: Mapped[Optional[List["Image"]]] = relationship("Image", back_populates="use_cases")


class ContributionMixin:
    """
    A mixin class designed to handle contribution-related data and behavior.

    This class provides attributes and relationships to manage contribution data,
    including old and new data fields stored as JSONB, issued AmberTokens, and a
    dynamic relationship with contributors. It serves as a base class for any
    model requiring contribution-tracking capabilities and expects certain class
    attributes (`__contribution_table__` and `__contribution_backref__`) to be
    defined for the contributor relationship to function correctly.

    :ivar old_data: Stores the previous state of contribution-related data as a JSONB object.
    :ivar new_data: Stores the updated state of contribution-related data as a JSONB object.
    :ivar ambertokens_issued: A list of `AmberToken` objects issued after contributions.
    """
    old_data: Mapped[Optional[dict]] = mapped_column(JSONB, default={})
    new_data: Mapped[Optional[dict]] = mapped_column(JSONB, default={})
    ambertokens_issued: Mapped[List["AmberToken"]] = relationship("AmberToken", back_populates="contributions")

    # noinspection PyMethodParameters
    @declared_attr
    def contributors(cls):
        """
        A declared attribute that dynamically creates a relationship for contributors.

        This attribute establishes a many-to-many relationship between the current
        class and the `Contributor` class using the specified secondary table and backref
        name. The class must define `__contribution_table__` and `__contribution_backref__`
        as attributes to specify the mapping table and the backref configuration,
        respectively. If these attributes are not implemented, an error will be raised.

        :return: A dynamic relationship to `Contributor` using the specified
                 secondary table and backref.
        :rtype: sqlalchemy.orm.RelationshipProperty

        :raises NotImplementedError: If the class does not define both
                                      `__contribution_table__` and
                                      `__contribution_backref__`.
        """
        table = getattr(cls, "__contribution_table__", None)
        backref_name = getattr(cls, "__contribution_backref__", None)

        if not table or not backref_name:
            raise NotImplementedError(
                f"{cls.__name__} must define a __contribution_table__ and __contribution_backref__ class attribute"
            )
        return relationship(
            "Contributor",
            secondary=table,
            backref=backref(backref_name, lazy="dynamic"),
        )


class PeriodMixin:
    """
    A mixin class for defining a period with a start and end time.

    This class provides attributes for specifying a time period. It is designed
    to be used as a mixin in other classes where start and end times for a given
    period are required. The `start_time` and `end_time` should typically be
    initialized with valid datetime values that align with the use case of the
    implementing class.

    :ivar start_time: The start time of the period.
    :type start_time: datetime
    :ivar end_time: The end time of the period.
    :type end_time: datetime
    """
    start_time: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)


class LibraryMixin:
    """
    Mixin class providing a relationship to `Library` objects.

    This class defines a relationship that maps and links the `Library` objects
    to the owning entity. It is intended to provide a convenient way for the
    owning entity to manage and access its associated `Library` objects.

    :ivar libraries: A list of `Library` objects linked to the owning
        entity through this relationship.
    :type libraries: Mapped[List["Library"]]
    """
    libraries: Mapped[List["Library"]] = relationship("Library", back_populates="owner")


class ListMixin:
    """
    Mixin for handling associations with lists of Scroll objects.

    Provides functionality for establishing relationships and associations
    between Scroll objects and a parent list. Designed to be used within an
    ORM (Object-Relational Mapping) context.

    :ivar scrolls: Represents the collection of Scroll objects associated
        with the parent list. Back references are managed using the
        `list` attribute of Scroll.
    :type scrolls: Mapped[List["Scroll"]]
    """
    scrolls: Mapped[List["Scroll"]] = relationship("Scroll", back_populates="list")


class MarkMixin:
    """
    Provides a mixin class to associate specific marks or categorizations with an
    entity. This class acts as a helper for relational mappings to various
    categorization models.

    The class defines relationships between an associated entity and a set of
    tags, keywords, languages, themes, genres, countries, nationalities, eras,
    and anchors. These relationships enable the linked entity to be organized,
    queried, and analyzed based on associated attributes like tags or eras.

    Attributes:
        tags: A list of `Tag` objects associated with the entity, defining
              tags for categorization.
        keywords: A list of `Keyword` objects associated with the entity
                  for descriptive identification.
        languages: A list of `Language` objects representing the entity's
                   associated language categories.
        themes: A list of `Theme` objects linked to the entity, representing
                thematic classifications.
        genres: A list of `Genre` objects related to the entity, indicating
                genre-based categorizations.
        countries: A list of `Country` objects linked to the entity for
                   geographical classification.
        nationalities: A list of `Nationality` objects associated with the
                       entity to represent cultural or national identity.
        eras: A list of `Era` objects (Periods) linked to the entity for
              chronological categorization.
        anchors: A list of `Anchor` objects associated with the entity,
                 defining specific points of reference.
    """
    tags: Mapped[Optional[list["Tag"]]] = relationship("Tag", back_populates="marked")
    keywords: Mapped[Optional[list["Keyword"]]] = relationship("Keyword", back_populates="marked")
    languages: Mapped[Optional[list["Language"]]] = relationship("Language", back_populates="marked")
    themes: Mapped[Optional[list["Theme"]]] = relationship("Theme", back_populates="marked")
    genres: Mapped[Optional[list["Genre"]]] = relationship("Genre", back_populates="marked")
    countries: Mapped[Optional[list["Country"]]] = relationship("Country", back_populates="marked")
    nationalities: Mapped[Optional[list["Nationality"]]] = relationship("Nationality", back_populates="marked")
    eras: Mapped[Optional[list["Era"]]] = relationship("Period", back_populates="marked")
    anchors: Mapped[Optional[list["Anchor"]]] = relationship("Anchor", back_populates="marked")


class CliqueMixin:
    """
    Mixin class providing attributes and relationships for cliques.

    This class is an SQLAlchemy mixin intended to define the attributes and relationships
    needed for a generic "clique" model. It represents a group of users with specific
    roles and a designated type. The mixin integrates with users through a relationship
    and supports storing role definitions in a JSONB format. The `clique_type` defines
    the type of the clique using an enumerated value. This class is intended to be used
    as part of larger ORM models.

    :ivar agents: Relationship to the `User` model representing a list of users
        associated with this clique.
    :type agents: List[User]
    :ivar clique_type: Enumerated type specifying the category of the clique.
    :type clique_type: CliqueTypeEnum
    :ivar roles: JSONB field used to store roles associated with users in the
        clique. Defaults to an empty dictionary.
    :type roles: dict
    """
    agents: List["User"] = relationship("User", back_populates="cliques")
    clique_type: Mapped[CliqueTypeEnum] = mapped_column(SQLAlchemyEnum(CliqueTypeEnum), nullable=False)
    roles: Mapped[dict] = mapped_column(JSONB, default={})


class HiveMixin(LibraryMixin):
    """
    Represents a HiveMixin class that contains specific attributes and relationships
    to define and manage the functionality of a hive in the domain context.

    This class is primarily used for associating logos, boards, walls, and tiers while
    storing additional information through join rules. It facilitates interaction
    and encapsulation of different entities in a structured, logical hierarchy.

    :ivar logo_id: Unique identifier for the associated logo.
    :type logo_id: uuid.UUID
    :ivar logo: Relationship to the associated Logo instance, not a list.
    :type logo: Logo
    :ivar boards: List of board instances related to this hive.
    :type boards: List[BoardMixin]
    :ivar walls: List of wall instances related to this hive.
    :type walls: List[WallMixin]
    :ivar join_rules: Optional dictionary defining rules for joining the hive.
    :type join_rules: Optional[dict]
    :ivar tiers: List of Tier instances defining the hierarchical structure of the hive.
    :type tiers: List[Tier]
    """
    logo_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("logos.id"), default=None, nullable=False)
    logo: Mapped["Logo"] = relationship(back_populates="use_cases", uselist=False)
    boards: Mapped[List["BoardMixin"]] = relationship("BoardMixin", back_populates="hive")
    walls: Mapped[List["WallMixin"]] = relationship("WallMixin", back_populates="hive")
    join_rules: Mapped[Optional[dict]] = mapped_column(JSONB, default={})
    tiers: Mapped[List["Tier"]] = relationship("Tier", back_populates="hive")


class FanMixin:
    """
    A mixin class for establishing a relationship with a fandom entity.

    This mixin provides attributes and relationships for associating the implementing
    class with a fandom entity. It includes a foreign key to the `fandoms` table through
    `fandom_id` and establishes a relationship with the `Fandom` entity.

    :ivar fandom_id: The foreign key column linking to the `fandoms` table. Used to associate
        the entity with a specific fandom.
    :type fandom_id: Mapped[uuid.UUID]
    :ivar fandom: The relationship property for the associated `Fandom` entity. This enables
        ORM-based navigation between the entity and its corresponding fandom.
    :type fandom: Mapped["Fandom"]
    """
    fandom_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("fandoms.id"), default=None)
    fandom: Mapped["Fandom"] = relationship("Fandom", back_populates="entity")


class ContentMixin:
    """
    Provides a mixin for content-related models.

    This mixin adds standardized attributes for managing content identification
    and content type in database models. It utilizes SQLAlchemy's ORM capabilities
    to map the attributes to database columns and ensures type consistency using
    Python type hints and enumerations.

    :ivar content_id: A unique identifier for the content. This is represented
                      as a UUID and is required (not nullable).
    :type content_id: UUID
    :ivar content_type: The type of the content is categorized by a predefined
                        enumeration, `ContentTypeEnum`. This is also a required
                        (not nullable) attribute.
    :type content_type: ContentTypeEnum
    """
    content_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    content_type: Mapped[ContentTypeEnum] = mapped_column(SQLAlchemyEnum(ContentTypeEnum), nullable=False)


class SharableMixin:
    """
    Adds social media sharing-related functionality to a model.

    This mixin provides basic attributes to track the number of views, likes,
    shares, and comments for a particular record. It is designed to be used
    with ORM models where such attributes are relevant and necessary for
    application logic.

    :ivar views: The number of times this object has been viewed.
    :type views: Mapped[int]
    :ivar likes: The number of likes this object has received.
    :type likes: Mapped[int]
    :ivar shares: The number of times this object has been shared.
    :type shares: Mapped[int]
    :ivar comments: The number of comments associated with this object.
    :type comments: Mapped[int]
    """
    views: Mapped[int] = mapped_column(Integer, default=0)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    shares: Mapped[int] = mapped_column(Integer, default=0)
    comments: Mapped[int] = mapped_column(Integer, default=0)


class AuthoredMixin:
    """
    A mixin class to provide authored content functionality.

    The AuthoredMixin class is designed to be used as a mixin for models in an
    application requiring authored content functionality. It includes attributes
    for content publication time, status, visibility, textual content, excerpts,
    revision history, and relationships such as thread association and its foreign
    key relationship. This class is intended to be used within the SQLAlchemy ORM
    context to manage relational database tables efficiently.

    :ivar publish_time: The timestamp indicating when the content is published.
    :type publish_time: DateTime
    :ivar status: The status of the article, represented as an enumerated value
        of `ArticleReportStatusEnum`. Defaults to `UNPUBLISHED`.
    :type status: ArticleReportStatusEnum
    :ivar visibility: The visibility level of the content, represented as an
        enumerated value of `VisibilityEnum`. Defaults to `PUBLIC`.
    :type visibility: VisibilityEnum
    :ivar content: The main textual content of the article. Includes optional
        rich-text editing metadata.
    :type content: str
    :ivar excerpt: A short summary or excerpt of the article content.
    :type excerpt: str
    :ivar revision_history: A list of dictionaries representing the content's
        revision history. Defaults to an empty list.
    :type revision_history: list[dict]
    :ivar thread: The associated thread, linking to the "Thread" model, realized
        with a back-populated relationship to the topic.
    :type thread: Thread
    :ivar thread_id: The unique identifier of the associated thread, represented
        as a UUID foreign key.
    :type thread_id: UUID
    """
    publish_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    status: Mapped[ArticleReportStatusEnum] = mapped_column(SQLAlchemyEnum, default=ArticleReportStatusEnum.UNPUBLISHED)
    visibility: Mapped[VisibilityEnum] = mapped_column(SQLAlchemyEnum, default=VisibilityEnum.PUBLIC)
    content: Mapped[str] = mapped_column(Text, nullable=False, info={"rich_text": "ckeditor"})
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    revision_history: Mapped[list[dict]] = mapped_column(JSONB, default=[])
    thread: Mapped["Thread"] = relationship("Thread", back_populates="topic")
    thread_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("threads.id"))


class PerksMixin:
    """
    Summary of what the class does.

    This mixin class provides functionality to associate perks with different tiers in a
    database relationship. It is used to add this relationship functionality to other
    classes that incorporate it. This association is established via a mapped relationship.

    The purpose of this class is to define a link between perks and tiers, allowing ORM
    tools to manage these relationships effectively. The setup enables bidirectional
    navigation and data integrity when working with tiers and their related perks.

    :ivar tiers: Represents a mapped database relationship linking a list of Tier objects
        to their associated perks.
    :type tiers: Mapped[List[Tier]]
    """
    tiers: Mapped[List["Tier"]] = relationship("Tier", back_populates="perks")


class BoardMixin:
    """
    A mixin class representing a board entity in the system.

    This class defines the attributes and relationships associated with a board,
    such as its unique identifier, related hive, type of hive, and its moderators.
    Used to describe the interactions and structure of a board within the larger
    system context.

    :ivar hive_id: The unique identifier for the hive associated with the board.
    :type hive_id: uuid.UUID
    :ivar hive: The hive associated with the board.
    :type hive: HiveMixin
    :ivar hive_type: The type of hive associated with the board.
    :type hive_type: HiveTypeEnum
    :ivar moderators: List of moderators managing the board.
    :type moderators: List[Moderator]
    """
    hive_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    hive: Mapped["HiveMixin"] = relationship(HiveMixin, foreign_keys=[hive_id], back_populates="boards")
    hive_type: Mapped[HiveTypeEnum] = mapped_column(SQLAlchemyEnum(HiveTypeEnum), nullable=False)
    moderators: Mapped[List["Moderator"]] = relationship("Moderator", back_populates="boards")


class WallMixin:
    """
    Mixin class for wall-related data and behavior in a database model.

    WallMixin provides attributes and relationships specific to the wall entity,
    allowing integration with related models such as hives and moderators. This
    mixin facilitates associating a wall instance with its corresponding hive
    and moderators while specifying important properties like the hive type.

    :ivar hive_id: Unique identifier for the hive associated with the wall.
    :type hive_id: uuid.UUID
    :ivar hive: Relationship to the `HiveMixin` model, representing the hive
        associated with the wall.
    :type hive: "HiveMixin"
    :ivar hive_type: Enumeration representing the type of the hive associated
        with the wall. The value is derived from the `HiveTypeEnum`.
    :type hive_type: HiveTypeEnum
    :ivar moderators: List of relationships to the `Moderator` model,
        representing moderators associated with the wall.
    :type moderators: List["Moderator"]
    """
    hive_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    hive: Mapped["HiveMixin"] = relationship(HiveMixin, foreign_keys=[hive_id], back_populates="walls")
    hive_type: Mapped[HiveTypeEnum] = mapped_column(SQLAlchemyEnum(HiveTypeEnum), nullable=False)
    moderators: Mapped[List["Moderator"]] = relationship("Moderator", back_populates="walls")


class WatchListMixin(ListMixin, MarkMixin):
    """
    Mixin class that provides functionality for managing and associating watchlists
    with films, along with handling original and derived watchlists.

    This class is meant to be used as part of an object relational mapping (ORM)
    system, integrating with a database to manage associations between films and
    watchlists. It includes attributes for storing related film objects and UUIDs
    representing original and derived watchlists.

    :ivar films: A list of `Film` objects associated with this watchlist.
    :ivar original_watchlists: A list of UUIDs corresponding to the original
        watchlists associated with this instance.
    :ivar derived_watchlists: A list of UUIDs corresponding to the derived
        watchlists associated with this instance.
    """
    films: Mapped[List["Film"]] = relationship("Film", back_populates="watchlists")
    original_watchlists: Mapped[List[UUID]] = mapped_column(ARRAY(UUID(as_uuid=True)), default=[])
    derived_watchlists: Mapped[List[UUID]] = mapped_column(ARRAY(UUID(as_uuid=True)), default=[])


class ScrollItemMixin:
    """
    Mixin that provides functionality for scroll items.

    This class represents a mixin for defining and managing scroll items. It includes
    relationships to scroll entries and defines attributes such as scrollpoints.
    The mixin can be used as part of an object-relational mapping (ORM) with a database.

    :ivar scroll_entries: The relationship to the list of associated scroll entries.
    :type scroll_entries: Mapped[List[ScrollEntry]]
    :ivar scrollpoints: The number of scroll points associated with the scroll item.
    :type scrollpoints: Mapped[int]
    """
    scroll_entries: Mapped[List["ScrollEntry"]] = relationship("ScrollEntry", back_populates="scroll_item")
    scrollpoints: Mapped[int] = mapped_column(Integer, default=0)


class MediaMixin:
    """
    Provides common attributes and relationships for media-related entities.

    This mixin is designed to be used in models that involve media assets, providing attributes
    and relationships for keywords, anchors, URLs, alternative text descriptions, associated
    assets, and their corresponding use cases.

    :ivar keywords: A list of associated keywords for the media entity.
    :type keywords: list[Keyword] or None
    :ivar anchors: A list of anchors linked to the media entity.
    :type anchors: list[Anchor] or None
    :ivar url: The URL of the media entity. This value is required.
    :type url: str
    :ivar use_cases: A list of use cases (models) associated with the media entity.
    :type use_cases: list[ModelMixin] or None
    :ivar alt_text: The alternative text description of the media entity, primarily used for
        accessibility purposes.
    :type alt_text: str or None
    :ivar asset_id: The unique identifier of the related asset, if any.
    :type asset_id: uuid.UUID or None
    :ivar asset: The related asset object linked to the media entity.
    :type asset: Asset or None
    """
    keywords: Mapped[Optional[list["Keyword"]]] = relationship("Keyword", back_populates="marked")
    anchors: Mapped[Optional[list["Anchor"]]] = relationship("Anchor", back_populates="marked")
    url: Mapped[str] = mapped_column(String, nullable=False)
    use_cases: Mapped[Optional[List[ModelMixin]]] = relationship("ModelMixin", back_populates="media")
    alt_text: Mapped[Optional[str]] = mapped_column(String)
    asset_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id"))
    asset: Mapped[Optional["Asset"]] = relationship("Asset", back_populates="media")


class ReleaseMixin:
    """
    A mixin class representing release-related metadata and statistics.

    This class encapsulates attributes related to a release, including titles,
    dates, ratings, external data, and statistical information. It is designed
    to be used in systems that manage media objects such as movies or shows,
    providing detailed metadata and tracking various aspects like popularity
    and reviews.

    :ivar title: Title of the release.
    :ivar original_title: Original title of the release, if different from the main title.
    :ivar release_date: Date when the release occurred.
    :ivar release_year: Year of the release.
    :ivar synopsis: Synopsis or summary of the release content.
    :ivar available_locally: Indicates whether the release is available locally.
    :ivar submission_status: Current submission status of the release.
    :ivar imdb_id: IMDB ID for the release.
    :ivar tmdb_id: TMDB ID for the release.
    :ivar imdb_rating: IMDB rating for the release.
    :ivar imdb_votes: Number of votes used to calculate the IMDB rating.
    :ivar tmdb_rating: TMDB rating for the release.
    :ivar tmdb_votes: Number of votes used to calculate the TMDB rating.
    :ivar rotten_tomatoes_rating: Rotten Tomatoes rating for the release.
    :ivar metascore: Metascore rating for the release.
    :ivar awards_string: String representation of awards won by the release.
    :ivar imdb_data: External data from IMDB in JSON format.
    :ivar tmdb_data: External data from TMDB in JSON format.
    :ivar omdb_data: External data from OMDB in JSON format.
    :ivar contributor_amber_points: Points contributed by users related to this release.
    :ivar popularity_score: Popularity score of the release.
    :ivar total_watch_count: Total number of watches logged for the release.
    :ivar total_scroll_reviews: Total number of scroll reviews received.
    :ivar scroll_stats: Statistical data about scroll reviews in JSON format.
    """
    title: Mapped[str] = mapped_column(String, nullable=False)
    original_title: Mapped[Optional[str]] = mapped_column(String)
    release_date: Mapped[Optional[datetime]] = mapped_column(Date)
    release_year: Mapped[Optional[int]] = mapped_column(Integer)
    synopsis: Mapped[Optional[str]] = mapped_column(Text)
    available_locally: Mapped[bool] = mapped_column(Boolean, default=False)
    submission_status: Mapped[SubmissionStatusEnum] = mapped_column(SQLAlchemyEnum(SubmissionStatusEnum), default=SubmissionStatusEnum.PENDING)
    # External stats
    imdb_id: Mapped[Optional[str]] = mapped_column(String)
    tmdb_id: Mapped[Optional[int]] = mapped_column(Integer)
    imdb_rating: Mapped[Optional[float]] = mapped_column(Float)
    imdb_votes: Mapped[Optional[int]] = mapped_column(Integer)
    tmdb_rating: Mapped[Optional[float]] = mapped_column(Float)
    tmdb_votes: Mapped[Optional[int]] = mapped_column(Integer)
    rotten_tomatoes_rating: Mapped[Optional[float]] = mapped_column(Float)
    metascore: Mapped[Optional[int]] = mapped_column(Integer)
    awards_string: Mapped[Optional[str]] = mapped_column(String)
    # External data
    imdb_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    tmdb_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    omdb_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    # Amber aspects
    contributor_amber_points: Mapped[float] = mapped_column(Float, default=0.0)
    popularity_score: Mapped[float] = mapped_column(Float, default=0.0)
    total_watch_count: Mapped[int] = mapped_column(Integer, default=0)
    total_scroll_reviews: Mapped[int] = mapped_column(Integer, default=0)
    scroll_stats: Mapped[Optional[dict]] = mapped_column(JSONB, default={})


class ChartMixin:
    """
    A mixin class for handling chart-related data.

    This class is designed to provide a relationship mapping for chart-related
    datasets. It establishes an association with the `DataSet` entity through the
    `Mapped` type hint and uses SQLAlchemy's relationship API to manage the
    bidirectional relationship. This mixin is intended to be used in chart or graph
    models where datasets are required.

    :ivar data_sets: A relationship mapping that links this chart mixin
                     to a list of `DataSet` objects. This property uses
                     SQLAlchemy's `relationship` function for a `back_populates`
                     connection with the `DataSet` model.
    :type data_sets: Mapped[List[DataSet]]
    """
    data_sets: Mapped[List["DataSet"]] = relationship("DataSet", back_populates="graphs_charts")


class CreatedMixin:
    """
    Mixin class that provides attributes and relationships for creator information and certification details.

    This class is designed to be used in scenarios requiring the tracking of entities' creators or storage
    of certification-related metadata. It leverages SQLAlchemy's ORM features for relationship and column
    definitions, ensuring efficient mapping and retrieval of data.

    :ivar creators: List of related creator entities linked to the mixin.
    :type creators: List[Creator]
    :ivar certification: Dictionary containing certification metadata.
    :type certification: dict
    """
    creators: Mapped[List["Creator"]] = relationship("Creator", back_populates="creations")
    certification: Mapped[dict] = mapped_column(JSONB, default={})


class AnalyzedMixin:
    """
    Mixin class that provides functionality related to analysis tracking.

    This class represents a mixin that links entities to analysts, allowing for
    tracking, queries, and relationships concerning analysis. It is designed to be
    used as a part of an object-relational mapping (ORM) model, allowing entities
    to share a many-to-many relationship with analysts. This can be useful in
    situations where entities are associated with multiple analysts or contributors
    and require relational mapping for data analysis workflows.

    :ivar analysts: List of analysts associated with the entity. Each analyst
        represents a contributor or individual involved in the entity's analysis.
    :type analysts: list of Analyst
    """
    analysts: Mapped[List["Analyst"]] = relationship("Analyst", back_populates="hives")


class FoundedMixin:
    """
    Mixin class providing attributes and relationships related to the concept of founders and
    certifications.

    The class is designed to be used as a mixin to add functionality and data related to founders
    and certifications to another SQLAlchemy model. It includes a relationship with a "Founder"
    entity and manages certification information as a JSONB column.

    :ivar founders: Relationship linking the entity to a list of associated "Founder" entities.
    :ivar certification: JSONB column storing certification-related information in a dictionary format.
    """
    founders: Mapped[List["Founder"]] = relationship("Founder", back_populates="foundlings")
    certification: Mapped[dict] = mapped_column(JSONB, default={})


class OwnedMixin:
    """
    Mixin class to represent ownership-related attributes.

    This class is designed to provide attributes and relationships for ownership
    management in a database schema. It allows tracking of owners associated with
    an entity and store ownership certifications in a structured format.

    :ivar owners: List of owners associated with the entity.
    :type owners: Mapped[List["Owner"]]
    :ivar ownership_certification: A dictionary containing ownership certification
        details, stored in JSONB format.
    :type ownership_certification: Mapped[dict]
    """
    owners: Mapped[List["Owner"]] = relationship("Owner", back_populates="holdings")
    ownership_certification: Mapped[dict] = mapped_column(JSONB, default={})


class PartnerLinksMixin:
    """
    Provides functionality to mix in partner link-related attributes.

    This mixin is designed to be used in database models representing partners.
    It introduces attributes that facilitate the storage and relationships of
    partner-specific endpoints and links. Use this mixin to ensure a consistent
    implementation of partner link data across multiple database models.

    :ivar endpoints: A JSONB column storing partner endpoints as key-value pairs.
    :type endpoints: dict
    :ivar links: A relationship containing a list of links associated with the
        partner. Links are back-populated via the "partner" relationship.
    :type links: Optional[List[Link]]
    """
    endpoints: Mapped[dict] = mapped_column(JSONB, default={})
    links: Mapped[Optional[List["Link"]]] = relationship("Link", back_populates="partner")
