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
    ContributorMixin, ModelMixin, TokenMixin
)


if TYPE_CHECKING:
    from .scrolls import Scroll
    from .user import User
    from .journal import Magazine, Article
    from .player import Bookmark, WatchHistory
    from .community import Reaction, Fandom
    from .calendar import Event, Calendar
    from .library import Library
    from .common import Genre, Language, Nationality, Country, Keyword, Theme, Tag, Period, WikiTemplate, DashboardTemplate


class Market(db.Model, ModelMixin, ContributionMixin, EntityMixin, HiveMixin):
    pass

class Ledger(db.Model, ModelMixin, ContributionMixin, EntityMixin):
    pass

class Currency(db.Model, ModelMixin, ContributionMixin):
    pass

class AmberTokens(db.Model, ModelMixin, ContributionMixin, TokenMixin):
    pass

class CustomToken(db.Model, ModelMixin, ContributionMixin, TokenMixin):
    pass

class Fund(db.Model, ModelMixin, ContributionMixin):
    pass

class Listing(db.Model, ModelMixin, ContributionMixin, EntityMixin):
    pass

class Exchange(db.Model, ModelMixin, ContributionMixin):
    pass

class Transaction(db.Model, ModelMixin, ContributionMixin):
    pass

class Order(db.Model, ModelMixin, ContributionMixin):
    pass

class Discount(db.Model, ModelMixin, ContributionMixin):
    pass

class Receipt(db.Model, ModelMixin, ContributionMixin):
    pass

class Inventory(db.Model, ModelMixin, ContributionMixin):
    pass
