import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, relationships
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from .mixins import ContributionMixin, ModelMixin
from .associations import scroll_contributors

if TYPE_CHECKING:
    from .user import User
    from .library import Portfolio
    from .journal import Magazine, Article
    from .player import WatchHistory
    from .commerce import Fund, Transaction
    from .common import Anchor
    from .calendar import Event, Calendar


class Scroll(db.Model, ModelMixin, ContributionMixin):
    __tablename__ = "scrolls"
    __contribution_table__ = scroll_contributors
    __contribution_backref__ = "scroll_contributions"
    reviewer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), nullable=True)
    reviewer: Mapped["Portfolio"] = relationship(back_populates="reviewed_scrolls")
    # TODO: Something to do with Collector


class ScrollPoints(db.Model, ModelMixin):
    pass


class Position(db.Model, ModelMixin):
    pass
