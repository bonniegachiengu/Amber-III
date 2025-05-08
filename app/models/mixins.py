import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr, relationships
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db

if TYPE_CHECKING:
    from .scrolls import Scroll
    from .library import Library
    from .journal import Magazine, Article
    from .player import WatchHistory
    from .community import Message, Thread, Reaction
    from .commerce import Fund, Transaction, Ledger, Currency
    from .common import WikiTemplate, DashboardTemplate, Exclusivity
    from .calendar import Event, Calendar


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

    def to_dict(self):
        return {
            "id": str(self.id),
        }


class EntityMixin:
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    icon: Mapped[Optional[str]] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    settings: Mapped[Optional[dict]] = mapped_column(JSON)
    calendar: Mapped["Calendar"] = relationship(back_populates="owner", uselist=False)

class EraMixin:
    start_time: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)

class LibraryMixin:
    library_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), default=None, nullable=False)
    library: Mapped["Library"] = relationship(back_populates="owner", uselist=False)

class ListMixin:
    scroll_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scrolls.id"), default=None, nullable=False)
    scroll: Mapped["Scroll"] = relationship(back_populates="lists", uselist=False)

class CreatorMixin:
    pass


class AuthorMixin:
    pass


class OwnerMixin:
    pass

class HiveMixin(LibraryMixin):
    pass

class CliqueMixin:
    pass

class ModeratorMixin:
    pass

class PerksMixin:
    pass

class ContentMixin:
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

class RecommendationMixin:
    pass

class ExhibitionMixin:
    pass

class PartnerMixin:
    pass

class MediaMixin:
    pass

class ThumbnailMixin:
    pass

class MarkMixin:
    pass

class WatchListMixin(ListMixin):
    pass

class AwardTypeMixin:
    pass

class AwardMixin:
    pass
