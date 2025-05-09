import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, relationships
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from .mixins import (
    EntityMixin, HiveMixin, CliqueMixin, ModeratorMixin, CreatorMixin, OwnerMixin, AuthorMixin,
    ModelMixin, PerksMixin, BoardMixin, EntryMixin, WallMixin, PostMixin, ActionMixin, ContributionMixin
)

if TYPE_CHECKING:
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
    pass


class Fandom(db.Model, ModelMixin, EntityMixin, HiveMixin, ContributionMixin):
    pass


class Thread(db.Model, ModelMixin):
    pass


class Message(db.Model, ModelMixin):
    pass


class Reaction(db.Model, ModelMixin):
    pass


class Founder(db.Model, ModelMixin, CliqueMixin, ModeratorMixin, CreatorMixin):
    pass



class Member(db.Model, ModelMixin, CliqueMixin):
    pass


class Subscriber(db.Model, ModelMixin, CliqueMixin):
    pass


class Fan(db.Model, ModelMixin, CliqueMixin):
    pass


class Watcher(db.Model, ModelMixin, CliqueMixin):
    pass


class Creator(db.Model, ModelMixin, CliqueMixin, ModeratorMixin, CreatorMixin):
    pass


class Owner(db.Model, ModelMixin, CliqueMixin, ModeratorMixin, OwnerMixin):
    pass

class Organizer(db.Model, ModelMixin, CliqueMixin, ModeratorMixin):
    pass

class Columnist(db.Model, ModelMixin, CliqueMixin, ModeratorMixin, OwnerMixin):
    pass


class Editor(db.Model, ModelMixin, CliqueMixin, ModeratorMixin, CreatorMixin, OwnerMixin, AuthorMixin):
    pass


class Writer(db.Model, ModelMixin, CliqueMixin, CreatorMixin, OwnerMixin, AuthorMixin):
    pass


class ChiefEditor(db.Model, ModelMixin, Editor, CreatorMixin, OwnerMixin, AuthorMixin):
    pass


class Correspondent(db.Model, ModelMixin, CliqueMixin, CreatorMixin, OwnerMixin, AuthorMixin):
    pass


class EditorInChief(db.Model, ModelMixin, Editor, CreatorMixin, OwnerMixin, AuthorMixin):
    pass


class Analyst(db.Model, ModelMixin, CliqueMixin, CreatorMixin, OwnerMixin, AuthorMixin):
    pass


class Reward(db.Model, ModelMixin, PerksMixin):
    pass


class Tier(db.Model, ModelMixin, PerksMixin):
    pass


class Pins(db.Model, ModelMixin, BoardMixin):
    pass


class Pin(db.Model, ModelMixin, EntryMixin, ContributionMixin):
    pass


class Updates(db.Model, ModelMixin, BoardMixin):
    pass


class Update(db.Model, ModelMixin, EntryMixin, ContributionMixin):
    pass


class Issues(db.Model, ModelMixin, BoardMixin):
    pass


class Issue(db.Model, ModelMixin, EntryMixin, ContributionMixin):
    pass


class Posts(db.Model, ModelMixin, WallMixin):
    pass


class Post(db.Model, ModelMixin, PostMixin, ContributionMixin):
    pass


class Clips(db.Model, ModelMixin, WallMixin):
    pass


class Clip(db.Model, ModelMixin, PostMixin, ContributionMixin):
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
