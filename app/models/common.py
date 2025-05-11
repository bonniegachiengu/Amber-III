import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, Boolean, ForeignKey, JSONB, Date, Float, Text, ARRAY, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Enum as SQLAlchemyEnum

from ..extensions import db
from .utils.config import ContentTypeEnum
from .mixins import (
    ModelMixin, MediaMixin, ContentMixin, ContributionMixin, EntityMixin, ChartMixin, OwnedMixin, CreatedMixin,
    PartnerLinksMixin
)
from .associations import (
    dashboard_template_contributors, wiki_template_contributors, tag_contributors, language_contributors,
    country_contributors, nationality_contributors, era_contributors, genre_contributors, theme_contributors,
    keyword_contributors, report_template_contributors, verification_contributors
)


if TYPE_CHECKING:
    from .user import User
    from .journal import Report
    from .library import Portfolio, Library
    from .calendar import Event



class Field(db.Model, ModelMixin):
    """
    Represents a database entity for fields in a model.

    This class is used to represent and manage fields associated with a specific
    model within the database. It includes information about the field's
    associated model ID, type, confidence weight, and confidence score, as well as
    a relationship to its parent model.

    :ivar model_id: Unique identifier of the associated model.
    :type model_id: uuid.UUID
    :ivar model_type: Type of the associated model.
    :type model_type: str
    :ivar model: Relationship to the parent model that this field belongs to.
    :type model: ModelMixin
    :ivar confidence_weight: Weight representing the confidence level of this field.
    :type confidence_weight: float
    :ivar confidence_score: Score indicating the confidence value of this field.
    :type confidence_score: float
    """
    __tablename__ = "fields"
    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    model_type: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped["ModelMixin"] = relationship("ModelMixin", foreign_keys=[model_id], back_populates="fields")
    confidence_weight: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)


class Preferences(db.Model, ModelMixin):
    """
    Represents the preferences associated with a library.

    This class serves as a database model for storing preferences related to a
    specific library. It includes a reference to the library it belongs to and
    a set of preferences stored as a JSONB object.

    :ivar library_id: The unique identifier of the associated library.
    :type library_id: uuid.UUID
    :ivar library: The relationship to the Library model representing the
        library with which these preferences are associated.
    :type library: Library
    :ivar preferences: The configuration or settings data for the library,
        represented as a JSONB object.
    :type preferences: dict
    """
    __tablename__ = "preferences"
    library_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), primary_key=True)
    library: Mapped["Library"] = relationship("Library", back_populates="preferences")
    preferences: Mapped[dict] = mapped_column(JSONB, default={})


class DashboardTemplate(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a dashboard template in the database.

    The DashboardTemplate class is a database model that defines the structure for
    storing and retrieving information about dashboard templates. It uses SQLAlchemy
    as an ORM and includes mixins for additional functionality. The class manages
    relationships with models, overviews, and widgets.

    :ivar model_id: The primary key identifier for the dashboard template.
    :type model_id: uuid.UUID
    :ivar model_type: The type of model associated with the dashboard template.
    :type model_type: str
    :ivar model: The associated model instance for this dashboard template.
    :type model: ModelMixin
    :ivar overviews: A list of overview instances linked to this dashboard template.
    :type overviews: list[Overview]
    :ivar widgets: A list of widget instances linked to this dashboard template.
    :type widgets: list[Widget]
    """
    __tablename__ = "dashboard_templates"
    __contribution_table__ = dashboard_template_contributors
    __contribution_backref__ = "dashboard_template_contributions"
    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    model_type: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped["ModelMixin"] = relationship("ModelMixin", foreign_keys=[model_id], back_populates="dashboard_templates")
    overviews: Mapped[List["Overview"]] = relationship("Overview", back_populates="dashboard_template")
    widgets: Mapped[List["Widget"]] = relationship("Widget", back_populates="dashboard_template")


class Overview(db.Model, ModelMixin):
    """
    Represents the overview information associated with a dashboard template.

    This class extends `db.Model` and `ModelMixin`. It defines the data model for
    storing overview information related to a specific dashboard template. The
    overview includes content details and establishes a relationship with its
    corresponding dashboard template.

    :ivar dashboard_template_id: UUID identifier of the related dashboard template.
    :type dashboard_template_id: uuid.UUID
    :ivar dashboard_template: The associated `DashboardTemplate` object. This
        specifies the relationship and connection to the DashboardTemplate model.
    :type dashboard_template: DashboardTemplate
    :ivar content: The content data for the overview is represented as a dictionary.
    :type content: dict
    """
    __tablename__ = "overviews"
    dashboard_template_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("dashboard_templates.id"), primary_key=True)
    dashboard_template: Mapped["DashboardTemplate"] = relationship("DashboardTemplate", back_populates="overviews")
    content: Mapped[dict] = mapped_column(JSONB, default={})


class Widget(db.Model, ModelMixin):
    """
    Represents a Widget, which is a component linked to a Dashboard Template.

    This class is a database model that defines the structure of the `Widget`
    table and its relationships in the database. A Widget is associated with
    a Dashboard Template, and it contains specific configuration or content
    in JSON format. The purpose of this class is to facilitate the
    representation and manipulation of Widgets within the application.

    :ivar dashboard_template_id: Unique identifier of the associated Dashboard
        Template.
    :type dashboard_template_id: uuid.UUID
    :ivar dashboard_template: Relationship to the Dashboard Template this
        Widget is linked to.
    :type dashboard_template: DashboardTemplate
    :ivar content: Additional content or configuration of the Widget is
        represented as a JSON structure.
    :type content: dict
    """
    __tablename__ = "widgets"
    dashboard_template_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("dashboard_templates.id"), primary_key=True)
    dashboard_template: Mapped["DashboardTemplate"] = relationship("DashboardTemplate", back_populates="widgets")
    content: Mapped[dict] = mapped_column(JSONB, default={})


class WikiTemplate(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a wiki template used within the application's system.

    This class serves as a template structure for a wiki-like feature, providing
    sections and relationships to models. It integrates functionality via mixins
    and interacts with contribution-related features. It is stored in the
    database as a model, referenced with the table name `wiki_templates`.

    :ivar model_id: The unique identifier for the model instance.
    :type model_id: uuid.UUID
    :ivar model_type: The type of model, stored as a string with a max length of 100.
    :type model_type: str
    :ivar model: The associated model instance connected to this template.
    :type model: ModelMixin
    :ivar sections: A list of related sections belonging to this wiki template.
    :type sections: List[WikiSection]
    """
    __tablename__ = "wiki_templates"
    __contribution_table__ = wiki_template_contributors
    __contribution_backref__ = "wiki_template_contributions"
    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    model_type: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped["ModelMixin"] = relationship("ModelMixin", foreign_keys=[model_id], back_populates="wiki_templates")
    sections: Mapped[List["WikiSection"]] = relationship("WikiSection", back_populates="wiki_template")


class WikiSection(db.Model, ModelMixin):
    """
    Represents a section of a Wiki template.

    This class is used to define and manage sections of a Wiki template. It stores
    the relationship between a section and its parent Wiki template, along with
    the content data associated with the section. Instances of this class are
    intended to be used as part of a system that organizes and manages hierarchical
    wiki content templates.

    :ivar wiki_template_id: Unique identifier for the associated Wiki template.
    :type wiki_template_id: uuid.UUID
    :ivar wiki_template: The associated WikiTemplate object. Represents the parent
        Wiki template that this section belongs to.
    :type wiki_template: WikiTemplate
    :ivar content: The content data for this section in a JSON-compatible format.
    :type content: dict
    """
    __tablename__ = "wiki_sections"
    wiki_template_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("wiki_templates.id"), primary_key=True)
    wiki_template: Mapped["WikiTemplate"] = relationship("WikiTemplate", back_populates="sections")
    content: Mapped[dict] = mapped_column(JSONB, default={})


class ReportTemplate(db.Model, ModelMixin, ContentMixin, ContributionMixin):
    """
    Represents a template for generating reports.

    This class is used to define and manage templates that can be utilized for
    creating detailed reports. It integrates various mixins to handle database
    models, content management, and contributions. The class also establishes
    relationships with related entities, such as reports, and provides the
    structure for managing content utilized in the templates.

    :ivar content: Stores the content of the report template in a JSONB format.
    :type content: dict
    :ivar reports: Represents a relationship to the associated reports that make
                   use of the template.
    :type reports: List[Report]
    """
    __tablename__ = "report_templates"
    __contribution_table__ = report_template_contributors
    __contribution_backref__ = "report_template_contributions"
    content: Mapped[dict] = mapped_column(JSONB, default={})
    reports: Mapped[List["Report"]] = relationship("Report", back_populates="report_template")


class Anchor(db.Model, ModelMixin):
    """
    Represents the Anchor model which associates content through anchors.

    The Anchor class is a database model used to associate various pieces of content
    through anchors. This allows for linking and organizing content pieces in a
    structured manner. Each instance of Anchor is uniquely identified and has specific
    attributes that describe its type and association with other content entities.

    :ivar marked: List of content entities associated with this anchor.
    :type marked: list[ContentMixin]
    :ivar anchors_type: Type of content associated with the anchor.
    :type anchors_type: ContentTypeEnum
    :ivar anchor_id: Unique identifier for the anchor.
    :type anchor_id: uuid.UUID
    :ivar anchored_content: Content entity that is anchored to this anchor.
    :type anchored_content: ContentMixin
    """
    __tablename__ = "anchors"
    marked: Mapped[List["ContentMixin"]] = relationship("ContentMixin", back_populates="anchors")
    anchors_type: Mapped[ContentTypeEnum] = mapped_column(SQLAlchemyEnum(ContentTypeEnum), nullable=False)
    anchor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    anchored_content: Mapped["ContentMixin"] = relationship("ContentMixin", foreign_keys=[anchor_id], back_populates="anchored")


class Tag(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a tag entity for marking and categorizing content.

    This class defines a tag that can be associated with various content objects.
    It inherits from database and contribution-related mixins to handle persistence
    and contribution functionality. Tags facilitate content organization and can
    be used in multiple contexts where content categorization or tagging is required.

    :ivar marked: List of content objects (of type ContentMixin) that are
        associated with this tag.
    :type marked: List[ContentMixin]
    """
    __tablename__ = "tags"
    __contribution_table__ = tag_contributors
    __contribution_backref__ = "tag_contributions"
    marked: Mapped[List["ContentMixin"]] = relationship("ContentMixin", back_populates="tags")


class Language(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a language entity in the database.

    This class is a database model that defines a language entity. It supports contributions
    through `ContributionMixin`, and serves as a central entity for managing languages by
    allowing relationships with other database entities, such as content marked for a language.

    :ivar marked: Represents a relationship between the language and its associated
                  content. This indicates the content marked in association with
                  this language entity.
    :type marked: List[ContentMixin]
    """
    __tablename__ = "languages"
    __contribution_table__ = language_contributors
    __contribution_backref__ = "language_contributions"
    marked: Mapped[List["ContentMixin"]] = relationship("ContentMixin", back_populates="languages")


class Country(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a country entity within the database.

    This class models a country within the application, leveraging SQLAlchemy's ORM
    capabilities for persistence. It also includes mixins for extending functionality
    related to contribution tracking and general model-related operations. The
    class is linked to contributors through a many-to-many relationship, enabling
    the tracking of contributions specific to a given country.

    :ivar marked: A list representing a many-to-many relationship with `ContentMixin`, used to
        associate specific content with countries. The relationship is bidirectional and
        uses `countries` as the back_populated field.
    :type marked: list[ContentMixin]
    """
    __tablename__ = "countries"
    __contribution_table__ = country_contributors
    __contribution_backref__ = "country_contributions"
    marked: Mapped[List["ContentMixin"]] = relationship("ContentMixin", back_populates="countries")


class Nationality(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a Nationality model for database interaction.

    This class defines the Nationality entity within the database, incorporating various
    mixins to provide extended functionality, such as database model behaviors and data
    contributions. It specifies table mappings and relationships used to track and
    manage nationalities and their related data content.

    :ivar marked: A list of associated ContentMixin objects linked to corresponding
        nationalities.
    :type marked: List[ContentMixin]
    """
    __tablename__ = "nationalities"
    __contribution_table__ = nationality_contributors
    __contribution_backref__ = "nationality_contributions"
    marked: Mapped[List["ContentMixin"]] = relationship("ContentMixin", back_populates="nationalities")


class Era(db.Model, ModelMixin, ContributionMixin):
    """
    Handles the representation and management of eras within the database.

    This class represents the 'eras' table and is responsible for managing the
    attributes and relationships relevant to historical or relevant time periods
    referred to as eras. It supports contributions and associations with
    content marked by these eras.

    :ivar marked: List of content associated with this era.
    :type marked: List[ContentMixin]
    """
    __tablename__ = "eras"
    __contribution_table__ = era_contributors
    __contribution_backref__ = "era_contributions"
    marked: Mapped[List["ContentMixin"]] = relationship("ContentMixin", back_populates="eras")


class Genre(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a genre entity in the database.

    This class models a genre object, mapping it to the "genres" table in the
    database. It integrates with contribution handling and allows relationships
    with associated content. The purpose of this model is to store and manage
    information about various genres that can have contributions or relate to
    other content entities.

    :ivar marked: Relationship with content entities that are marked within the
        genre scope.
    :type marked: List[ContentMixin]
    """
    __tablename__ = "genres"
    __contribution_table__ = genre_contributors
    __contribution_backref__ = "genre_contributions"
    marked: Mapped[List["ContentMixin"]] = relationship("ContentMixin", back_populates="genres")


class Theme(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a theme within the application.

    This class defines a theme entity, including its related contributions and
    relationships with other entities. It acts as a table in the database, storing
    information about themes and their associations with various contents and
    contributors. The class inherits functionalities for database modeling and
    contribution handling.

    :ivar marked: Represents a relationship between themes and contents,
        allowing bidirectional access between them.
    :type marked: List[ContentMixin]
    """
    __tablename__ = "themes"
    __contribution_table__ = theme_contributors
    __contribution_backref__ = "theme_contributions"
    marked: Mapped[List["ContentMixin"]] = relationship("ContentMixin", back_populates="themes")


class Keyword(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a database model for keywords in the application.

    The Keyword class is a part of the database schema and connects to the
    `keywords` table in the database. It inherits from multiple mixins to
    utilize shared functionality pertaining to database models and contribution
    management. Keywords are associated with content items and store
    relationships useful in various application contexts.

    :ivar marked: Defines the many-to-many relationship between `ContentMixin` and
        `Keyword`. Tracks the content items associated with this keyword.
    :type marked: List[ContentMixin]
    """
    __tablename__ = "keywords"
    __contribution_table__ = keyword_contributors
    __contribution_backref__ = "keyword_contributions"
    marked: Mapped[List["ContentMixin"]] = relationship("ContentMixin", back_populates="keywords")


class Verification(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a verification entity within the database.

    This class is used to manage and store details of verifications associated
    with various system entities. It extends `db.Model`, `ModelMixin`, and
    `ContributionMixin` to inherit functionalities for database interaction,
    model behaviors, and contribution tracking. Each verification is linked to
    specific entities and may involve one or more verifiers.

    :ivar entity_id: Unique identifier of the associated entity.
    :type entity_id: uuid.UUID
    :ivar entity_type: Type of the associated entity.
    :type entity_type: str
    :ivar entity: Reference to the associated entity.
    :type entity: EntityMixin
    :ivar verifiers: List of verifiers (portfolios) associated with the verification.
    :type verifiers: List[Portfolio]
    """
    __tablename__ = "verifications"
    __contribution_table__ = verification_contributors
    __contribution_backref__ = "verification_contributions"
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(100), primary_key=True)
    entity: Mapped["EntityMixin"] = relationship("EntityMixin", foreign_keys=[entity_id], back_populates="verification")
    verifiers: Mapped[List["Portfolio"]] = relationship("Portfolio", back_populates="verifications")


class Link(db.Model, ModelMixin):
    """
    Represents a database model for a Link entity.

    This class defines the schema for the "links" table in the database and includes
    relationships with other entities such as Anchor and EntityMixin. It acts as a
    data representation of a link, including its associated anchors and use cases.

    :ivar anchors: List of associated Anchor objects. Represents the anchors
        that are marked with this link.
    :type anchors: Optional[list[Anchor]]
    :ivar url: The URL represented by this Link. It is a required string.
    :type url: str
    :ivar use_cases: List of associated EntityMixin objects. Represents the
        use cases where this link is utilized.
    :type use_cases: Optional[List[EntityMixin]]
    """
    __tablename__ = "links"
    anchors: Mapped[Optional[list["Anchor"]]] = relationship("Anchor", back_populates="marked")
    url: Mapped[str] = mapped_column(String, nullable=False)
    partner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    partner: Mapped['PartnerLinksMixin'] = relationship("PartnerLinksMixin", back_populates="links")
    use_cases: Mapped[Optional[List[EntityMixin]]] = relationship("EntityMixin", back_populates="links")


class Image(db.Model, ModelMixin, MediaMixin):
    """
    Represents an image resource in the application.

    This class is used to manage image-related data stored in the database,
    including metadata such as the name, MIME type, size, and storage path of
    the image. It also tracks the various use cases where the image is used
    within the application.

    :ivar name: The name of the image.
    :ivar mime_type: The MIME type of the image, such as 'image/jpeg' or
        'image/png'.
    :ivar size: The size of the image in bytes.
    :ivar path: The storage path where the image file is located.
    :ivar use_cases: A list of entities where the image is used. It establishes
        a relationship with other entities in the application.
    """
    __tablename__ = "images"
    name: Mapped[str] = mapped_column(String, nullable=False)
    mime_type: Mapped[str] = mapped_column(String, nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False)
    use_cases: Mapped[Optional[List[EntityMixin]]] = relationship("EntityMixin", back_populates="images")


class Avatar(db.Model, ModelMixin, Image):
    """
    Represents an Avatar model within the database, containing relationships to
    other entities and functionality for managing avatars.

    The Avatar class integrates with ModelMixin and Image functionalities and is mapped
    using the SQLAlchemy ORM. It serves to connect various use cases to the avatar and
    manage their associated relationships (e.g., storing references to other entities).

    :ivar use_cases: A list of related EntityMixin objects that the avatar is associated
        with. This establishes a relationship where the avatar can belong to multiple
        entities via the back_populates mechanism.
    :type use_cases: Optional[List[EntityMixin]]
    """
    __tablename__ = "avatars"
    use_cases: Mapped[Optional[List[EntityMixin]]] = relationship("EntityMixin", back_populates="avatar")


class Icon(db.Model, ModelMixin, Image):
    """
    Represents an icon entity within the database.

    This class defines the representation of an icon, its attributes, and any
    relationships it may have with other entities. It is used to store and manage
    icon-related data, while providing database integration and additional
    functionalities via its inheritance.

    :ivar use_cases: Represents a relationship with `EntityMixin` objects where
        the icon is associated with various use cases.
    :type use_cases: Optional[List[EntityMixin]]
    """
    __tablename__ = "icons"
    use_cases: Mapped[Optional[List[EntityMixin]]] = relationship("EntityMixin", back_populates="icon")


class Logo(db.Model, ModelMixin, Image):
    """
    Represents a logo entity within the application's database.

    A `Logo` object is a database model that contains information about a specific
    logo used in the system. It extends functionality from `db.Model`, `ModelMixin`,
    and `Image` classes. This model is used for maintaining relationships with entities
    that use the logo and managing other related characteristics.

    :ivar use_cases: A list of related entities that use this logo. Represents a
        one-to-many relationship with `EntityMixin`.
    :type use_cases: Optional[List[EntityMixin]]
    """
    __tablename__ = "logos"
    use_cases: Mapped[Optional[List[EntityMixin]]] = relationship("EntityMixin", back_populates="logo")


class Poster(db.Model, ModelMixin, MediaMixin, CreatedMixin, OwnedMixin, Image):
    """
    Represents a Poster object, typically used for storing and managing data related to posters in
    the database. Combines multiple mixins and `Image` class to extend functionality.

    The Poster class is built upon SQLAlchemy's `db.Model` and utilizes the following mixins:
    `ModelMixin`, `MediaMixin`, `CreatedMixin`, `OwnedMixin`. It also represents an image-like
    entity and supports relationships with `EntityMixin`.

    :ivar __tablename__: Table name in the database for this model.
    :type __tablename__: str
    :ivar use_cases: A relationship field linking to a list of `EntityMixin` objects, representing
                     the entities associated with this poster.
    :type use_cases: Optional[List[EntityMixin]]
    """
    __tablename__ = "posters"
    use_cases: Mapped[Optional[List[EntityMixin]]] = relationship("EntityMixin", back_populates="posters")


class Video(db.Model, ModelMixin, MediaMixin):
    """
    Handles the representation and functionality associated with video entries in the database.

    This class models a video object with its associated attributes and relationships as part of the ORM
    (Object-Relational Mapping) configuration. It is configured to interact with the "videos" database table
    and provides extensions for mixing in behavior and media-related utility. The relationships and properties
    defined here render this class a suitable abstraction for managing video entities, aligning with ORM
    practices in software development.

    :ivar __tablename__: Name of the database table for this model.
    :type __tablename__: str
    :ivar use_cases: A relationship attribute that links this video entity to a list of associated entities
        of type EntityMixin. This represents the back-population of entities referencing this video.
    :type use_cases: Optional[List[EntityMixin]]
    """
    __tablename__ = "videos"
    use_cases: Mapped[Optional[List[EntityMixin]]] = relationship("EntityMixin", back_populates="videos")


class Figure(db.Model, ModelMixin, ContentMixin, MediaMixin, ChartMixin):
    """
    Represents a figure entity within the database schema.

    The Figure class is used to define a database model for storing information
    associated with a figure. This model inherits functionalities from various
    mixins, enabling additional features such as content handling, media support,
    and chart integration. It is designed for use in the database context.

    :ivar __tablename__: The name of the database table associated with this model.
    :type __tablename__: str
    :ivar use_cases: Relationships to the `EntityMixin` instances associated with
        this figure. These are bidirectional relationships that allow access to
        related figures from `EntityMixin` objects.
    :type use_cases: Optional[List[EntityMixin]]
    """
    __tablename__ = "figures"
    use_cases: Mapped[Optional[List[EntityMixin]]] = relationship("EntityMixin", back_populates="figures")


class Map(db.Model, ModelMixin):
    """
    Represents a map database model and defines the relationship with associated locations.

    This class is used to manage and represent maps in the database. It establishes
    a one-to-many relationship with the "Location" model, implying that a map can contain
    multiple locations. It inherits features from the `db.Model` and `ModelMixin` classes
    to provide database and utility functionality within the application.

    :ivar locations: A list representing related locations associated with this map.
    :type locations: list[Location]
    """
    __tablename__ = "maps"
    locations: Mapped[List["Location"]] = relationship("Location", back_populates="maps")


class Location(db.Model, ModelMixin):
    """
    Represents a geographical location, including relationships to associated
    users, maps, and venues.

    This class is a model in the database representing a specific location, as
    well as information about the users, maps, and venues linked to the location.
    It simplifies queries and operations related to location-based relationships
    by maintaining mapped associations.

    :ivar coordinates: Geographical coordinates of the location.
    :type coordinates: List[float]
    :ivar users: List of user objects associated with the location.
    :type users: List["User"]
    :ivar maps: List of map objects associated with the location.
    :type maps: List["Map"]
    :ivar occasions: List of venue objects that reference this location.
    :type occasions: List["Venue"]
    """
    __tablename__ = "locations"
    coordinates: Mapped[List[float]] = mapped_column(ARRAY(Float))
    users: Mapped[List["User"]] = relationship("User", back_populates="locations")
    maps: Mapped[List["Map"]] = relationship("Map", back_populates="locations")
    occasions: Mapped[List["Venue"]] = relationship("Venue", back_populates="location")


class Venue(db.Model, ModelMixin):
    """
    Represents the data model for a venue in the application.

    This class defines the database schema for venues, their associations, and
    attributes. Venues are linked to specific locations and can host events. It
    provides a blueprint for managing venue-related data in the application.

    :ivar location_id: Unique identifier for the associated location.
    :type location_id: uuid.UUID
    :ivar location: Relationship to the associated `Location` model, representing
        the venue's specific location.
    :type location: Location
    :ivar events: List of `Event` objects associated with the venue, representing
        the events that take place at the venue.
    :type events: List[Event]
    """
    __tablename__ = "venues"
    location_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("locations.id"), primary_key=True)
    location: Mapped["Location"] = relationship("Location", back_populates="occasions")
    events: Mapped[List["Event"]] = relationship("Event", back_populates="venue")


class Axis(db.Model, ModelMixin):
    """
    Represents an axis entity in the database.

    This class defines the structure and relationships associated with an axis, including
    its data, legends, and associated datasets. It inherits from `db.Model` and `ModelMixin`
    to integrate ORM functionalities and common model behaviors. The class primarily stores
    JSON-based structured data and manages a relationship with the `DataSet` model.

    :ivar data: Stores JSON-compatible data as a dictionary.
    :type data: dict
    :ivar legends: Contains legend information represented as a dictionary.
    :type legends: dict
    :ivar data_sets: Represents the relationship with the `DataSet` model, allowing
        access to the associated datasets linked to the axis.
    :type data_sets: List[DataSet]
    """
    __tablename__ = "axes"
    data: Mapped[dict] = mapped_column(JSONB, default={})
    legends: Mapped[dict] = mapped_column(JSONB, default={})
    data_sets: Mapped[List["DataSet"]] = relationship("DataSet", back_populates="axes")


class DataSet(db.Model, ModelMixin, ContentMixin):
    """
    Represents a data set entity in the database.

    This class models a data set, which includes its relationships to other
    entities such as axes and charts. It inherits functionality from
    `db.Model`, `ModelMixin`, and `ContentMixin` to support database
    interaction, model convenience methods, and additional content-related
    attributes or methods.

    :ivar axes: List of `Axis` instances related to the data set.
    :type axes: List[Axis]
    :ivar data_set_type: Type of the data set, stored as a string with a
        maximum length of 100 characters.
    :type data_set_type: str
    :ivar charts: List of `ChartMixin` objects related to the data set.
    :type charts: List[ChartMixin]
    """
    __tablename__ = "data_sets"
    axes: Mapped[List["Axis"]] = relationship("Axis", back_populates="data_sets")
    data_set_type: Mapped[str] = mapped_column(String(100), nullable=False)
    charts: Mapped[List["ChartMixin"]] = relationship("ChartMixin", back_populates="data_sets")


class BarGraph(db.Model, ModelMixin, ContentMixin, ChartMixin):
    """
    Represents a bar graph entity in the database.

    This class is used to define a bar graph model that interacts with the database.
    It inherits from `db.Model` for database integration, and mixins `ModelMixin`,
    `ContentMixin`, and `ChartMixin` for extended functionality like model operations,
    content management, and chart utilities.
    """
    __tablename__ = "bar_graphs"


class LineGraph(db.Model, ModelMixin, ContentMixin, ChartMixin):
    """
    Represents a Line Graph model which integrates with database and different utility mixins.

    This class is used to define and manage the representation, properties, and associated
    behaviors of a line graph. It interacts with the database via SQLAlchemy ORM and includes
    additional mixins for common functionalities. The primary purpose of the LineGraph model
    is to store and handle data related to line graphs effectively. It inherits attributes
    and methods from ModelMixin, ContentMixin, and ChartMixin to extend its functionality.
    """
    __tablename__ = "line_graphs"


class PieChart(db.Model, ModelMixin, ContentMixin, ChartMixin):
    """
    Represents a Pie Chart as part of the database model.

    The PieChart class is a database model that inherits from db.Model, ModelMixin,
    ContentMixin, and ChartMixin. It corresponds to the "pie_charts" table in the
    database. This model is used for the creation and management of pie chart
    objects. It includes chart-specific attributes and integrations with the database.
    """
    __tablename__ = "pie_charts"


class Notification(db.Model, ModelMixin):
    """
    Represents a notification entity in the system.

    The Notification class is used to manage and store notification-related
    data. It includes details such as the sender, recipient, message content,
    read status, and timestamp. Notifications can be used to facilitate
    communication between users and are associated with specific events or
    alerts within the system.

    :ivar recipient_id: The unique identifier of the user receiving the
        notification.
    :type recipient_id: uuid.UUID
    :ivar recipient: The recipient user entity associated with the
        notification.
    :type recipient: Library
    :ivar sender_id: The unique identifier of the user who sent the
        notification.
    :type sender_id: uuid.UUID
    :ivar sender: The sender user entity associated with the notification.
    :type sender: Library
    :ivar message: The content of the notification.
    :type message: str
    :ivar read: Indicates whether the notification has been read.
    :type read: bool
    :ivar timestamp: The date and time when the notification was created.
    :type timestamp: datetime
    """
    __tablename__ = "notifications"
    recipient_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    recipient: Mapped["Library"] = relationship("Library", back_populates="notifications")
    sender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    sender: Mapped["Library"] = relationship("Library", back_populates="sent_notifications")
    message: Mapped[str] = mapped_column(Text, nullable=False)
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    timestamp: Mapped[datetime] = mapped_column(Date, default=datetime.now)
