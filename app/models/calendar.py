from uuid import uuid4
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, Boolean, ForeignKey, JSON, Date, Integer, Float, Text, ARRAY, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, relationships
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from .associations import event_guests, event_moderators
from .utils.config import EventRepeat, EventStatus, EventType
from .mixins import (
    EntityMixin, HiveMixin, CliqueMixin, ModeratorMixin, CreatorMixin, OwnerMixin, AuthorMixin,
    ModelMixin
)


if TYPE_CHECKING:
    from .scrolls import Scroll
    from .user import User
    from .journal import Magazine, Article
    from .player import Bookmark, WatchHistory
    from .community import Message, Reaction, Fandom
    from .commerce import Fund, Transaction, Exchange
    from .library import Film, Person, Library
    from .common import DashboardTemplate, Visibility


def generate_uuid():
    return str(uuid4())


class Event(db.Model, ModelMixin):
    __tablename__ = "events"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    # Core fields
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    event_type: Mapped["EventType"] = mapped_column(SQLAlchemyEnum(EventType, name="event_type"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime)
    repeat: Mapped[EventRepeat] = mapped_column(SQLAlchemyEnum(EventRepeat, name="event_repeat"),
                                                default=EventRepeat.NONE)
    notification: Mapped[bool] = mapped_column(Boolean, default=True)
    reminder_offset: Mapped[Optional[int]] = mapped_column(Integer)
    # Metadata
    tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    status: Mapped[EventStatus] = mapped_column(SQLAlchemyEnum(EventStatus, name="event_status"),
                                                default=EventStatus.UPCOMING)
    visibility: Mapped[Visibility] = mapped_column(SQLAlchemyEnum(Visibility, name="event_visibility"),
                                                   default=Visibility.PRIVATE)
    priority: Mapped[Optional[int]] = mapped_column(Integer)
    # System Fields
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    synced_external_id: Mapped[Optional[str]] = mapped_column(String)
    # Relationships # TODO: Review these relationships
    calendar_id: Mapped[UUID] = mapped_column(ForeignKey("calendars.id"), nullable=False)
    calendar = relationship("Calendar", backref="events")
    venue_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("venues.id"))
    venue = relationship("Venue", backref="events")
    guests: Mapped[List["User"]] = relationship("User", secondary="event_guests", backref="invited_events")
    # moderators: Mapped[List["Clique"]] = relationship("Clique", secondary="event_moderators",
    #                                                   backref="moderated_events")

    def __repr__(self):
        return f"<Event {self.title} ({self.start_time})>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "event_type": self.event_type.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "repeat": self.repeat.value,
            "notification": self.notification,
            "reminder_offset": self.reminder_offset,
            "tags": self.tags,
            "status": self.status.value,
            "visibility": self.visibility.value,
            "priority": self.priority,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "synced_external_id": self.synced_external_id,
            "calendar_id": str(self.calendar_id),
            "venue_id": str(self.venue_id) if self.venue_id else None,
        }


class Log(db.Model, ModelMixin):
    pass


class Reminder(db.Model, ModelMixin):
    pass


class Calendar(db.Model, ModelMixin):
    __tablename__ = "calendars"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    # TODO: Generic ownership links that make Common Models generic, meaning they can belong to any Model
    owner_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    owner_type: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    # TODO: Review these relationships
    events: Mapped[List["Event"]] = relationship("Event", backref="calendar", cascade="all, delete-orphan")


