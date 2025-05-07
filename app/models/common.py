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
    EntityMixin, HiveMixin, CliqueMixin, ModeratorMixin, CreatorMixin, OwnerMixin, AuthorMixin,
    ModelMixin, MarkMixin, MediaMixin, ThumbnailMixin
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


class DashboardTemplate(db.Model, ModelMixin):
    pass


class Overview(db.Model, ModelMixin):
    pass


class Widget(db.Model, ModelMixin):
    pass


class WikiTemplate(db.Model, ModelMixin):
    pass


class WikiSection(db.Model, ModelMixin):
    pass


class Anchor(db.Model, ModelMixin):
    pass


class Link(db.Model, ModelMixin):
    pass


class Image(db.Model, ModelMixin, MediaMixin):
    pass


class Video(db.Model, ModelMixin, MediaMixin):
    pass


class SubtitleFile(db.Model, ModelMixin, MediaMixin):
    pass


class Tag(db.Model, ModelMixin, MarkMixin):
    pass


class Language(db.Model, ModelMixin):
    pass


class Country(db.Model, ModelMixin):
    pass


class Nationality(db.Model, ModelMixin):
    pass


class Period(db.Model, ModelMixin):
    pass


class Genre(db.Model, ModelMixin):
    pass


class Theme(db.Model, ModelMixin):
    pass


class Keyword(db.Model, ModelMixin):
    pass


class Map(db.Model, ModelMixin):
    pass


class Location(db.Model, ModelMixin):
    pass


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


class Exclusivity(db.Model, ModelMixin):
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


class ReportTemplate(db.Model, ModelMixin, ContentMixin):
    pass


class Notification(db.Model, ModelMixin):
    pass


class Local(db.Model, ModelMixin):
    pass


class Verification(db.Model, ModelMixin):
    pass
