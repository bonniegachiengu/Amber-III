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
    EntityMixin, HiveMixin, CliqueMixin, ModeratorMixin, CreatorMixin, OwnerMixin, AuthorMixin,
    ModelMixin, RecommendationMixin, ExhibitionMixin
)


if TYPE_CHECKING:
    from .scrolls import Scroll
    from .user import User
    from .journal import Magazine, Article
    from .player import Bookmark, WatchHistory
    from .community import Reaction, Fandom
    from .calendar import Event, Calendar
    from .commerce import Fund, Transaction, Exchange
    from .common import Genre, Language, Nationality, Country, Keyword, Theme, Tag, Period, WikiTemplate, DashboardTemplate


class Curator(db.Model, ModelMixin, EntityMixin):
    pass


class Insight(db.Model, ModelMixin):
    pass


class OldGem(db.Model, ModelMixin, RecommendationMixin):
    pass


class NewGem(db.Model, ModelMixin, RecommendationMixin):
    pass


class PopularFilms(db.Model, ModelMixin, ExhibitionMixin):
    pass


class ResumeWatching(db.Model, ModelMixin, ExhibitionMixin):
    pass
