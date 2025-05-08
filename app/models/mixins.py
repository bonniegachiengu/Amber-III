import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.schema import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr, relationships
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from utils.config import ContentType

if TYPE_CHECKING:
    from .user import User
    from .scrolls import Scroll
    from .library import Library, Film, Album, Hitlist
    from .journal import Magazine, Article
    from .player import WatchHistory
    from .community import Message, Thread, Reaction
    from .commerce import Fund, Transaction, Ledger, Currency
    from .common import WikiTemplate, DashboardTemplate, Tag, Keyword, Language, Country, Nationality, Period, Anchor
    from .calendar import Event, Calendar, Ticket


class ModelMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), default=None, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    deleted_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), default=None)
    wiki: Mapped[Optional["WikiTemplate"]] = relationship(back_populates="user", uselist=False)
    dashboard: Mapped[Optional["DashboardTemplate"]] = relationship(back_populates="user", uselist=False)
    fields: Mapped[Optional[dict]] = mapped_column(JSON)


class EntityMixin:
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    icon: Mapped[Optional[str]] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    settings: Mapped[Optional[dict]] = mapped_column(JSON)
    calendar_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("calendars.id"), default=None, nullable=False)
    calendar: Mapped["Calendar"] = relationship(back_populates="entities", uselist=False)


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


class HiveMixin(LibraryMixin):
    pass


class ContentMixin:
    content_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    content_type: Mapped[ContentType] = mapped_column(SQLAlchemyEnum(ContentType), nullable=False)


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

class PerksMixin:
    pass

class BoardMixin:
    pass

class EntryMixin:
    pass

class PostMixin:
    pass

class WallMixin:
    pass

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
