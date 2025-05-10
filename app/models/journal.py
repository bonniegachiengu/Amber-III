from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, JSONB, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..extensions import db
from .utils.config import EventRepeatEnum, ColumnStatusEnum, VisibilityEnum
from associations import magazine_contributors, column_contributors, article_contributors, report_contributors
from .mixins import (
    EntityMixin, HiveMixin, ModelMixin, ContentMixin, ContributionMixin, SharableMixin, AuthoredMixin, FoundedMixin,
    CliqueMixin, MarkMixin, OwnedMixin, AnalyzedMixin, CreatedMixin
)

if TYPE_CHECKING:
    from .library import Portfolio
    from .community import Thread
    from .common import Image, ReportTemplate


class Journal(db.Model, ModelMixin, EntityMixin, HiveMixin, AnalyzedMixin):
    """
    Represents a journal entity in the database.

    The `Journal` class combines functionality from several mixins and represents
    a journal entity with its related data and relationships in the database.
    This class uses SQLAlchemy ORM with several relationships that define how
    it interacts with other entities in the system. It provides fields to capture
    editorial and organizational structure, as well as associated publications.

    :ivar editor_in_chief: The editor-in-chief of the journal.
    :type editor_in_chief: Editor-in-Chief
    :ivar executive_editors: List of executive editors associated with the journal.
    :type executive_editors: List[ExecutiveEditor]
    :ivar chief_analysts: List of chief analysts associated with the journal.
    :type chief_analysts: List[ChiefAnalyst]
    :ivar chief_correspondents: List of chief correspondents for the journal.
    :type chief_correspondents: List[ChiefCorrespondent]
    :ivar front_pages: List of front pages associated with the journal.
    :type front_pages: List[FrontPage]
    :ivar magazines: List of magazines related to the journal.
    :type magazines: List[Magazine]
    """
    __tablename__ = "journal"
    editor_in_chief: Mapped["EditorInChief"] = relationship("EditorInChief", back_populates="journal")
    executive_editors: Mapped[List["ExecutiveEditor"]] = relationship("ExecutiveEditor", back_populates="journal")
    chief_analysts: Mapped[List["ChiefAnalyst"]] = relationship("ChiefAnalyst", back_populates="journal")
    chief_correspondents: Mapped[List["ChiefCorrespondent"]] = relationship("ChiefCorrespondent", back_populates="journal")
    front_pages: Mapped[List["FrontPage"]] = relationship("FrontPage", back_populates="journal")
    magazines: Mapped[List["Magazine"]] = relationship("Magazine", back_populates="journal")


class Magazine(
    db.Model, ModelMixin, EntityMixin, HiveMixin, ContributionMixin, CreatedMixin, OwnedMixin, AnalyzedMixin, FoundedMixin
):
    """
    Represents a Magazine entity in the database.

    The Magazine class serves as a representation of a magazine entity, providing
    various attributes and relationships to describe its structure, contributors, and
    associations. It is primarily used to model the behavior and relationships of
    a magazine, including its journal, contributors (e.g., editors, writers,
    analysts), and associated content such as articles, reports, and columns.

    :ivar journal_id: The unique identifier of the associated journal.
    :type journal_id: UUID
    :ivar cover_image_id: The unique identifier of the cover image of this magazine.
    :type cover_image_id: UUID
    :ivar chief_editor_id: The unique identifier of the chief editor of this magazine.
    :type chief_editor_id: UUID
    :ivar journal: The relationship linking this magazine to its associated journal.
    :type journal: Journal
    :ivar chief_editor: The relationship linking this magazine to its chief editor.
    :type chief_editor: Editor
    :ivar cover_image: The relationship linking this magazine to its cover image.
    :type cover_image: Image
    :ivar front_pages: A list of front pages associated with the magazine.
    :type front_pages: List[FrontPage]
    :ivar columns: A list of columns associated with the magazine.
    :type columns: List[Column]
    :ivar articles: A list of articles published in the magazine.
    :type articles: List[Article]
    :ivar reports: A list of reports published in the magazine.
    :type reports: List[Report]
    :ivar owners: A list of owners associated with the magazine.
    :type owners: List[Portfolio]
    :ivar founders: A list of founders who created the magazine.
    :type founders: List[Portfolio]
    :ivar editors: A list of editors contributing to the magazine.
    :type editors: List[Editor]
    :ivar correspondents: A list of correspondents contributing to the magazine.
    :type correspondents: List[Correspondent]
    :ivar writers: A list of writers contributing to the magazine.
    :type writers: List[Writer]
    :ivar analysts: A list of analysts related to the magazine's hive.
    :type analysts: List[Analyst]
    """
    __tablename__ = "magazines"
    __contribution_table__ = magazine_contributors
    __contribution_backref__ = "magazine_contributions"
    journal_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("journals.id"))
    cover_image_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("images.id"))
    chief_editor_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("editors.id"))
    journal: Mapped["Journal"] = relationship("Journal", back_populates="magazines")
    chief_editor: Mapped["Editor"] = relationship("Editor", back_populates="magazine")
    cover_image: Mapped["Image"] = relationship("Image")
    front_pages: Mapped[List["FrontPage"]] = relationship("FrontPage", back_populates="magazine")
    columns: Mapped[List["Column"]] = relationship("Column", back_populates="magazine")
    articles: Mapped[List["Article"]] = relationship("Article", back_populates="publishing_magazine")
    reports: Mapped[List["Report"]] = relationship("Report", back_populates="publishing_magazine")
    editors: Mapped[List["Editor"]] = relationship("Editor", back_populates="magazine")
    correspondents: Mapped[List["Correspondent"]] = relationship("Correspondent", back_populates="magazine")
    writers: Mapped[List["Writer"]] = relationship("Writer", back_populates="magazine")


class FrontPage(db.Model, ModelMixin):
    """
    Represents a front page entity that links magazines, journal, and slots.

    This class is modeled as a database table via SQLAlchemy and establishes
    relationships between magazines, journals, and slots. It represents the
    front page of a publication and serves as a reference for organizing
    content for magazines and journals.

    :ivar magazine_id: Identifier of the associated magazine.
    :type magazine_id: UUID
    :ivar journal_id: Identifier of the associated journal.
    :type journal_id: UUID
    :ivar journal: The journal linked to the front page.
    :type journal: Journal
    :ivar magazine: The magazine linked to the front page.
    :type magazine: Magazine
    :ivar slots: A list of slots that are part of the front page.
    :type slots: List[Slot]
    """
    __tablename__ = "front_pages"
    magazine_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("magazines.id"))
    journal_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("journals.id"))
    journal: Mapped["Journal"] = relationship("Journal", back_populates="front_pages")
    magazine: Mapped["Magazine"] = relationship("Magazine", back_populates="front_pages")
    slots: Mapped[List["Slot"]] = relationship("Slot", back_populates="front_page")


class Slot(db.Model, ModelMixin):
    """
    Represents a Slot entity within the database.

    The Slot class is used to define the relationship between different entities such as
    front pages, columns, articles, and reports in a database schema. It establishes the
    correlation between these entities for purposes such as querying, data association,
    and manipulation.

    :ivar front_page_id: ID of the related front page.
    :type front_page_id: UUID
    :ivar column_id: ID of the related column.
    :type column_id: UUID
    :ivar article_id: ID of the related article.
    :type article_id: UUID
    :ivar report_id: ID of the related report.
    :type report_id: UUID
    :ivar front_page: Relationship to the FrontPage entity, enabling back-population of slots.
    :type front_page: FrontPage
    :ivar column: Relationship to the Column entity, enabling back-population of slots.
    :type column: Column
    :ivar article: Relationship to the Article entity, enabling back-population of slots.
    :type article: Article
    :ivar report: Relationship to the Report entity, enabling back-population of slots.
    :type report: Report
    """
    __tablename__ = "slots"
    front_page_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("front_pages.id"))
    column_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("columns.id"))
    article_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("articles.id"))
    report_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("reports.id"))
    front_page: Mapped["FrontPage"] = relationship("FrontPage", back_populates="slots")
    column: Mapped["Column"] = relationship("Column", back_populates="slots")
    article: Mapped["Article"] = relationship("Article", back_populates="slots")
    report: Mapped["Report"] = relationship("Report", back_populates="slots")


class Column(
    db.Model, ModelMixin, EntityMixin, HiveMixin, ContributionMixin, MarkMixin, CreatedMixin, OwnedMixin, AnalyzedMixin,
    FoundedMixin, SharableMixin
):
    """
    Represents a column within a magazine, managing relationships with articles, reports,
    columnists, and tiering structures.

    The `Column` class provides comprehensive mappings and relationships between various
    entities such as magazines, articles, reports, slots, columnists, and related
    metadata. It also tracks the current state and historical changes, facilitating
    dynamic operations across the application.

    :ivar magazine_id: The unique identifier of the associated magazine.
    :type magazine_id: UUID
    :ivar current_article_id: The unique identifier of the current article linked to the column.
    :type current_article_id: UUID
    :ivar current_report_id: The unique identifier of the current report linked to the column.
    :type current_report_id: UUID
    :ivar magazine: The magazine entity this column belongs to, establishing a
        one-to-many relationship.
    :type magazine: Magazine
    :ivar current_article: The article currently associated with this column.
    :type current_article: Article
    :ivar current_report: The report currently associated with this column.
    :type current_report: Report
    :ivar slots: A list of slots related to this column, maintaining a one-to-many
        relationship.
    :type slots: List[Slot]
    :ivar columnists: A list of columnists contributing to this column.
    :type columnists: List[Columnist]
    :ivar maintainers: A list of portfolios managing this column.
    :type maintainers: List[Portfolio]
    :ivar previous_articles: A list of articles previously associated
        with this column.
    :type previous_articles: List[Article]
    :ivar previous_reports: A list of reports previously associated
        with this column.
    :type previous_reports: List[Report]
    :ivar next_articles: A list of articles planned to succeed the current article.
    :type next_articles: List[Article]
    :ivar next_reports: A list of reports planned to succeed the current report.
    :type next_reports: List[Report]
    :ivar editors: A list of editors responsible for editing this column.
    :type editors: List[Editor]
    :ivar frequency: Represents the recurrence frequency of events related to this column.
    :type frequency: EventRepeatEnum
    :ivar status: The current operational status of the column.
    :type status: ColumnStatusEnum
    """
    __tablename__ = "columns"
    __contribution_table__ = column_contributors
    __contribution_backref__ = "column_contributions"
    magazine_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("magazines.id"))
    current_article_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("articles.id"))
    current_report_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("reports.id"))
    thread_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("threads.id"))
    magazine: Mapped["Magazine"] = relationship("Magazine", back_populates="columns")
    current_article: Mapped["Article"] = relationship("Article", back_populates="current_columns")
    current_report: Mapped["Report"] = relationship("Report", back_populates="current_columns")
    thread: Mapped["Thread"] = relationship("Thread", back_populates="topic")
    slots: Mapped[List["Slot"]] = relationship("Slot", back_populates="column")
    columnists: Mapped[List["Columnist"]] = relationship("Columnist", back_populates="columns")
    maintainers: Mapped[List["Portfolio"]] = relationship("Portfolio", back_populates="maintained_columns")
    previous_articles: Mapped[List["Article"]] = relationship("Article", back_populates="previous_columns")
    previous_reports: Mapped[List["Report"]] = relationship("Report", back_populates="previous_columns")
    next_articles: Mapped[List["Article"]] = relationship("Article", back_populates="next_columns")
    next_reports: Mapped[List["Report"]] = relationship("Report", back_populates="next_columns")
    editors: Mapped[List["Editor"]] = relationship("Editor", back_populates="edited_columns")
    frequency: Mapped[EventRepeatEnum] = mapped_column(SQLAlchemyEnum(EventRepeatEnum), nullable=True)
    status: Mapped[ColumnStatusEnum] = mapped_column(SQLAlchemyEnum(ColumnStatusEnum), nullable=False)
    visibility: Mapped[VisibilityEnum] = mapped_column(SQLAlchemyEnum, default=VisibilityEnum.PUBLIC)


class Article(db.Model, ModelMixin, EntityMixin, ContentMixin, ContributionMixin, MarkMixin, SharableMixin, AuthoredMixin):
    """
    Represents an article entity with various relationships and attributes.

    This class defines an article within the context of a publishing system. It includes
    associations with magazines, authors, writers, editors, columns, and slots. The purpose
    of this class is to model an article as a central entity that interacts with other
    elements of the publishing ecosystem. It supports relationships for contributions,
    collaborative editing, and magazine associations.

    :ivar publishing_magazine_id: The unique identifier for the magazine in which the article
        is published.
    :type publishing_magazine_id: UUID
    :ivar publishing_magazine: The magazine instance associated with the article.
    :type publishing_magazine: Magazine
    :ivar authors: A list of portfolios associated with authorship of the article.
    :type authors: List[Portfolio]
    :ivar writers: A list of writers who contributed to the article.
    :type writers: List[Writer]
    :ivar editors: A list of editors who reviewed or edited the article.
    :type editors: List[Editor]
    :ivar current_columns: A list of columns where the article is currently featured.
    :type current_columns: List[Column]
    :ivar previous_columns: A list of columns where the article has been featured in the past.
    :type previous_columns: List[Column]
    :ivar next_columns: A list of columns where the article might be featured in the future.
    :type next_columns: List[Column]
    :ivar slots: A list of slots associated with the article.
    :type slots: List[Slot]
    """
    __tablename__ = "articles"
    __contribution_table__ = article_contributors
    __contribution_backref__ = "article_contributions"
    publishing_magazine_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("magazines.id"))
    publishing_magazine: Mapped["Magazine"] = relationship("Magazine", back_populates="articles")
    authors: Mapped[List["Portfolio"]] = relationship("Portfolio", back_populates="authored_articles")
    writers: Mapped[List["Writer"]] = relationship("Writer", back_populates="articles")
    editors: Mapped[List["Editor"]] = relationship("Editor", back_populates="edited_articles")
    current_columns: Mapped[List["Column"]] = relationship("Column", back_populates="current_article")
    previous_columns: Mapped[List["Column"]] = relationship("Column", back_populates="previous_articles")
    next_columns: Mapped[List["Column"]] = relationship("Column", back_populates="next_articles")
    slots: Mapped[List["Slot"]] = relationship("Slot", back_populates="article")


class Report(db.Model, ModelMixin, EntityMixin, ContentMixin, ContributionMixin, MarkMixin, SharableMixin, AuthoredMixin):
    """
    Represents a report entity within the system.

    This class models the core properties and relationships of a report object,
    used in conjunction with various mixins to provide extended functionality such
    as content handling, entity management, contribution tracking, and more. It can
    be associated with magazines, authors, analysts, editors, columns, and slots.
    The report entity is an integral part of the system, enabling collective
    collaboration and editorial processes.

    :ivar publishing_magazine_id: Unique identifier of the magazine in which this
        report is being published.
    :type publishing_magazine_id: UUID
    :ivar publishing_magazine: The magazine object this report is associated with.
    :type publishing_magazine: Magazine
    :ivar authors: List of portfolio objects representing the authors who
        contributed to this report.
    :type authors: List[Portfolio]
    :ivar analysts: List of analyst objects associated with this report.
    :type analysts: List[Analyst]
    :ivar editors: List of editor objects who have made editorial contributions
        to this report.
    :type editors: List[Editor]
    :ivar current_columns: List of column objects currently associated with this
        report.
    :type current_columns: List[Column]
    :ivar previous_columns: List of column objects formerly associated with this
        report.
    :type previous_columns: List[Column]
    :ivar next_columns: List of column objects scheduled to associate with this
        report in the future.
    :type next_columns: List[Column]
    :ivar slots: List of slot objects linked to this report for scheduling or
        organizational purposes.
    :type slots: List[Slot]
    """
    __tablename__ = "reports"
    __contribution_table__ = report_contributors
    __contribution_backref__ = "report_contributions"
    publishing_magazine_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("magazines.id"))
    publishing_magazine: Mapped["Magazine"] = relationship("Magazine", back_populates="reports")
    report_template_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("report_templates.id"))
    authors: Mapped[List["Portfolio"]] = relationship("Portfolio", back_populates="authored_reports")
    analysts: Mapped[List["Analyst"]] = relationship("Analyst", back_populates="reports")
    editors: Mapped[List["Editor"]] = relationship("Editor", back_populates="edited_reports")
    current_columns: Mapped[List["Column"]] = relationship("Column", back_populates="current_report")
    previous_columns: Mapped[List["Column"]] = relationship("Column", back_populates="previous_reports")
    next_columns: Mapped[List["Column"]] = relationship("Column", back_populates="next_reports")
    slots: Mapped[List["Slot"]] = relationship("Slot", back_populates="report")
    report_template: Mapped["ReportTemplate"] = relationship("ReportTemplate", back_populates="reports")


class Writer(db.Model, ModelMixin, CliqueMixin):
    """
    Represents a writer entity within the system.

    This class models a writer, providing relationships to associated articles
    and integrating functionalities from multiple mixins, combining various
    behaviors and properties. Each writer is associated with a collection of
    articles, reflecting their contributions or authored works. The class uses
    SQLAlchemy's ORM for database mapping and leverages specified mixins for
    additional functionalities.

    :ivar articles: List of articles associated with the writer.
    :type articles: List[Article]
    """
    __tablename__ = "writers"
    articles: Mapped[List["Article"]] = relationship("Article", back_populates="writers")


class Columnist(db.Model, ModelMixin, CliqueMixin, Writer):
    """
    Represents a columnist associated with multiple columns.

    This class is part of the database model and defines the relationship
    between columnists and columns. It inherits behaviors and functionalities
    from multiple mixins like ModelMixin, CliqueMixin,
    and Writer. The purpose of this class is to handle and manage data
    related to columnists within the application, particularly their association
    with various columns.

    :ivar columns: A list of columns associated with the columnist.
    :type columns: Mapped[List[Column]]
    """
    __tablename__ = "columnists"
    columns: Mapped[List["Column"]] = relationship("Column", back_populates="columnists")


class Analyst(db.Model, ModelMixin, CliqueMixin, Writer):
    """
    Represents an Analyst in the system, linking reports to various associated mixins.

    This class defines the properties and associations of an Analyst, which can be
    linked to multiple reports. Using various mixins, it extends the functionality
    to support database models, operations for associated cliques, creation metadata,
    and authoring capabilities. The Analyst serves as a central model for managing
    relationships to other entities such as reports.

    :ivar reports: A list of reports associated with the analyst.
    :type reports: Mapped[List[Report]]
    """
    __tablename__ = "analysts"
    reports: Mapped[List["Report"]] = relationship("Report", back_populates="analysts")


class Editor(db.Model, ModelMixin, CliqueMixin, Writer, Analyst):
    """
    Represents an editor in the system.

    This class defines an editor, which is associated with a specific magazine and has access
    to perform editorial tasks on various publishable items, including articles, reports, and
    columns. It incorporates several mixins that extend its functionality for managing roles,
    content creation, moderation, and analytics. The class also provides relationships to
    other entities it interacts with, enabling seamless data modeling within the system.

    :ivar magazine_id: The unique identifier of the magazine associated with this editor.
    :type magazine_id: UUID
    :ivar magazines_sections: A JSON-structured mapping representing the editor's sections
        within the magazine. Defaults to an empty dictionary.
    :type magazines_sections: Optional[dict]
    :ivar magazine: A relationship to the associated magazine, allowing access to the
        magazine details and related information.
    :type magazine: Magazine
    :ivar edited_articles: A collection of articles that the editor has edited, enabling
        tracking of content contributions.
    :type edited_articles: List[Article]
    :ivar edited_reports: A collection of reports that the editor has reviewed or edited as
        part of their responsibilities.
    :type edited_reports: List[Report]
    :ivar edited_columns: A collection of columns that the editor has worked on, indicating
        involvement in specific journalistic or editorial segments.
    :type edited_columns: List[Column]
    """
    __tablename__ = "editors"
    magazine_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("magazines.id"))
    magazines_sections: Mapped[Optional[dict]] = mapped_column(JSONB, default={})
    magazine: Mapped["Magazine"] = relationship("Magazine", back_populates="editors")
    edited_articles: Mapped[List["Article"]] = relationship("Article", back_populates="editors")
    edited_reports: Mapped[List["Report"]] = relationship("Report", back_populates="editors")
    edited_columns: Mapped[List["Column"]] = relationship("Column", back_populates="editors")


class ChiefEditor(db.Model, ModelMixin, Editor):
    """
    Represents the ChiefEditor model in the database.

    This class is a database model that defines the structure and behavior of
    a ChiefEditor entity. It inherits functionalities from various mixins
    and models, such as `db.Model`, `ModelMixin`, `Editor`, `CreatorMixin`,
    and `AuthorMixin`. ChiefEditor serves the purpose of linking to a magazine
    and providing additional functionalities.

    :ivar magazine: The Magazine entity associated with the Chief Editor.
                    Relationship is established with the "Magazine" model,
                    using the back_populates attribute to enable bidirectional
                    access.
    :type magazine: Mapped[Magazine]
    """
    __tablename__ = "chief_editors"
    magazine: Mapped["Magazine"] = relationship("Magazine", back_populates="chief_editor")


class ExecutiveEditor(db.Model, ModelMixin, CliqueMixin, Writer, Analyst, ChiefEditor):
    """
    Represents an Executive Editor entity in the database.

    This class is used to manage executive editors who oversee and manage journals, their
    related sections, and various editorial processes. It establishes relationships with
    journals, including defining attributes for maintaining journal data and relationships
    to other models.

    :ivar journal_id: The unique identifier of the journal associated with this executive
        editor.
    :type journal_id: UUID
    :ivar journal_sections: A dictionary containing sections of the journal overseen by
        the executive editor. Defaults to an empty dictionary.
    :type journal_sections: dict
    :ivar journal: Relationship to the Journal instance associated with the executive editor.
    :type journal: Journal
    """
    __tablename__ = "executive_editors"
    journal_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("journals.id"))
    journal_sections: Mapped[dict] = mapped_column(JSONB, default={})
    journal: Mapped["Journal"] = relationship("Journal", back_populates="executive_editors")


class ChiefAnalyst(db.Model, ModelMixin, CliqueMixin, Analyst, Editor):
    """
    Represents the Chief Analyst entity.

    This class models a Chief Analyst in the application, providing
    a link between the Chief Analyst and a specific journal. It includes
    associations and relationships with other data models and inherits
    multiple mixins to implement additional functionalities related to
    database operations, analytics, and editing.

    :ivar journal_id: The unique identifier of the associated journal.
    :type journal_id: UUID
    :ivar journal: The Journal object associated with the Chief Analyst.
    :type journal: Journal
    """
    __tablename__ = "chief_analysts"
    journal_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("journals.id"))
    journal: Mapped["Journal"] = relationship("Journal", back_populates="chief_analysts")


class Correspondent(db.Model, ModelMixin, CliqueMixin, Writer):
    """
    Represents a Correspondent entity in the database.

    This class is used to define the structure and relationships of the correspondent
    table in the database. It includes attributes and relationships that define the
    correspondent's association with magazines and other related entities.

    :ivar __tablename__: Name of the database table associated with this class.
    :type __tablename__: str
    :ivar magazine_id: Foreign key associating the correspondent with a specific magazine.
    :type magazine_id: UUID
    :ivar magazine: Relationship mapping this correspondent to a magazine object.
    :type magazine: Magazine
    """
    __tablename__ = "correspondents"
    magazine_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("magazines.id"))
    magazine: Mapped["Magazine"] = relationship("Magazine", back_populates="correspondents")


class ChiefCorrespondent(db.Model, ModelMixin, CliqueMixin, Correspondent, Editor):
    """
    Represents a Chief Correspondent in the system.

    The ChiefCorrespondent class ties together functionality from multiple
    mixins including `ModelMixin`, `CliqueMixin`, `CreatorMixin`, `AuthorMixin`,
    and inherits behaviors as a `Correspondent` and `Editor`. It is specifically
    associated with a journal entity in the database.

    :ivar __tablename__: The database table associated with this class.
    :type __tablename__: str
    :ivar journal_id: The unique identifier for the journal with which the
        Chief Correspondent is associated.
    :type journal_id: UUID
    :ivar journal: The journal entity associated with the Chief Correspondent.
    :type journal: Journal
    """
    __tablename__ = "chief_correspondents"
    journal_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("journals.id"))
    journal: Mapped["Journal"] = relationship("Journal", back_populates="chief_correspondents")


class EditorInChief(db.Model, ModelMixin, Editor, ExecutiveEditor, ChiefCorrespondent, ChiefAnalyst):
    """
    Represents the Editor-in-Chief role in the system.

    The Editor-in-Chief class models an Editor-in-Chief responsible for overseeing
    the operations of a journal. This class consolidates multiple mixins and
    inheritance from related classes such as Editor,
    ExecutiveEditor, ChiefCorrespondent, and ChiefAnalyst to provide a comprehensive
    representation of an Editor-in-Chief. It also defines the relationship between
    the Editor-in-Chief and the journal they manage.

    :ivar journal: The journal entity associated with the Editor-in-Chief. This
        illustrates a bidirectional relationship between the journal and the
        Editor-in-Chief.
    :type journal: Mapped[Journal]
    """
    __tablename__ = "editor_in_chief"
    journal: Mapped["Journal"] = relationship("Journal", back_populates="editor_in_chief")
