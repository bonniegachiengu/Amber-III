import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, relationships
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db

if TYPE_CHECKING:
    from .scrolls import Scroll
    from .library import Library
    from .journal import Magazine, Article
    from .player import WatchHistory
    from .community import Message, Thread, Reaction
    from .commerce import Fund, Transaction, Exchange
    from .common import WikiTemplate, DashboardTemplate, Exclusivity
    from .calendar import Event, Calendar


class ModelMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    deleted_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"), default=None)

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
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(default=None)


class CreatorMixin:
    pass


class AuthorMixin:
    pass


class OwnerMixin:
    pass


class ContributorMixin:
    pass


class ContributionMixin:
    pass

class TokenMixin:
    pass

class HiveMixin:
    pass

class CliqueMixin:
    pass

class ModeratorMixin:
    pass

class PerksMixin:
    pass

class ContentMixin:
    # exclusivity:
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

class WatchListMixin:
    pass

class AwardTypeMixin:
    pass

class AwardMixin:
    pass
