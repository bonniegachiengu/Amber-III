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
    ModelMixin, PerksMixin, BoardMixin, EntryMixin, WallMixin, PostMixin, ActionMixin
)

if TYPE_CHECKING:
    from .scrolls import Scroll
    from .library import Library, Shop
    from .journal import Magazine, Article
    from .player import WatchHistory
    from .commerce import Fund, Transaction, Exchange
    from .common import WikiTemplate, DashboardTemplate
    from .calendar import Event, Calendar


class Arena(db.Model, ModelMixin, EntityMixin, HiveMixin):
    pass


class Fandom(db.Model, ModelMixin, EntityMixin, HiveMixin):
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


class Pin(db.Model, ModelMixin, EntryMixin):
    pass


class Updates(db.Model, ModelMixin, BoardMixin):
    pass


class Update(db.Model, ModelMixin, EntryMixin):
    pass


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
