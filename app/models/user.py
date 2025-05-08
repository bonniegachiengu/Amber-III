from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import String, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from .utils.config import Visibility
from .mixins import EntityMixin, CliqueMixin, ModelMixin, LibraryMixin


if TYPE_CHECKING:
    from .community import Thread
    from .common import Location


class User(db.Model, ModelMixin, UserMixin, EntityMixin, LibraryMixin):
    """
    Represents a user model in the database.

    The User class encapsulates data and behavior related to application users. It extends
    multiple mixins to provide reusable functionalities for user authentication, entity
    management, and library interactions. The class also defines relationships to other
    models, such as locations, followers, and threads. Key system attributes include
    account metadata, preferences, and social features. This class can be used across
    the application to represent and manage user-related data.

    :ivar username: The unique username associated with the user.
    :type username: str
    :ivar email: The unique email address associated with the user.
    :type email: str
    :ivar password_hash: The hashed representation of the user's password.
    :type password_hash: str
    :ivar joined_at: The datetime when the user created their account.
    :type joined_at: datetime
    :ivar last_seen: The last datetime the user was active (optional).
    :type last_seen: Optional[datetime]
    :ivar bio: A brief biography or description of the user (optional).
    :type bio: Optional[str]
    :ivar avatar_url: URL of the user's avatar or profile picture (optional).
    :type avatar_url: Optional[str]
    :ivar location_id: The UUID reference to the user’s associated location (optional).
    :type location_id: Optional[UUID]
    :ivar portfolio_visibility: Visibility setting for the user's portfolio.
    :type portfolio_visibility: Visibility
    :ivar location: The `Location` instance representing the user’s location (related model).
    :type location: Location
    :ivar preferred_tags: A list of user-preferred tags for personalization (optional).
    :type preferred_tags: Optional[list]
    :ivar language: The user’s preferred language for the application interface.
    :type language: str
    :ivar streaming_accounts: A dictionary mapping user's streaming account info (optional).
    :type streaming_accounts: Optional[dict]
    :ivar playback_settings: A dictionary mapping user's playback preferences (optional).
    :type playback_settings: Optional[dict]
    :ivar role: The application-defined role assigned to the user (default is "user").
    :type role: str
    :ivar notifications_enabled: Indicates whether the user has enabled notifications.
    :type notifications_enabled: bool
    :ivar api_key: The API key for external services or integrations (optional).
    :type api_key: Optional[str]
    :ivar followers: List of `UserFollow` objects representing users following this user.
    :type followers: List[UserFollow]
    :ivar following: List of `UserFollow` objects representing users this user follows.
    :type following: List[UserFollow]
    :ivar cliques: List of `CliqueMixin` instances associated with the user.
    :type cliques: List[CliqueMixin]
    :ivar threads: List of `Thread` instances in which the user participates.
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
    catch_phrase: Mapped[Optional[str]] = mapped_column(String(100))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255))
    location_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("locations.id"), default=None)
    portfolio_visibility: Mapped[Visibility] = mapped_column(SQLAlchemyEnum(Visibility, name="portfolio_visibility"), default=Visibility.PUBLIC)
    location: Mapped["Location"] = relationship(back_populates="users")
    # Preferences & Personalization Fields
    preferred_tags: Mapped[Optional[list]] = mapped_column(JSON)
    language: Mapped[str] = mapped_column(String(10), default="en")
    streaming_accounts: Mapped[Optional[dict]] = mapped_column(JSON)
    playback_settings: Mapped[Optional[dict]] = mapped_column(JSON)
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
