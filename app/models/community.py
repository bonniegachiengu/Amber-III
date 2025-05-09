import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, relationships
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from .associations import fandom_contributors, club_contributors
from .mixins import (
    EntityMixin, HiveMixin, CliqueMixin, ModeratorMixin, CreatorMixin, OwnerMixin, AuthorMixin,
    ModelMixin, PerksMixin, BoardMixin, EntryMixin, WallMixin, PostMixin, ActionMixin, ContributionMixin
)

if TYPE_CHECKING:
    from user import User
    from .scrolls import Scroll
    from .library import Library, Shop
    from .journal import Magazine, Article
    from .player import WatchHistory
    from .commerce import Fund, Transaction
    from .common import WikiTemplate, DashboardTemplate
    from .calendar import Event, Calendar


class Contributor(db.Model, ModelMixin):
    __tablename__ = "contributors"
    contributor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), primary_key=True)
    contributions_fund_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("funds.id"), primary_key=True)
    contribution_type: Mapped[str] = mapped_column(String(100), primary_key=True)
    contributor: Mapped["Library"] = relationship(back_populates="contributions")
    contributions_fund: Mapped["Fund"] = relationship("Fund")


class Arena(db.Model, ModelMixin, EntityMixin, HiveMixin):
    __tablename__ = "arena"

class Club(db.Model, ModelMixin, EntityMixin, HiveMixin, ContributionMixin):
    __tablename__ = "clubs"
    __contribution_table__ = club_contributors
    __contribution_backref__ = "club_contributions"


class Fandom(db.Model, ModelMixin, EntityMixin, HiveMixin, ContributionMixin):
    __tablename__ = "fandoms"
    __contribution_table__ = fandom_contributors
    __contribution_backref__ = "fandom_contributions"


class Thread(db.Model, ModelMixin):
    __tablename__ = "threads"
    topic_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    participants: Mapped[List["User"]] = relationship("User", secondary="threads")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="thread")


class Message(db.Model, ModelMixin):
    __tablename__ = "messages"
    thread_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("threads.topic_id"), primary_key=True)
    sender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)

    message: Mapped[str] = mapped_column(String(500))
    thread: Mapped["Thread"] = relationship("Thread", back_populates="messages")
    sender: Mapped["User"] = relationship("User", foreign_keys=[sender_id])
    replies: Mapped[List["Reply"]] = relationship("Reply", back_populates="parent_message")
    reactions: Mapped[List["Reaction"]] = relationship("Reaction", back_populates="message")


class Reply(db.Model, ModelMixin, Message): # TODO: Make reply and message and reaction Polymorphic
    parent_message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("messages.id"), primary_key=True)
    parent_message: Mapped["Message"] = relationship("Message", foreign_keys=[parent_message_id], back_populates="replies")

class Reaction(db.Model, ModelMixin, Message):
    parent_message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("messages.id"), primary_key=True)
    parent_message: Mapped["Message"] = relationship("Message", foreign_keys=[parent_message_id], back_populates="reactions")
    reaction: Mapped[str] = mapped_column(String(100))




class Member(db.Model, ModelMixin, CliqueMixin):
    pass


class Subscriber(db.Model, ModelMixin, CliqueMixin):
    __tablename__ = "subscribers"
    hive_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    hive: Mapped["HiveMixin"] = relationship(HiveMixin, back_populates="subscribers")


class Fan(db.Model, ModelMixin, CliqueMixin):
    pass


class Watcher(db.Model, ModelMixin, CliqueMixin):
    pass

class Tracker(db.Model, ModelMixin, CliqueMixin):
    pass

class Collector(db.Model, ModelMixin, CliqueMixin): # something to do with scrolls
    pass

class Creator(db.Model, ModelMixin, CliqueMixin, ModeratorMixin, CreatorMixin):
    pass


class Organizer(db.Model, ModelMixin, CliqueMixin, ModeratorMixin):
    pass


class Reward(db.Model, ModelMixin, PerksMixin):
    pass


class Tier(db.Model, ModelMixin):
    __tablename__ = "tiers"
    hive_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False) # TODO: Perhaps add an ID override in all Mixins suggesting a need for it
    hive: Mapped["HiveMixin"] = relationship(HiveMixin, back_populates="tiers")
    perks: Mapped[List["PerksMixin"]] = relationship("PerksMixin", back_populates="tier")
    subscribers: Mapped[List["Subscriber"]] = relationship("Subscriber", back_populates="hive")


class Pins(db.Model, ModelMixin, BoardMixin):
    pass


class Pin(db.Model, ModelMixin, EntryMixin):
    __tablename__ = "pins"


class Updates(db.Model, ModelMixin, BoardMixin):
    pass


class Update(db.Model, ModelMixin, EntryMixin):
    __tablename__ = "updates"


class Issues(db.Model, ModelMixin, BoardMixin):
    pass


class Issue(db.Model, ModelMixin, EntryMixin):
    pass


class Posts(db.Model, ModelMixin, WallMixin):
    pass


class Post(db.Model, ModelMixin, PostMixin):
    pass


class Clips(db.Model, ModelMixin, WallMixin):
    pass


class Clip(db.Model, ModelMixin, PostMixin):
    pass


#---------------------------- Actions ------------------------------

class Write(db.Model, ModelMixin, ActionMixin):
    pass


class Publish(db.Model, ModelMixin, ActionMixin):
    pass


class Review(db.Model, ModelMixin, ActionMixin):
    pass


class Follow(db.Model, ModelMixin, ActionMixin):
    pass
