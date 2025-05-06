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
    EntityMixin, HiveMixin, CliqueMixin, ModeratorMixin, CreatorMixin, OwnerMixin, AuthorMixin, ContributionMixin,
    ContributorMixin, ModelMixin, PerksMixin, BoardMixin, EntryMixin, WallMixin, PostMixin, ActionMixin
)

if TYPE_CHECKING:
    from .scrolls import Scroll
    from .library import Library, Shop
    from .journal import Magazine, Article
    from .player import WatchHistory
    from .commerce import Fund, Transaction, Exchange
    from .common import WikiTemplate, DashboardTemplate
    from .calendar import Event, Calendar


class Arena(db.Model, ModelMixin, ContributionMixin, EntityMixin, HiveMixin):
    pass


class Fandom(db.Model, ModelMixin, ContributionMixin, EntityMixin, HiveMixin):
    pass


class Thread(db.Model, ModelMixin, ContributorMixin):
    pass


class Message(db.Model, ModelMixin, ContributionMixin):
    pass


class Reaction(db.Model, ModelMixin, ContributionMixin):
    pass


class Founder(db.Model, ModelMixin, ContributionMixin, CliqueMixin, ModeratorMixin, CreatorMixin):
    pass



class Member(db.Model, ModelMixin, ContributionMixin, CliqueMixin):
    pass


class Subscriber(db.Model, ModelMixin, ContributionMixin, CliqueMixin):
    pass


class Fan(db.Model, ModelMixin, ContributionMixin, CliqueMixin):
    pass


class Watcher(db.Model, ModelMixin, ContributionMixin, CliqueMixin):
    pass


class Creator(db.Model, ModelMixin, ContributionMixin, CliqueMixin, ModeratorMixin, CreatorMixin):
    pass


class Owner(db.Model, ModelMixin, ContributionMixin, CliqueMixin, ModeratorMixin, OwnerMixin):
    pass


class Columnist(db.Model, ModelMixin, ContributionMixin, CliqueMixin, ModeratorMixin, OwnerMixin):
    pass


class Editor(db.Model, ModelMixin, ContributionMixin, CliqueMixin, ModeratorMixin, CreatorMixin, OwnerMixin, AuthorMixin):
    pass


class Writer(db.Model, ModelMixin, ContributionMixin, CliqueMixin, CreatorMixin, OwnerMixin, AuthorMixin):
    pass


class ChiefEditor(db.Model, ModelMixin, ContributionMixin, Editor, CreatorMixin, OwnerMixin, AuthorMixin):
    pass


class Correspondent(db.Model, ModelMixin, ContributionMixin, CliqueMixin, CreatorMixin, OwnerMixin, AuthorMixin):
    pass


class EditorInChief(db.Model, ModelMixin, ContributionMixin, Editor, CreatorMixin, OwnerMixin, AuthorMixin):
    pass


class Analyst(db.Model, ModelMixin, ContributionMixin, CliqueMixin, CreatorMixin, OwnerMixin, AuthorMixin):
    pass


class Reward(db.Model, ModelMixin, ContributionMixin, PerksMixin):
    pass


class Tier(db.Model, ModelMixin, ContributionMixin, PerksMixin):
    pass


class Pins(db.Model, ModelMixin, ContributionMixin, BoardMixin):
    pass


class Pin(db.Model, ModelMixin, ContributionMixin, EntryMixin):
    pass


class Updates(db.Model, ModelMixin, ContributionMixin, BoardMixin):
    pass


class Update(db.Model, ModelMixin, ContributionMixin, EntryMixin):
    pass


class Issues(db.Model, ModelMixin, ContributionMixin, BoardMixin):
    pass


class Issue(db.Model, ModelMixin, ContributionMixin, EntryMixin):
    pass


class Posts(db.Model, ModelMixin, ContributionMixin, WallMixin):
    pass


class Post(db.Model, ModelMixin, ContributionMixin, PostMixin):
    pass


class Clips(db.Model, ModelMixin, ContributionMixin, WallMixin):
    pass


class Clip(db.Model, ModelMixin, ContributionMixin, PostMixin):
    pass


#---------------------------- Actions ------------------------------

class Write(db.Model, ModelMixin, ContributorMixin, ActionMixin):
    pass


class Publish(db.Model, ModelMixin, ContributorMixin, ActionMixin):
    pass


class Review(db.Model, ModelMixin, ContributorMixin, ActionMixin):
    pass


class Follow(db.Model, ModelMixin, ContributorMixin, ActionMixin):
    pass
