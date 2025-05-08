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
    """
    Representation of a calendar entity.

    This class models a calendar that can have associated entities, events,
    and logs. It is designed for use within a database context and provides
    relational mapping to other components such as entities, events, and logs.
    The calendar additionally holds metadata such as its name and description.

    :ivar name: The name of the calendar.
    :type name: str
    :ivar description: Optional description for the calendar.
    :type description: Optional[str]
    :ivar entities: List of entities associated with the calendar.
    :type entities: List["EntityMixin"]
    :ivar events: List of events tied to this calendar.
    :type events: List["Event"]
    :ivar logs: List of logs related to operations on or within the calendar.
    :type logs: List["Log"]
    """
    __tablename__ = "calendars"
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(200))
    entities: Mapped[List["EntityMixin"]] = relationship("EntityMixin", backref="calendar")
    events: Mapped[List["Event"]] = relationship("Event", backref="parent_calendar")
    logs: Mapped[List["Log"]] = relationship("Log", backref="calendar")


class Event(db.Model, ModelMixin, EntityMixin, MarkMixin, EraMixin):
    """
    Represents an event within a calendar application, allowing configuration
    of event-specific attributes and relationships with other entities.

    This class is mapped to the "events" table in the database and facilitates
    the creation, modification, and management of events. It enables associating
    events with calendars, venues, users, and other related objects such as
    notifications, reminders, tickets, and logs. The use of mixin classes enhances
    the model with additional functionality such as marking, entity identification,
    and tracking within the historical context (era).

    :ivar event_type: The specific type of the event (e.g., meeting, party,
        appointment).
    :type event_type: EventType
    :ivar repeat: The recurrence configuration of the event (e.g., none, daily,
        weekly).
    :type repeat: EventRepeat
    :ivar status: The current status of the event (e.g., upcoming,
        completed, canceled).
    :type status: EventStatus
    :ivar visibility: The visibility setting of the event (e.g., private,
        public, restricted).
    :type visibility: Visibility
    :ivar priority: An optional integer representing the priority level of the
        event, where a smaller value indicates higher priority.
    :type priority: Optional[int]
    :ivar parent_calendar_id: Identifier of the calendar that this event belongs
        to.
    :type parent_calendar_id: UUID
    :ivar venue_id: Optional identifier of the venue where the event is
        taking place.
    :type venue_id: Optional[UUID]
    :ivar parent_calendar: Relationship linking this event to the parent
        calendar entity.
    :type parent_calendar: Calendar
    :ivar venue: Optional relationship linking this event to the venue entity.
    :type venue: Venue
    :ivar guests: List of users invited to attend the event.
    :type guests: List[User]
    :ivar organizers: List of organizers associated with the event.
    :type organizers: List[Organizer]
    :ivar notifications: List of notifications associated with the event.
        Notifications are cascaded and removed when the event is deleted.
    :type notifications: List[Notification]
    :ivar reminders: List of reminders tied to the event. Reminders are deleted
        along with the event.
    :type reminders: List[Reminder]
    :ivar tickets: List of tickets associated with the event. Tickets are
        also deleted when the event is removed.
    :type tickets: List[Ticket]
    :ivar logs: List of logs recording changes or actions associated with the
        event. Logs are cascaded and removed with the event.
    :type logs: List[Log]
    :ivar ctas: List of call-to-action (CTA) elements associated with the
        event. These elements are also removed when the event is deleted.
    :type ctas: List[CTA]
    """
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
    """
    Represents a reminder associated with an event in the system.

    This class defines a Reminder, which is linked to an event and includes details
    like the reminder message and the time the reminder should trigger. It utilizes
    SQLAlchemy's ORM capabilities to map this class to the corresponding database
    table and manage relationships with other entities.

    :ivar event_id: Identifier of the associated event to which the reminder belongs.
    :type event_id: UUID
    :ivar message: The reminder message text.
    :type message: str
    :ivar reminder_at: The datetime at which the reminder is set to trigger.
    :type reminder_at: datetime
    :ivar event: The event object associated with the reminder.
    :type event: Event
    """
    __tablename__ = "reminders"
    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id"), nullable=False)
    message: Mapped[str] = mapped_column(String(200), nullable=False)
    reminder_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    event: Mapped["Event"] = relationship("Event", backref="reminders")


class Ticket(db.Model, ModelMixin, EraMixin):
    """
    Represents a ticket for an event, including information about its associated entities
    and attributes such as type, quantity, and price.

    This class is used to model tickets within the system, linking them to their respective
    creator portfolios, events, currencies, orders, transactions, and other related entities.
    It provides fields for tracking ticket details, such as type, price, quantity, and status.

    :ivar creator_portfolio_id: Identifier of the portfolio that created the ticket.
    :type creator_portfolio_id: UUID
    :ivar event_id: Identifier of the event associated with the ticket.
    :type event_id: UUID
    :ivar currency_id: Identifier of the currency associated with the ticket.
    :type currency_id: UUID
    :ivar order_id: Identifier of the order associated with the ticket.
    :type order_id: UUID
    :ivar transaction_id: Identifier of the transaction associated with the ticket.
    :type transaction_id: UUID, optional
    :ivar type: Type of the ticket (e.g., FREE, PAID).
    :type type: TicketType
    :ivar quantity: Number of tickets associated with this instance.
    :type quantity: int
    :ivar price: Price of the ticket in specified currency.
    :type price: float
    :ivar status: Current status of the ticket (e.g., ACTIVE, CANCELLED).
    :type status: TicketStatus
    :ivar creator_portfolio: The portfolio that created this ticket. Related via `creator_portfolio_id`.
    :type creator_portfolio: Portfolio
    :ivar event: The event associated with this ticket. Related via `event_id`.
    :type event: Event
    :ivar buying_portfolios: List of portfolios that have purchased this ticket.
    :type buying_portfolios: List[Portfolio]
    :ivar currency: The currency associated with this ticket. Related via `currency_id`.
    :type currency: Currency
    :ivar transaction: The transaction associated with this ticket. Related via `transaction_id`.
    :type transaction: Transaction, optional
    :ivar order: The order associated with this ticket. Related via `order_id`.
    :type order: Order
    """
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
    """
    Represents a log entry in the database.

    This class defines a log entry model that is associated with an event and a
    calendar. It stores information about the log's title, content, and its
    associations with corresponding event and calendar objects. The class is
    defined as part of an ORM model, inheriting from `db.Model` and `ModelMixin`.

    :ivar event_id: The unique identifier for the associated event.
    :type event_id: UUID
    :ivar calendar_id: The unique identifier for the associated calendar.
    :type calendar_id: UUID
    :ivar title: The title of the log entry, limited to 100 characters.
    :type title: str
    :ivar content: The optional content of the log entry.
    :type content: str or None
    :ivar event: The associated `Event` object for the log entry, forming a
        relationship with the `Event` table.
    :type event: Event
    :ivar calendar: The associated `Calendar` object for the log entry, forming a
        relationship with the `Calendar` table.
    :type calendar: Calendar
    """
    __tablename__ = "logs"
    event_id: Mapped[UUID] = mapped_column(ForeignKey("events.id"), nullable=False)
    calendar_id: Mapped[UUID] = mapped_column(ForeignKey("calendars.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    event: Mapped["Event"] = relationship("Event", backref="logs")
    calendar: Mapped["Calendar"] = relationship("Calendar", backref="logs")
