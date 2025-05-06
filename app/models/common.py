import enum
from uuid import uuid4
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, Boolean, ForeignKey, JSON, Date, Integer, Float, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, relationships
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum as SQLAlchemyEnum

from . import ContentMixin
from ..extensions import db
from .mixins import (
    EntityMixin, HiveMixin, CliqueMixin, ModeratorMixin, CreatorMixin, OwnerMixin, AuthorMixin, ContributionMixin,
    ContributorMixin, ModelMixin, MarkMixin, MediaMixin, ThumbnailMixin
)


if TYPE_CHECKING:
    from .scrolls import Scroll
    from .user import User
    from .journal import Magazine, Article
    from .player import Bookmark, WatchHistory
    from .community import Reaction, Fandom
    from .commerce import Fund, Transaction, Exchange
    from .library import Library


def generate_uuid():
    return str(uuid4())


class Visibility(enum.Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    FOLLOWERS = "followers"
    HIVE = "hive"
    CLIQUE = "clique"


class DashboardTemplate(db.Model, ModelMixin, ContributionMixin):
    pass


class Overview(db.Model, ModelMixin, ContributionMixin):
    pass


class Widget(db.Model, ModelMixin, ContributionMixin):
    pass


class WikiTemplate(db.Model, ModelMixin, ContributionMixin):
    pass


class WikiSection(db.Model, ModelMixin, ContributionMixin):
    pass


class Anchor(db.Model, ModelMixin, ContributionMixin):
    pass


class Link(db.Model, ModelMixin, ContributionMixin):
    pass


class Image(db.Model, ModelMixin, ContributionMixin, MediaMixin):
    pass


class Video(db.Model, ModelMixin, ContributionMixin, MediaMixin):
    pass


class SubtitleFile(db.Model, ModelMixin, ContributionMixin, MediaMixin):
    pass


class Tag(db.Model, ModelMixin, ContributionMixin, MarkMixin):
    pass


class Language(db.Model, ModelMixin, ContributionMixin):
    pass


class Country(db.Model, ModelMixin, ContributionMixin):
    pass


class Nationality(db.Model, ModelMixin, ContributionMixin):
    pass


class Period(db.Model, ModelMixin, ContributionMixin):
    pass


class Genre(db.Model, ModelMixin, ContributionMixin):
    pass


class Theme(db.Model, ModelMixin, ContributionMixin):
    pass


class Keyword(db.Model, ModelMixin, ContributionMixin):
    pass


class Map(db.Model, ModelMixin, ContributionMixin):
    pass


class Location(db.Model, ModelMixin, ContributionMixin):
    pass


class Venue(db.Model, ModelMixin, ContributionMixin):
    pass


class Directory(db.Model, ModelMixin, ContributionMixin):
    pass


class Feature(db.Model, ModelMixin, ContributionMixin):
    pass


class Figure(db.Model, ModelMixin, ContributionMixin, ContentMixin):
    pass


class BarGraph(db.Model, ModelMixin, ContributionMixin, ContentMixin):
    pass


class LineGraph(db.Model, ModelMixin, ContributionMixin, ContentMixin):
    pass


class PieChart(db.Model, ModelMixin, ContributionMixin, ContentMixin):
    pass


class Axis(db.Model, ModelMixin, ContributionMixin, ContentMixin):
    pass


class Legend(db.Model, ModelMixin, ContributionMixin, ContentMixin):
    pass


class DataSet(db.Model, ModelMixin, ContributionMixin, ContentMixin):
    pass


class Preferences(db.Model, ModelMixin, ContributionMixin):
    pass


class Field(db.Model, ModelMixin, ContributionMixin):
    pass


class Confidence(db.Model, ModelMixin, ContributionMixin):
    pass


class Weight(db.Model, ModelMixin, ContributionMixin):
    pass


class ConfidenceScore(db.Model, ModelMixin, ContributionMixin):
    pass


class Avatar(db.Model, ModelMixin, ContributionMixin, MediaMixin):
    pass


class Exclusivity(db.Model, ModelMixin, ContributionMixin):
    pass


class CTA(db.Model, ModelMixin, ContributionMixin):
    pass


class Filters(db.Model, ModelMixin, ContributionMixin):
    pass


class Search(db.Model, ModelMixin, ContributionMixin):
    pass


class Explorer(db.Model, ModelMixin, ContributionMixin):
    pass


class SortBy(db.Model, ModelMixin, ContributionMixin):
    pass


class SearchResult(db.Model, ModelMixin, ContributionMixin):
    pass


class ClipThumbnail(db.Model, ModelMixin, ContributionMixin, ThumbnailMixin, ContentMixin):
    pass


class ColumnThumbnail(db.Model, ModelMixin, ContributionMixin, ThumbnailMixin, ContentMixin):
    pass


class ArticleThumbnail(db.Model, ModelMixin, ContributionMixin, ThumbnailMixin, ContentMixin):
    pass


class PostThumbnail(db.Model, ModelMixin, ContributionMixin, ThumbnailMixin, ContentMixin):
    pass


class ReportThumbnail(db.Model, ModelMixin, ContributionMixin, ThumbnailMixin, ContentMixin):
    pass


class ReportTemplate(db.Model, ModelMixin, ContributionMixin, ContentMixin):
    pass


class Notification(db.Model, ModelMixin, ContributionMixin):
    pass


class Local(db.Model, ModelMixin, ContributionMixin):
    pass
