import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, relationships
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from .mixins import (
    EntityMixin, HiveMixin, CliqueMixin, ModeratorMixin, CreatorMixin, OwnerMixin, AuthorMixin,
    ModelMixin, LibraryMixin
)


if TYPE_CHECKING:
    from .scrolls import Scroll
    from .library import Library, Shop, Assets, Merchandise
    from .journal import Magazine, Article
    from .player import WatchHistory
    from .community import Message, Thread, Reaction
    from .commerce import Fund, Transaction, Exchange
    from .common import WikiTemplate, DashboardTemplate
    from .calendar import Event, Calendar


class User(db.Model, ModelMixin, UserMixin, EntityMixin, LibraryMixin):

    __tablename__ = "users"
    # Core Fields
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(default=datetime.now)
    last_seen: Mapped[Optional[datetime]] = mapped_column(default=None)
    # Profile & Social Fields
    bio: Mapped[Optional[str]] = mapped_column(String(500))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255))
    location: Mapped[Optional[str]] = mapped_column(String(100))
    portfolio_visibility: Mapped[str] = mapped_column(String(10), default="public")  # 'public' or 'private'
    # Preferences & Personalization Fields
    preferred_tags: Mapped[Optional[list]] = mapped_column(JSON)
    language: Mapped[str] = mapped_column(String(10), default="en")
    streaming_accounts: Mapped[Optional[dict]] = mapped_column(JSON)
    playback_settings: Mapped[Optional[dict]] = mapped_column(JSON)
    # System Fields
    role: Mapped[str] = mapped_column(String(20), default="user")
    notifications_enabled: Mapped[bool] = mapped_column(default=True)
    api_key: Mapped[Optional[str]] = mapped_column(String(64), unique=True)
    # Relationships # TODO: Review these relationships
    # --- Encompassing Singular Models ---
    # --- Content Creation ---


    # --- Activity Tracking ---
    watch_history: Mapped[List["WatchHistory"]] = relationship(back_populates="user")
    # --- Social Features ---
    followers: Mapped[List["UserFollow"]] = relationship(
        "UserFollow",
        foreign_keys="[UserFollow.followed_id]",
        back_populates="followed",
        cascade="all, delete-orphan"
    )
    following: Mapped[List["UserFollow"]] = relationship(
        "UserFollow",
        foreign_keys="[UserFollow.follower_id]",
        back_populates="follower",
        cascade="all, delete-orphan"
    )
    # joined_hives: Mapped[List["Hive"]] = relationship(back_populates="members")
    # cliques: Mapped[List["Clique"]] = relationship(back_populates="user")
    threads: Mapped[List["Thread"]] = relationship(back_populates="participants")

    # --- Marketplace ---
    fund: Mapped[Optional["Fund"]] = relationship(back_populates="user", uselist=False)
    shop: Mapped[Optional["Shop"]] = relationship(back_populates="owner", uselist=False)
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="user")
    exchanges: Mapped[List["Exchange"]] = relationship(back_populates="user")
    assets: Mapped[List["Assets"]] = relationship(back_populates="owner")
    purchased_merchandise: Mapped[List["Merchandise"]] = relationship(back_populates="buyers")

    # --- Amber Currency ---
    ambertokens: Mapped[int] = mapped_column(default=0)

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "location": self.location,
            "portfolio_visibility": self.portfolio_visibility,
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "followers_count": len(self.followers),
            "following_count": len(self.following),
            "role": self.role,
            "notifications_enabled": self.notifications_enabled,
            "preferred_tags": self.preferred_tags,
        }


class UserFollow(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a relationship where a user can follow another user within the system.

    The UserFollow class models the many-to-many relationship between users, where one
    user can follow another. It tracks the follower, the user being followed, and the
    timestamp of when the follow action occurred. This class is linked to the user's table
    to establish relationships between users.

    :ivar id: Unique identifier of the user follow relationship.
    :type id: int
    :ivar follower_id: The UUID of the user who is following.
    :type follower_id: uuid.UUID
    :ivar followed_id: The UUID of the user being followed.
    :type followed_id: uuid.UUID
    :ivar created_at: The datetime when the 'follow' relationship was created.
    :type created_at: datetime
    :ivar follower: The User instance representing the follower of the relationship.
    :type follower: User
    :ivar followed: The User instance representing the 'followed' user in the relationship.
    :type followed: User
    """
    __tablename__ = "user_follows"

    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    followed_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    # Relationships
    follower: Mapped["User"] = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed: Mapped["User"] = relationship("User", foreign_keys=[followed_id], back_populates="followers")
