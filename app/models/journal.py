from uuid import uuid4
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from enum import Enum

from sqlalchemy import String, Boolean, ForeignKey, JSON, Date, Integer, Float, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, relationships
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from .mixins import (
    EntityMixin, HiveMixin, CliqueMixin, ModeratorMixin, CreatorMixin, OwnerMixin, AuthorMixin, ContributionMixin,
    ContributorMixin, ModelMixin, ContentMixin
)


if TYPE_CHECKING:
    from .scrolls import Scroll
    from .user import User
    from .library import Library
    from .player import Bookmark, WatchHistory
    from .community import Reaction, Fandom
    from .calendar import Event, Calendar
    from .commerce import Fund, Transaction, Exchange
    from .common import Genre, Language, Nationality, Country, Keyword, Theme, Tag, Period, WikiTemplate, DashboardTemplate


class Journal(db.Model, ModelMixin, ContributionMixin, EntityMixin, HiveMixin):
    pass

class Magazine(db.Model, ModelMixin, ContributionMixin, EntityMixin, HiveMixin):
    pass

class FrontPage(db.Model, ModelMixin, ContributionMixin):
    pass

class Slot(db.Model, ModelMixin, ContributionMixin):
    pass

class Column(db.Model, ModelMixin, ContributionMixin, EntityMixin, HiveMixin):
    pass

class Article(db.Model, ModelMixin, ContributionMixin, EntityMixin, ContentMixin):
    pass

class Report(db.Model, ModelMixin, ContributionMixin, EntityMixin, ContentMixin):
    pass
