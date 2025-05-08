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
    ContributorMixin, ModelMixin
)

if TYPE_CHECKING:
    from .user import User
    from .library import Library
    from .journal import Magazine, Article
    from .player import WatchHistory
    from .commerce import Fund, Transaction, Exchange
    from .common import Anchor
    from .calendar import Event, Calendar


class Scroll(db.Model, ModelMixin, ContributionMixin):
    pass


class ScrollPoints(db.Model, ModelMixin, ContributionMixin):
    pass


class Position(db.Model, ModelMixin, ContributionMixin):
    pass
