from uuid import uuid4
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Integer, Text, DateTime, Numeric
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..extensions import db
from .utils.config import EventRepeat, EventStatus, EventType, Visibility, TicketType, TicketStatus
from .mixins import EntityMixin, ModelMixin, MarkMixin, EraMixin


if TYPE_CHECKING:
    from .user import User
    from .community import Organizer
    from .commerce import Transaction, Currency, Order
    from .library import Portfolio
    from .common import Notification, Venue, CTA


def generate_uuid():
    return str(uuid4())

class Calendar(db.Model, ModelMixin):
    __tablename__ = "calendars"
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(200))
    entities: Mapped[List["EntityMixin"]] = relationship("EntityMixin", backref="calendar")
    events: Mapped[List["Event"]] = relationship("Event", backref="parent_calendar")
    logs: Mapped[List["Log"]] = relationship("Log", backref="calendar")


class Event(db.Model, ModelMixin, EntityMixin, MarkMixin, EraMixin):
    __tablename__ = "events"
    event_type: Mapped["EventType"] = mapped_column(SQLAlchemyEnum(EventType, name="event_type"), nullable=False)
    repeat: Mapped[EventRepeat] = mapped_column(SQLAlchemyEnum(EventRepeat, name="event_repeat"), default=EventRepeat.NONE)
    status: Mapped[EventStatus] = mapped_column(SQLAlchemyEnum(EventStatus, name="event_status"), default=EventStatus.UPCOMING)
    visibility: Mapped[Visibility] = mapped_column(SQLAlchemyEnum(Visibility, name="event_visibility"), default=Visibility.PRIVATE)
    priority: Mapped[Optional[int]] = mapped_column(Integer)
    parent_calendar_id: Mapped[UUID] = mapped_column(ForeignKey("calendars.id"), nullable=False)
    venue_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("venues.id"))
    parent_calendar: Mapped["Calendar"] = relationship("Calendar", backref="events")
    venue: Mapped["Venue"] = relationship("Venue", backref="events")
    guests: Mapped[List["User"]] = relationship("User", backref="invited_events")
    organizers: Mapped[List["Organizer"]] = relationship("Organizer", backref="events")
    notifications: Mapped[List["Notification"]] = relationship("Notification", backref="event", cascade="all, delete-orphan")
    reminders: Mapped[List["Reminder"]] = relationship("Reminder", backref="event", cascade="all, delete-orphan")
    tickets: Mapped[List["Ticket"]] = relationship("Ticket", backref="event", cascade="all, delete-orphan")
    logs: Mapped[List["Log"]] = relationship("Log", backref="event", cascade="all, delete-orphan")
    ctas: Mapped[List["CTA"]] = relationship("CTA", cascade="all, delete-orphan")


class Reminder(db.Model, ModelMixin):
    __tablename__ = "reminders"
    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id"), nullable=False)
    message: Mapped[str] = mapped_column(String(200), nullable=False)
    reminder_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    event: Mapped["Event"] = relationship("Event", backref="reminders")


class Ticket(db.Model, ModelMixin, EraMixin):
    __tablename__ = "tickets"
    creator_portfolio_id: Mapped[UUID] = mapped_column(ForeignKey("portfolios.id"), nullable=False)
    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id"), nullable=False)
    currency_id: Mapped[UUID] = mapped_column(ForeignKey("currencies.id"), nullable=False)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id"), nullable=False)
    transaction_id: Mapped[UUID] = mapped_column(ForeignKey("transactions.id"))
    type: Mapped["TicketType"] = mapped_column(SQLAlchemyEnum(TicketType, name="ticket_type"), nullable=False, default=TicketType.FREE)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0.0)
    status: Mapped["TicketStatus"] = mapped_column(SQLAlchemyEnum(TicketStatus, name="ticket_status"), nullable=False)
    creator_portfolio: Mapped["Portfolio"] = relationship("Portfolio", backref="created_tickets")
    event: Mapped["Event"] = relationship("Event", backref="tickets")
    buying_portfolios: Mapped[List["Portfolio"]] = relationship("Portfolio", backref="bought_tickets")
    currency: Mapped["Currency"] = relationship("Currency", backref="tickets")
    transaction: Mapped["Transaction"] = relationship("Transaction")
    order: Mapped["Order"] = relationship("Order")


class Log(db.Model, ModelMixin):
    __tablename__ = "logs"
    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id"), nullable=False)
    calendar_id: Mapped[UUID] = mapped_column(ForeignKey("calendars.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    event: Mapped["Event"] = relationship("Event", backref="logs")
    calendar: Mapped["Calendar"] = relationship("Calendar", backref="logs")
