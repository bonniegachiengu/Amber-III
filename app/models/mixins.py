import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSONB, Integer, Float, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.schema import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr, backref
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from utils.config import ContentTypeEnum, CliqueTypeEnum, VisibilityEnum, ArticleReportStatusEnum, HiveTypeEnum

if TYPE_CHECKING:
    from .user import User
    from .scrolls import Scroll
    from .library import Library, Film, Album, Hitlist
    from .journal import Magazine, Article
    from .player import WatchHistory
    from .community import Message, Thread, Reaction, Tier, Posts, Updates, Issues, Pins, Clips
    from .commerce import Fund, Transaction, Ledger, Currency, AmberToken
    from .common import WikiTemplate, DashboardTemplate, Tag, Keyword, Language, Country, Nationality, Period, Anchor
    from .calendar import Event, Calendar, Ticket

def generate_uuid():
    return str(uuid.uuid4())

class ModelMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), default=None, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    deleted_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), default=None)
    wiki: Mapped[Optional["WikiTemplate"]] = relationship(back_populates="user", uselist=False)
    dashboard: Mapped[Optional["DashboardTemplate"]] = relationship(back_populates="user", uselist=False)
    fields: Mapped[Optional[dict]] = mapped_column(JSONB)


class EntityMixin:
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    icon: Mapped[Optional[str]] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    settings: Mapped[Optional[dict]] = mapped_column(JSONB, default={})
    calendar_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("calendars.id"), default=None, nullable=False)
    calendar: Mapped["Calendar"] = relationship(back_populates="entities", uselist=False)


class ContributionMixin:
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


class EraMixin:
    start_time: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)


class LibraryMixin:
    library_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), default=None, nullable=False)
    library: Mapped["Library"] = relationship(back_populates="owner", uselist=False)


class ListMixin:
    scroll_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scrolls.id"), default=None, nullable=False)
    scroll: Mapped["Scroll"] = relationship(back_populates="lists", uselist=False)


class MarkMixin:
    tags: Mapped[Optional[list["Tag"]]] = relationship("Tag", back_populates="marked")
    keywords: Mapped[Optional[list["Keyword"]]] = relationship("Keyword", back_populates="marked")
    languages: Mapped[Optional[list["Language"]]] = relationship("Language", back_populates="marked")
    countries: Mapped[Optional[list["Country"]]] = relationship("Country", back_populates="marked")
    nationalities: Mapped[Optional[list["Nationality"]]] = relationship("Nationality", back_populates="marked")
    periods: Mapped[Optional[list["Period"]]] = relationship("Period", back_populates="marked")
    anchors: Mapped[Optional[list["Anchor"]]] = relationship("Anchor", back_populates="marked")


class CliqueMixin:
    agents: List["User"] = relationship("User", back_populates="cliques")
    clique_type: Mapped[CliqueTypeEnum] = mapped_column(SQLAlchemyEnum(CliqueTypeEnum), nullable=False)


class HiveMixin(LibraryMixin):
    boards: Mapped[List["BoardMixin"]] = relationship("BoardMixin", back_populates="hive")
    walls: Mapped[List["WallMixin"]] = relationship("WallMixin", back_populates="hive")
    join_rules: Mapped[Optional[dict]] = mapped_column(JSONB, default={})


class ContentMixin:
    content_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    content_type: Mapped[ContentTypeEnum] = mapped_column(SQLAlchemyEnum(ContentTypeEnum), nullable=False)


class SharableMixin:
    views: Mapped[int] = mapped_column(Integer, default=0)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    shares: Mapped[int] = mapped_column(Integer, default=0)
    comments: Mapped[int] = mapped_column(Integer, default=0)


class AuthoredMixin:
    publish_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    status: Mapped[ArticleReportStatusEnum] = mapped_column(SQLAlchemyEnum, default=ArticleReportStatusEnum.UNPUBLISHED)
    visibility: Mapped[VisibilityEnum] = mapped_column(SQLAlchemyEnum, default=VisibilityEnum.PUBLIC)
    content: Mapped[str] = mapped_column(Text, nullable=False, info={"rich_text": "ckeditor"})
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    revision_history: Mapped[list[dict]] = mapped_column(JSONB, default=[])
    thread: Mapped["Thread"] = relationship("Thread", back_populates="topic")
    thread_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("threads.id"))


class PerksMixin:
    tiers: Mapped[List["Tier"]] = relationship("Tier", back_populates="perks")


class WatchListMixin(ListMixin):
    pass


class CreatorMixin:
    pass


class AuthorMixin:
    pass


class OwnerMixin:
    pass

class ModeratorMixin:
    pass

class BoardMixin:
    hive_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    hive: Mapped["HiveMixin"] = relationship(HiveMixin, foreign_keys=[hive_id], back_populates="boards")
    hive_type: Mapped[HiveTypeEnum] = mapped_column(SQLAlchemyEnum(HiveTypeEnum), nullable=False)

class WallMixin:
    hive_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    hive: Mapped["HiveMixin"] = relationship(HiveMixin, foreign_keys=[hive_id], back_populates="walls")
    hive_type: Mapped[HiveTypeEnum] = mapped_column(SQLAlchemyEnum(HiveTypeEnum), nullable=False)

class ActionMixin:
    pass

class PartnerMixin:
    pass

class MediaMixin:
    pass

class ThumbnailMixin:
    pass

class AwardTypeMixin:
    pass

class AwardMixin:
    pass
