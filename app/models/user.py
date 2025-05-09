import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import String, ForeignKey, JSONB, UniqueConstraint, Enum as SQLAlchemyEnum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from .utils.config import Visibility
from .mixins import CliqueMixin, ModelMixin, LibraryMixin


if TYPE_CHECKING:
    from .community import Thread
    from .common import Location
    from .calendar import Calendar


class User(db.Model, ModelMixin, UserMixin, LibraryMixin):
    """
    Represents a user entity in the application, managing core user-related data and preferences.

    This class is used for managing user data within the database. It contains essential attributes
    such as username, email, password_hash, as well as optional fields for personalization like bio,
    avatar_url, and social features like 'followers' and 'following' relationships. It integrates with
    multiple mixins to provide enhanced functionality for user models.

    :ivar username: The unique identifier for the user.
    :type username: str
    :ivar email: The email address of the user, used for identification and communication.
    :type email: str
    :ivar password_hash: A hashed representation of the user's password.
    :type password_hash: str
    :ivar name: The full name of the user.
    :type name: str
    :ivar joined_at: The date and time when the user created the account.
    :type joined_at: datetime
    :ivar last_seen: The most recent date and time the user was active. This may be None.
    :type last_seen: Optional[datetime]
    :ivar is_active: Indicates if the user account is currently active.
    :type is_active: bool
    :ivar is_verified: Indicates if the user's email address or account is verified.
    :type is_verified: bool
    :ivar is_deleted: Indicates if the user's account has been marked for deletion.
    :type is_deleted: bool
    :ivar icon: A path or URL for the user's profile icon. This may be None.
    :type icon: Optional[str]
    :ivar slug: A unique slug identifier for the user's profile.
    :type slug: str
    :ivar bio: A short biography or description of the user. This may be None.
    :type bio: Optional[str]
    :ivar catchphrase: A user's chosen phrase or tagline. This may be None.
    :type catchphrase: Optional[str]
    :ivar avatar_url: URL for the user's profile avatar. This may be None.
    :type avatar_url: Optional[str]
    :ivar location_id: The UUID of the user's associated location. This may be None.
    :type location_id: Optional[UUID]
    :ivar portfolio_visibility: Determines the user's portfolio visibility. Defaults to public.
    :type portfolio_visibility: Visibility
    :ivar location: Relationship to the location associated with the user.
    :type location: Location
    :ivar calendar_id: The UUID of the user's associated calendar.
    :type calendar_id: uuid.UUID
    :ivar calendar: Relationship to the user's linked calendar entity.
    :type calendar: Calendar
    :ivar preferred_tags: A list of user's preferred tags for personalization. This may be None.
    :type preferred_tags: Optional[list]
    :ivar language: The language preference of the user. Defaults to "en".
    :type language: str
    :ivar streaming_accounts: A dictionary of the user's streaming accounts. This may be None.
    :type streaming_accounts: Optional[dict]
    :ivar playback_settings: A dictionary defining playback settings for the user. This may be None.
    :type playback_settings: Optional[dict]
    :ivar settings: A dictionary containing the user's system and personalization settings. This may be None.
    :type settings: Optional[dict]
    :ivar role: The role assigned to the user, defaults to "user".
    :type role: str
    :ivar notifications_enabled: Specifies whether notifications are enabled for the user.
    :type notifications_enabled: bool
    :ivar api_key: A unique API key assigned to the user. This may be None.
    :type api_key: Optional[str]
    :ivar followers: List of relationships representing other users following this user.
    :type followers: List[UserFollow]
    :ivar following: List of relationships representing other users followed by this user.
    :type following: List[UserFollow]
    :ivar cliques: List of cliques the user belongs to.
    :type cliques: List[CliqueMixin]
    :ivar threads: List of threads in which the user is a participant.
    :type threads: List[Thread]
    """
    __tablename__ = "users"
    # Core Fields
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), generate_password_hash())
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(default=datetime.now)
    last_seen: Mapped[Optional[datetime]] = mapped_column(default=None)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    # Profile & Social Fields
    icon: Mapped[Optional[str]] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(500))
    catchphrase: Mapped[Optional[str]] = mapped_column(String(100))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255))
    location_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("locations.id"), default=None)
    portfolio_visibility: Mapped[Visibility] = mapped_column(SQLAlchemyEnum(Visibility, name="portfolio_visibility"), default=Visibility.PUBLIC)
    location: Mapped["Location"] = relationship(back_populates="users")
    calendar_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("calendars.id"), default=None, nullable=False)
    calendar: Mapped["Calendar"] = relationship(back_populates="entities", uselist=False)
    # Preferences & Personalization Fields
    preferred_tags: Mapped[Optional[list]] = mapped_column(JSONB)
    language: Mapped[str] = mapped_column(String(10), default="en")
    streaming_accounts: Mapped[Optional[dict]] = mapped_column(JSONB)
    playback_settings: Mapped[Optional[dict]] = mapped_column(JSONB)
    settings: Mapped[Optional[dict]] = mapped_column(JSONB)
    # System Fields
    role: Mapped[str] = mapped_column(String(20), default="user")
    notifications_enabled: Mapped[bool] = mapped_column(default=True)
    api_key: Mapped[Optional[str]] = mapped_column(String(64), unique=True)
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
    cliques: Mapped[List["CliqueMixin"]] = relationship(back_populates="agents", cascade="all, delete-orphan")
    threads: Mapped[List["Thread"]] = relationship(back_populates="participants")

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        pass

    def set_password(self, password: str) -> None:
        """
        Hashes the provided password and sets it as the password hash.

        :param password: The plain text password that needs to be hashed.
        :type password: str
        :return: None
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Check if the provided password matches the stored password hash.

        This method verifies if the given password, after being hashed, matches
        the previously stored password hash for the user. It is commonly used
        for authentication to validate user credentials.

        :param password: The plain text password input is provided for verification.
        :type password: str
        :return: True if the password matches the hash, False otherwise.
        :rtype: bool
        """
        return check_password_hash(self.password_hash, password)


class UserFollow(db.Model, ModelMixin):
    """
    Represents a relationship where one user follows another user.

    UserFollow is a database model that establishes a many-to-many relationship between
    users, where one user (follower) tracks or subscribes to the updates of another user (followed).
    Each instance corresponds to a unique follower-followed pair.

    :ivar __tablename__: The name of the database table associated with this model.
    :type __tablename__: str
    :ivar __table_args__: Additional configurations for the database table, including constraints.
    :type __table_args__: tuple
    :ivar follower_id: Unique identifier of the user who follows another user.
    :type follower_id: UUID
    :ivar followed_id: Unique identifier of the user being followed.
    :type followed_id: UUID
    :ivar follower: Relationship representing the user entity acting as the follower in the relationship.
    :type follower: User
    :ivar followed: Relationship representing the user entity being followed in the relationship.
    :type followed: User
    """
    __tablename__ = "user_follows"
    __table_args__ = (UniqueConstraint("follower_id", "followed_id"), "uq_user_follows",)
    follower_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    followed_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    follower: Mapped["User"] = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed: Mapped["User"] = relationship("User", foreign_keys=[followed_id], back_populates="followers")
