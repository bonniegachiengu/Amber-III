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
    from .library import Watchlist, Collection
    from .journal import Magazine, Article
    from .player import Bookmark, WatchHistory
    from .community import Hive, Clique, Comment, Reaction
    from .commerce import Fund, Shop, Transaction, Asset, Exchange, Merchandise
    from .common import Contribution


class User(db.Model, UserMixin):
    """
    Represents a user within the application.

    This class models users and their associated attributes, preferences, system fields,
    and relationships with other entities within the application.

    :ivar id: A unique identifier for the user.
    :ivar username: The unique username for the user.
    :ivar email: The unique email address associated with the user.
    :ivar password_hash: The hashed password for the user's account.
    :ivar is_verified: Indicates whether the user's email has been verified.
    :ivar is_active: Indicates whether the user's account is active.
    :ivar joined_at: The date and time the user joined the platform.
    :ivar last_seen: The last recorded date and time the user was seen online.

    :ivar bio: A short biography or description provided by the user.
    :ivar avatar_url: A URL to the user's profile avatar image.
    :ivar location: The user's geographical location.
    :ivar portfolio_visibility: The visibility of the user's portfolio, either "public" or "private".

    :ivar preferred_tags: A list of tags representing the user's preferred interests or topics.
    :ivar language: The user's preferred language for interactions.
    :ivar streaming_accounts: A dictionary of the user's linked streaming accounts.
    :ivar playback_settings: A dictionary containing the user's playback preferences.
    :ivar calendar: A dictionary representing the user's calendar data.

    :ivar created_at: The date and time when the user's account was created.
    :ivar updated_at: The date and time of the user's most recent account update.
    :ivar deleted_at: The date and time, if applicable, when the user's account was deleted.
    :ivar deleted_by: The ID of the user who deleted this account, if applicable.
    :ivar role: The user's role within the application (e.g., "user", "admin").
    :ivar settings: A dictionary of additional user-specific settings.
    :ivar notifications_enabled: Indicates whether the user has enabled notifications.
    :ivar api_key: A unique API key associated with the user.

    :ivar watchlists: A list of watchlists owned by the user.
    :ivar library: A list of collections owned by the user.
    :ivar magazines: A list of magazines created by the user.
    :ivar articles: A list of articles authored by the user.
    :ivar scrolls: A list of scrolls associated with the user.
    :ivar bookmarks: A list of bookmarks created by the user.
    :ivar watch_history: A list of watch history records associated with the user.
    :ivar contributions: A list of contributions made by the user.

    :ivar followers: A list of users who follow this user.
    :ivar following: A list of users whom this user is following.
    :ivar joined_hives: A list of hives the user has joined.
    :ivar cliques: A list of cliques associated with the user.
    :ivar comments: A list of comments made by the user.
    :ivar reactions: A list of reactions made by the user.
    :ivar cloned_hitlists: A list of hitlists cloned by the user.

    :ivar ambertokens: The number of AmberTokens associated with the user's account.

    :ivar fund: A Fund object including details about the user's fund, if any.
    :ivar shop: A Shop object representing the user's shop, if any.
    :ivar transactions: A list of transactions made by the user.
    :ivar exchanges: A list of exchanges involving the user.
    :ivar assets: A list of assets owned by the user.
    :ivar purchased_merchandise: A list of merchandise purchased by the user.
    """
    __tablename__ = "users"

    # Core Fields
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
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
    calendar: Mapped[Optional[dict]] = mapped_column(JSON)

    # System Fields
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    deleted_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"), default=None)
    role: Mapped[str] = mapped_column(String(20), default="user")
    settings: Mapped[Optional[dict]] = mapped_column(JSON)
    notifications_enabled: Mapped[bool] = mapped_column(default=True)
    api_key: Mapped[Optional[str]] = mapped_column(String(64), unique=True)

    # Content Relationships
    watchlists: Mapped[List["Watchlist"]] = relationship(back_populates="owner")
    library: Mapped[List["Collection"]] = relationship(back_populates="owner")
    magazines: Mapped[List["Magazine"]] = relationship(back_populates="creator")
    articles: Mapped[List["Article"]] = relationship(back_populates="author")
    scrolls: Mapped[List["Scroll"]] = relationship(back_populates="user")
    bookmarks: Mapped[List["Bookmark"]] = relationship(back_populates="user")
    watch_history: Mapped[List["WatchHistory"]] = relationship(back_populates="user")
    contributions: Mapped[List["Contribution"]] = relationship(back_populates="user")

    # Social
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
    joined_hives: Mapped[List["Hive"]] = relationship(secondary="hive_memberships", back_populates="members")
    cliques: Mapped[List["Clique"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")
    reactions: Mapped[List["Reaction"]] = relationship(back_populates="user")
    cloned_hitlists: Mapped[List["Watchlist"]] = relationship(
        back_populates="cloned_by", foreign_keys="[Watchlist.cloned_by_id]"
    )

    # AmberTokens
    ambertokens: Mapped[int] = mapped_column(default=0)

    # Marketplace Relationships
    fund: Mapped[Optional["Fund"]] = relationship(back_populates="user", uselist=False)
    shop: Mapped[Optional["Shop"]] = relationship(back_populates="owner", uselist=False)
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="user")
    exchanges: Mapped[List["Exchange"]] = relationship(back_populates="user")
    assets: Mapped[List["Asset"]] = relationship(back_populates="user")
    purchased_merchandise: Mapped[List["Merchandise"]] = relationship(
        secondary="purchases", back_populates="buyers"
    )

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


class UserFollow(db.Model):
    """
    Represents a relationship where a user can follow another user within the system.

    The UserFollow class models the many-to-many relationship between users, where one
    user can follow another. It tracks the follower, the user being followed, and the
    timestamp of when the follow action occurred. This class is linked to the users table
    to establish relationships between users.

    :ivar id: Unique identifier of the user follow relationship.
    :type id: int
    :ivar follower_id: The UUID of the user who is following.
    :type follower_id: uuid.UUID
    :ivar followed_id: The UUID of the user being followed.
    :type followed_id: uuid.UUID
    :ivar created_at: The datetime when the follow relationship was created.
    :type created_at: datetime
    :ivar follower: The User instance representing the follower of the relationship.
    :type follower: User
    :ivar followed: The User instance representing the followed user in the relationship.
    :type followed: User
    """
    __tablename__ = "user_follows"

    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    followed_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationships
    follower: Mapped["User"] = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed: Mapped["User"] = relationship("User", foreign_keys=[followed_id], back_populates="followers")
