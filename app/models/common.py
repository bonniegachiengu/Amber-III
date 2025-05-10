import uuid
from uuid import uuid4
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, Boolean, ForeignKey, JSON, Date, Integer, Float, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, relationships
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum as SQLAlchemyEnum

from ..extensions import db
from .utils.config import ContentTypeEnum
from .mixins import ModelMixin, MediaMixin, ThumbnailMixin, ContentMixin, ContributionMixin
from .associations import (
    dashboard_template_contributors, wiki_template_contributors, tag_contributors, language_contributors,
    country_contributors, nationality_contributors, era_contributors, genre_contributors, theme_contributors,
    keyword_contributors, report_template_contributors, verification_contributors
)


if TYPE_CHECKING:
    from .scrolls import Scroll
    from .user import User
    from .journal import Magazine, Article
    from .player import Bookmark, WatchHistory
    from .community import Reaction, Fandom
    from .commerce import Fund, Transaction
    from .library import Library



class DashboardTemplate(db.Model, ModelMixin, ContributionMixin):
    __tablename__ = "dashboard_templates"
    __contribution_table__ = dashboard_template_contributors
    __contribution_backref__ = "dashboard_template_contributions"


class Overview(db.Model, ModelMixin):
    pass


class Widget(db.Model, ModelMixin):
    pass


class WikiTemplate(db.Model, ModelMixin, ContributionMixin):
    __tablename__ = "wiki_templates"
    __contribution_table__ = wiki_template_contributors
    __contribution_backref__ = "wiki_template_contributions"


class WikiSection(db.Model, ModelMixin):
    pass


class Anchor(db.Model, ModelMixin):
    __tablename__ = "anchors"
    marked: Mapped[List["ContentMixin"]] = relationship("ContentMixin", back_populates="anchors")
    anchors_type: Mapped[ContentTypeEnum] = mapped_column(SQLAlchemyEnum(ContentTypeEnum), nullable=False)
    anchor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    anchored_content: Mapped["ContentMixin"] = relationship("ContentMixin", foreign_keys=[anchor_id], back_populates="anchored") # TODO: Enforce the use of anchored in Films, watchlists, people etc.



class Link(db.Model, ModelMixin):
    pass


class Image(db.Model, ModelMixin, MediaMixin):
    pass


class Video(db.Model, ModelMixin, MediaMixin):
    pass


class Tag(db.Model, ModelMixin, ContributionMixin):
    __tablename__ = "tags"
    __contribution_table__ = tag_contributors
    __contribution_backref__ = "tag_contributions"


class Language(db.Model, ModelMixin, ContributionMixin):
    __tablename__ = "languages"
    __contribution_table__ = language_contributors
    __contribution_backref__ = "language_contributions"


class Country(db.Model, ModelMixin, ContributionMixin):
    __tablename__ = "countries"
    __contribution_table__ = country_contributors
    __contribution_backref__ = "country_contributions"


class Nationality(db.Model, ModelMixin, ContributionMixin):
    __tablename__ = "nationalities"
    __contribution_table__ = nationality_contributors
    __contribution_backref__ = "nationality_contributions"


class Era(db.Model, ModelMixin, ContributionMixin):
    __tablename__ = "eras"
    __contribution_table__ = era_contributors
    __contribution_backref__ = "era_contributions"


class Genre(db.Model, ModelMixin, ContributionMixin):
    __tablename__ = "genres"
    __contribution_table__ = genre_contributors
    __contribution_backref__ = "genre_contributions"


class Theme(db.Model, ModelMixin, ContributionMixin):
    __tablename__ = "themes"
    __contribution_table__ = theme_contributors
    __contribution_backref__ = "theme_contributions"


class Keyword(db.Model, ModelMixin, ContributionMixin):
    __tablename__ = "keywords"
    __contribution_table__ = keyword_contributors
    __contribution_backref__ = "keyword_contributions"


class Map(db.Model, ModelMixin):
    pass


class Location(db.Model, ModelMixin):
    users: Mapped[List["User"]] = relationship("User", secondary="user_locations")


class Venue(db.Model, ModelMixin):
    pass


class Directory(db.Model, ModelMixin):
    pass


class Feature(db.Model, ModelMixin):
    pass


class Figure(db.Model, ModelMixin, ContentMixin):
    pass


class BarGraph(db.Model, ModelMixin, ContentMixin):
    pass


class LineGraph(db.Model, ModelMixin, ContentMixin):
    pass


class PieChart(db.Model, ModelMixin, ContentMixin):
    pass


class Axis(db.Model, ModelMixin, ContentMixin):
    pass


class Legend(db.Model, ModelMixin, ContentMixin):
    pass


class DataSet(db.Model, ModelMixin, ContentMixin):
    pass


class Preferences(db.Model, ModelMixin):
    pass


class Field(db.Model, ModelMixin):
    pass


class Confidence(db.Model, ModelMixin):
    pass


class Weight(db.Model, ModelMixin):
    pass


class ConfidenceScore(db.Model, ModelMixin):
    pass


class Avatar(db.Model, ModelMixin, MediaMixin):
    pass


class CTA(db.Model, ModelMixin):
    pass


class Filters(db.Model, ModelMixin):
    pass


class Search(db.Model, ModelMixin):
    pass


class Explorer(db.Model, ModelMixin):
    pass


class SortBy(db.Model, ModelMixin):
    pass


class SearchResult(db.Model, ModelMixin):
    pass


class ClipThumbnail(db.Model, ModelMixin, ThumbnailMixin, ContentMixin):
    pass


class ColumnThumbnail(db.Model, ModelMixin, ThumbnailMixin, ContentMixin):
    pass


class ArticleThumbnail(db.Model, ModelMixin, ThumbnailMixin, ContentMixin):
    pass


class PostThumbnail(db.Model, ModelMixin, ThumbnailMixin, ContentMixin):
    pass


class ReportThumbnail(db.Model, ModelMixin, ThumbnailMixin, ContentMixin):
    pass


class ReportTemplate(db.Model, ModelMixin, ContentMixin, ContributionMixin):
    __tablename__ = "report_templates"
    __contribution_table__ = report_template_contributors
    __contribution_backref__ = "report_template_contributions"


class Notification(db.Model, ModelMixin):
    pass


class Local(db.Model, ModelMixin):
    pass


class Verification(db.Model, ModelMixin, ContributionMixin):
    __tablename__ = "verifications"
    __contribution_table__ = verification_contributors
    __contribution_backref__ = "verification_contributions"
