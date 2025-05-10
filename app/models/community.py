import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, relationships
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from .associations import fandom_contributors, club_contributors
from .mixins import (
    EntityMixin, HiveMixin, CliqueMixin, CreatedMixin, ListMixin, ScrollItemMixin, OwnedMixin,
    FoundedMixin, ModelMixin, PerksMixin, BoardMixin, WallMixin, MarkMixin, ContributionMixin, AnalyzedMixin
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


class Arena(db.Model, ModelMixin, EntityMixin, HiveMixin):
    __tablename__ = "arena"
    moderators: Mapped[List["Moderator"]] = relationship("Moderator", back_populates="hive")


class Club(
    db.Model, ModelMixin, EntityMixin, HiveMixin, ContributionMixin, MarkMixin, FoundedMixin, OwnedMixin,
    AnalyzedMixin, CreatedMixin
):
    __tablename__ = "clubs"
    __contribution_table__ = club_contributors
    __contribution_backref__ = "club_contributions"
    fandom_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("fandoms.id"), default=None, nullable=False)
    fandom: Mapped["Fandom"] = relationship("Fandom", back_populates="club")
    moderators: Mapped[List["Moderator"]] = relationship("Moderator", back_populates="hive")


class Fandom(
    db.Model, ModelMixin, EntityMixin, HiveMixin, ContributionMixin, MarkMixin, FoundedMixin, AnalyzedMixin,
    CreatedMixin
):
    __tablename__ = "fandoms"
    __contribution_table__ = fandom_contributors
    __contribution_backref__ = "fandom_contributions"
    fans: Mapped[Optional[List["Fan"]]] = relationship("Fan", back_populates="fandom")
    moderators: Mapped[List["Moderator"]] = relationship("Moderator", back_populates="hive")


class Fan(db.Model, ModelMixin, CliqueMixin):
    __tablename__ = "fans"
    fandom_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("fandoms.id"), primary_key=True)
    fan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), primary_key=True)
    fandom: Mapped["Fandom"] = relationship("Fandom", back_populates="fans")
    fan: Mapped["Library"] = relationship("Library", back_populates="fandoms")


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

    __mapper_args__ = {
        "polymorphic_identity": "message",
        "polymorphic_on": type,
    }


class Reply(db.Model, ModelMixin, Message): # TODO: Make reply and message and reaction Polymorphic
    parent_message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("messages.id"), primary_key=True)
    parent_message: Mapped["Message"] = relationship("Message", foreign_keys=[parent_message_id], back_populates="replies")
    reply: Mapped[str] = mapped_column(String(500))

    __mapper_args__ = {
        "polymorphic_identity": "reply",
    }


class Reaction(db.Model, ModelMixin, Message):
    parent_message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("messages.id"), primary_key=True)
    parent_message: Mapped["Message"] = relationship("Message", foreign_keys=[parent_message_id], back_populates="reactions")
    reaction: Mapped[str] = mapped_column(String(100))

    __mapper_args__ = {
        "polymorphic_identity": "reaction",
    }


class Contributor(db.Model, ModelMixin):
    __tablename__ = "contributors"
    contributor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), primary_key=True)
    contributions_fund_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("funds.id"), primary_key=True)
    contribution_type: Mapped[str] = mapped_column(String(100), primary_key=True)
    contributor: Mapped["Library"] = relationship(back_populates="contributions")
    contributions_fund: Mapped["Fund"] = relationship("Fund")


class Subscriber(db.Model, ModelMixin, CliqueMixin):
    __tablename__ = "subscribers"
    tier_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tiers.hive_id"), primary_key=True)
    subscriber_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), primary_key=True)
    tier: Mapped["Tier"] = relationship("Tier", back_populates="subscribers")
    subscriber: Mapped["Library"] = relationship("Library", back_populates="subscriptions")


class Moderator(db.Model, ModelMixin, CliqueMixin):
    __tablename__ = "moderators"
    hive_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    hive: Mapped["HiveMixin"] = relationship(HiveMixin, back_populates="moderators")


class Creator(db.Model, ModelMixin, CliqueMixin):
    creations: Mapped[List["CreatedMixin"]] = relationship("CreatedMixin", back_populates="creators")


class Owner(db.Model, ModelMixin, CliqueMixin):
    holdings: Mapped[List["OwnedMixin"]] = relationship("OwnedMixin", back_populates="owners")


class Founder(db.Model, ModelMixin, CliqueMixin):
    foundlings: Mapped[List["FoundedMixin"]] = relationship("FoundedMixin", back_populates="founders")


class Tier(db.Model, ModelMixin):
    __tablename__ = "tiers"
    hive_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    hive: Mapped["HiveMixin"] = relationship(HiveMixin, back_populates="tiers")
    perks: Mapped[List["PerksMixin"]] = relationship("PerksMixin", back_populates="tier")
    subscribers: Mapped[Optional[List["Subscriber"]]] = relationship("Subscriber", back_populates="tier")
    members: Mapped[Optional[List["Member"]]] = relationship("Member", back_populates="tier")


class Member(db.Model, ModelMixin, CliqueMixin):
    tier_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tiers.hive_id"), primary_key=True)
    member_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), primary_key=True)
    tier: Mapped["Tier"] = relationship("Tier", back_populates="members")
    member: Mapped["Library"] = relationship("Library", back_populates="memberships")


class Watcher(db.Model, ModelMixin, CliqueMixin):
    pass


class Tracker(db.Model, ModelMixin, CliqueMixin):
    pass


class Collector(db.Model, ModelMixin, CliqueMixin):
    pass


class Organizer(db.Model, ModelMixin, CliqueMixin):
    pass


class Reward(db.Model, ModelMixin, PerksMixin):
    pass


class Pins(db.Model, ModelMixin, BoardMixin):
    pass


class Pin(db.Model, ModelMixin):
    __tablename__ = "pins"


class Updates(db.Model, ModelMixin, BoardMixin):
    pass


class Update(db.Model, ModelMixin):
    __tablename__ = "updates"


class Issues(db.Model, ModelMixin, BoardMixin, ListMixin):
    pass


class Issue(db.Model, ModelMixin, ScrollItemMixin):
    pass


class Posts(db.Model, ModelMixin, WallMixin):
    pass


class Post(db.Model, ModelMixin):
    pass


class Clips(db.Model, ModelMixin, WallMixin):
    pass


class Clip(db.Model, ModelMixin):
    pass

