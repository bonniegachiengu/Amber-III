from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import String, ForeignKey, JSONB, UniqueConstraint, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from . import EntityMixin
from ..extensions import db
from .utils.config import VisibilityEnum
from .mixins import CliqueMixin, ModelMixin, LibraryMixin


if TYPE_CHECKING:
    from .community import Thread
    from .common import Location, Avatar
    from .calendar import Event
    from .library import Person


class User(db.Model, ModelMixin, UserMixin, LibraryMixin, EntityMixin):
    """
    Represents a user in the system.

    This class defines the `User` model, which includes core user attributes,
    profile details, preferences, and social features. It supports authentication,
    relationships with other models, and customization of the user experience. The
    class integrates with SQLAlchemy for database mapping and allows user details
    to be securely stored and managed.

    :ivar __tablename__: Name of the database table associated with this model.
    :type __tablename__: str
    :ivar username: Unique username for the user.
    :type username: str
    :ivar email: Unique email address used for user identification and communication.
    :type email: str
    :ivar password_hash: Encrypted password hash for authenticating the user.
    :type password_hash: str
    :ivar joined_at: The timestamp of when the user account was originally created.
    :type joined_at: datetime
    :ivar last_seen: The timestamp of when the user was last active.
    :type last_seen: Optional[datetime]
    :ivar bio: A short biography provided by the user.
    :type bio: Optional[str]
    :ivar catchphrase: User's personal catchphrase or tagline.
    :type catchphrase: Optional[str]
    :ivar avatar: The user's avatar image.
    :type avatar: Optional[Avatar]
    :ivar location_id: Unique identifier for the user's location.
    :type location_id: Optional[UUID]
    :ivar portfolio_visibility: Enum representing the visibility preference for the user's portfolio.
    :type portfolio_visibility: VisibilityEnum
    :ivar location: Relationship to the related `Location` object.
    :type location: Location
    :ivar preferred_tags: List of user-preferred tags represented in JSON format.
    :type preferred_tags: Optional[list]
    :ivar language: Default language preference for the user. Defaults to "en".
    :type language: str
    :ivar streaming_accounts: User's linked streaming service accounts in JSON format.
    :type streaming_accounts: Optional[dict]
    :ivar playback_settings: User's playback configuration or settings in JSON format.
    :type playback_settings: Optional[dict]
    :ivar role: User's role in the system, specifying permissions or access level.
    :type role: str
    :ivar notifications_enabled: Denotes whether the user has enabled notifications.
    :type notifications_enabled: bool
    :ivar api_key: Unique API key assigned to the user for accessing system API.
    :type api_key: Optional[str]
    :ivar followers: List of `UserFollow` entries where the user is being followed.
    :type followers: List[UserFollow]
    :ivar following: List of `UserFollow` entries where the user is following others.
    :type following: List[UserFollow]
    :ivar cliques: List of related groups (cliques) where the user is a participant.
    :type cliques: List[CliqueMixin]
    :ivar threads: List of message threads where the user is a participant.
    :type threads: List[Thread]
    """
    __tablename__ = "users"
    # Core Fields
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), generate_password_hash())
    joined_at: Mapped[datetime] = mapped_column(default=datetime.now)
    last_seen: Mapped[Optional[datetime]] = mapped_column(default=None)
    # Profile & Social Fields
    bio: Mapped[Optional[str]] = mapped_column(String(500))
    catchphrase: Mapped[Optional[str]] = mapped_column(String(100))
    avatar_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("avatars.id"), default=None)

    avatar: Mapped["Avatar"] = relationship("Person", back_populates="use_cases")

    location_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("locations.id"), default=None)
    location: Mapped["Location"] = relationship(back_populates="users")
    portfolio_visibility: Mapped[VisibilityEnum] = mapped_column(SQLAlchemyEnum(VisibilityEnum, name="portfolio_visibility"), default=VisibilityEnum.PUBLIC)
    claimed_person_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("persons.id"), default=None)
    claimed_person: Mapped["Person"] = relationship("Person", back_populates="claimed_by")
    # Preferences & Personalization Fields
    preferred_tags: Mapped[Optional[list]] = mapped_column(JSONB)
    language: Mapped[str] = mapped_column(String(10), default="en")
    streaming_accounts: Mapped[Optional[dict]] = mapped_column(JSONB)
    playback_settings: Mapped[Optional[dict]] = mapped_column(JSONB)
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
    invited_events: Mapped[List["Event"]] = relationship("Event", foreign_keys="[Event.invited_by_id]", back_populates="invited_guests")
    confirmed_events: Mapped[List["Event"]] = relationship("Event", foreign_keys="[Event.accepted_by_id]", back_populates="confirmed_guests")

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
