from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, Boolean, ForeignKey, JSONB, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..extensions import db
from .mixins import ModelMixin, EraMixin, ContributionMixin
from .associations import subtitle_contributors

if TYPE_CHECKING:
    from .library import Library, WatchHistory, Film, Album, Hitlist


class PlaybackSession(db.Model, ModelMixin, EraMixin):
    """
    Represents a playback session for media content.

    This class defines the structure and relationships of a playback session within
    the application. It is used to track media playback status, associated media
    entities, and related bookmark and queue information. The class integrates with
    the database via SQLAlchemy and manages associations with Library, Film, Album,
    and Hitlist entities. It also tracks playback position and whether the session
    is part of a watch party.

    Relationships are defined for accessing related entities and their interactions
    with playback sessions, such as bookmarks and playback queue items.

    :ivar library_id: Identifier for the associated library.
    :type library_id: UUID
    :ivar film_id: Identifier for the associated film.
    :type film_id: UUID
    :ivar album_id: Identifier for the associated album, nullable if no album is
        linked.
    :type album_id: Optional[UUID]
    :ivar hitlist_id: Identifier for the associated hitlist, nullable if no hitlist
        is linked.
    :type hitlist_id: Optional[UUID]
    :ivar is_watch_party: Indicates if the session is part of a watch party.
    :type is_watch_party: bool
    :ivar current_position: Current playback position in seconds.
    :type current_position: float
    :ivar library: Relationship linking the playback session to the library table.
    :type library: Library
    :ivar film: Relationship linking the playback session to the film table.
    :type film: Film
    :ivar album: Relationship linking the playback session to the album table.
    :type album: Album
    :ivar hitlist: Relationship linking the playback session to the hitlist table.
    :type hitlist: Hitlist
    :ivar bookmarks: List of bookmark entities associated with the playback session.
    :type bookmarks: List[Bookmark]
    :ivar queue_items: List of queue items associated with playback, maintaining
        their order, and supporting cascading delete functionality.
    :type queue_items: List[QueueItem]
    """
    __tablename__ = "playback_sessions"
    library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("libraries.id"))
    film_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("films.id"))
    album_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("albums.id"), nullable=True)
    hitlist_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("hitlists.id"), nullable=True)
    is_watch_party: Mapped[bool] = mapped_column(Boolean, default=False)
    current_position: Mapped[float] = mapped_column(Float, default=0.0)
    library: Mapped["Library"] = relationship("Library", back_populates="playback_sessions")
    film: Mapped["Film"] = relationship("Film")
    album: Mapped["Album"] = relationship("Album")
    hitlist: Mapped["Hitlist"] = relationship("Hitlist")
    bookmarks: Mapped[List["Bookmark"]] = relationship("Bookmark", back_populates="session")
    queue_items: Mapped[List["QueueItem"]] = relationship("QueueItem", order_by="QueueItem.position", back_populates="session", cascade="all, delete-orphan")


class QueueItem(db.Model, ModelMixin):
    """
    Represents an item in a queue system.

    This class is used to manage and organize items within a queue, which is tied to a playback
    session and a specific film. It provides information about the current state of the queued
    item (played, skipped, etc.), its position, loop count, and any additional metadata. It also
    manages relationships with associated PlaybackSession and Film objects.

    :ivar session_id: The unique identifier of the playback session the queue item belongs to.
    :type session_id: UUID
    :ivar film_id: The unique identifier of the film associated with the queue item.
    :type film_id: UUID
    :ivar position: The position of the queue item within the playback queue.
    :type position: int
    :ivar is_played: Indicates whether the film has been played or not.
    :type is_played: bool
    :ivar is_skipped: Indicates whether the film has been skipped or not.
    :type is_skipped: bool
    :ivar loop_count: The number of times this film has been looped.
    :type loop_count: int
    :ivar metadata: Additional data or settings associated with the queue item.
    :type metadata: dict
    :ivar session: The playback session to which this queue item belongs.
    :type session: PlaybackSession
    :ivar film: The film associated with this queue item.
    :type film: Film
    """
    __tablename__ = "queues"
    session_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("playback_sessions.id"))
    film_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("films.id"))
    position: Mapped[int] = mapped_column(Integer, default=0)
    is_played: Mapped[bool] = mapped_column(Boolean, default=False)
    is_skipped: Mapped[bool] = mapped_column(Boolean, default=False)
    loop_count: Mapped[int] = mapped_column(Integer, default=0)
    metadata: Mapped[dict] = mapped_column(JSONB, default={})
    session: Mapped["PlaybackSession"] = relationship("PlaybackSession", back_populates="queue_items")
    film: Mapped["Film"] = relationship("Film")


class Subtitle(db.Model, ModelMixin, ContributionMixin):
    """
    Represents the Subtitle model within the database.

    This class is used to define the attributes and relationships associated with
    a subtitle entry in the database. Each subtitle entry corresponds to a
    specific film and includes details such as language and the URL for the
    subtitle file.

    :ivar film_id: The unique identifier of the related film, which is a foreign key
        linking this subtitle to a film entry.
    :type film_id: UUID
    :ivar language: The language of the subtitle.
    :type language: str
    :ivar url: The URL where the subtitle file can be accessed.
    :type url: str
    :ivar film: The film object associated with the subtitle, defining a relationship
        between the subtitle and its respective film.
    :type film: Film
    """
    __tablename__ = "subtitles"
    __contribution_table__ = subtitle_contributors
    __contribution_backref__ = "subtitle_contributions"
    film_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("films.id"))
    language: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    film: Mapped["Film"] = relationship("Film", back_populates="subtitles")


class Bookmark(db.Model, ModelMixin):
    """
    Represents a bookmark in the system.

    This class is a representation of a bookmark, which stores information about
    the user's position in a film, the sequence of films being watched, and related
    data like the associated watch history and playback session. It is closely
    linked with other entities in the system such as WatchHistory, PlaybackSession,
    and Film for relational mapping. The purpose of this class is to manage and
    persist bookmark-related data efficiently.

    :ivar watch_history_id: ID of the associated watch history.
    :type watch_history_id: UUID
    :ivar session_id: ID of the associated playback session.
    :type session_id: UUID
    :ivar film_id: ID of the associated film.
    :type film_id: UUID
    :ivar position: The playback position in seconds.
    :type position: float
    :ivar film_sequence: an Ordered list of film IDs representing a sequence of
        films.
    :type film_sequence: list[UUID]
    :ivar watch_history: The related WatchHistory object.
    :type watch_history: WatchHistory
    :ivar session: The related PlaybackSession object.
    :type session: PlaybackSession
    :ivar film: The related Film object.
    :type film: Film
    """
    __tablename__ = "bookmarks"
    watch_history_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("watch_histories.id"), nullable=False)
    session_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("playback_sessions.id"), nullable=False)
    film_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("films.id"), nullable=False)
    position: Mapped[float] = mapped_column(Float, default=0.0) # seconds
    film_sequence: Mapped[list[UUID]] = mapped_column(JSONB, default=[]) # ordered list of film ids
    watch_history: Mapped["WatchHistory"] = relationship("WatchHistory", back_populates="bookmarks")
    session: Mapped["PlaybackSession"] = relationship("PlaybackSession", back_populates="bookmarks")
    film: Mapped["Film"] = relationship("Film")
