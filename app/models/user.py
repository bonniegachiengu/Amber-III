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
    Represents a user in the system.

    The User class encompasses all core attributes, social information, relationships,
    preferences, and system-level metadata about a user. It is heavily utilized in
    authentication, authorization, and user-related content creation. This class
    interacts with other parts of the system such as watchlists, content libraries,
    social connections, and marketplace activity.

    Direct database relationships and rich metadata enable the User model to serve
    as a centralized entity for personal, social, and system-level features. User
    details such as preferences, social connections, and activity facilitate flexible
    customization and personalization.

    :ivar id: The unique identifier for the user.
    :ivar username: The unique username associated with the user.
    :ivar email: The unique email address of the user.
    :ivar password_hash: The hashed password for authentication purposes.
    :ivar is_verified: Indicates whether the user has verified their email.
    :ivar is_active: Indicates whether the user's account is active.
    :ivar joined_at: The date and time when the user joined.
    :ivar last_seen: The last date and time the user was active.
    :ivar bio: A short biography of the user.
    :ivar avatar_url: The URL of the user's avatar or profile picture.
    :ivar location: The geographical location of the user.
    :ivar portfolio_visibility: Visibility setting of the user's portfolio.
    :ivar preferred_tags: Tags representing the user's preferred topics or interests.
    :ivar language: The preferred language code of the user.
    :ivar streaming_accounts: Streaming account details connected to the user.
    :ivar playback_settings: User's personal playback preferences or configurations.
    :ivar calendar: Calendar metadata associated with the user's activities.
    :ivar created_at: The datetime when the user record was created.
    :ivar updated_at: The datetime when the user record was last updated.
    :ivar deleted_at: The datetime when the user record was deleted.
    :ivar deleted_by: ID of the user who deleted this user record, if applicable.
    :ivar role: The role assigned to the user (e.g., admin, user).
    :ivar settings: Arbitrary user settings stored as a JSON object.
    :ivar notifications_enabled: Indicates if notifications are enabled for the user.
    :ivar api_key: The unique API key generated for the user.
    :ivar watchlists: List of watchlists created or owned by the user.
    :ivar library: List of collections in the user's library.
    :ivar magazines: List of magazines created by the user.
    :ivar articles: List of articles authored by the user.
    :ivar scrolls: List of scrolls associated with the user.
    :ivar bookmarks: List of bookmarks created by the user.
    :ivar watch_history: List of media watch history records for the user.
    :ivar contributions: List of contributions made by the user.
    :ivar followers: List of users following this user.
    :ivar following: List of users this user is following.
    :ivar joined_hives: List of hives the user has joined.
    :ivar cliques: List of cliques the user is a member of.
    :ivar comments: List of comments made by the user.
    :ivar reactions: List of reactions created by the user.
    :ivar cloned_hitlists: List of watchlists cloned by the user.
    :ivar ambertokens: Number of AmberTokens owned by the user.
    :ivar fund: The associated fund for the user, if applicable.
    :ivar shop: The associated shop owned by the user, if applicable.
    :ivar transactions: List of transactions belonging to the user.
    :ivar exchanges: List of exchanges associated with the user.
    :ivar assets: List of assets owned by the user.
    :ivar purchased_merchandise: List of merchandise purchased by the user.
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
