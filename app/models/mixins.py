import uuid
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import String, Boolean, DateTime, ForeignKey, JSONB, Integer, Float, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.schema import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr, backref
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from utils.config import ContentTypeEnum, CliqueTypeEnum, VisibilityEnum, ArticleReportStatusEnum, HiveTypeEnum

if TYPE_CHECKING:
    from .user import User
    from .scrolls import Scroll, ScrollEntry
    from .library import Library, Film, Asset
    from .journal import Analyst
    from .player import WatchHistory
    from .community import Thread, Tier, Creator, Founder, Owner, Moderator, Fandom
    from .commerce import Fund, Transaction, Ledger, Currency, AmberToken
    from .calendar import Event, Calendar, Ticket
    from .common import (
        WikiTemplate, DashboardTemplate, Tag, Keyword, Language, Country, Nationality, Era, Anchor, Theme, Genre,
        Field, Verification, Link, DataSet, Icon, Logo, Image, Avatar, Poster, Video, Figure
    )

def generate_uuid():
    return str(uuid.uuid4())

class ModelMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), default=None, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    deleted_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), default=None)
    wiki_templates: Mapped[Optional[List["WikiTemplate"]]] = relationship(back_populates="model")
    dashboard_templates: Mapped[Optional[List["DashboardTemplate"]]] = relationship(back_populates="model")
    fields: Mapped[Optional[List["Field"]]] = relationship("Field", back_populates="model")
    confidence_score: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    confidence_score_report: Mapped[dict] = mapped_column(JSONB, default={})


class EntityMixin:
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    settings: Mapped[Optional[dict]] = mapped_column(JSONB, default={})
    calendar_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("calendars.id"), default=None, nullable=False)
    calendar: Mapped["Calendar"] = relationship(back_populates="entities", uselist=False)
    verification_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("verifications.id"), default=None, nullable=False)
    verification: Mapped["Verification"] = relationship(back_populates="Entity", uselist=False)
    images: Mapped[Optional[List["Image"]]] = relationship("Image", back_populates="use_cases")
    icons: Mapped[Optional[List["Icon"]]] = relationship("Icon", back_populates="use_cases")
    avatars: Mapped[Optional[List["Avatar"]]] = relationship("Avatar", back_populates="use_cases")
    posters: Mapped[Optional[List["Poster"]]] = relationship("Poster", back_populates="use_cases")
    videos: Mapped[Optional[List["Video"]]] = relationship("Video", back_populates="use_cases")
    figures: Mapped[Optional[List["Figure"]]] = relationship("Figure", back_populates="use_cases")
    links: Mapped[Optional[List["Link"]]] = relationship("Link", back_populates="use_cases")
    logos: Mapped[Optional[List["Logo"]]] = relationship("Logo", back_populates="use_cases")
    backdrops: Mapped[Optional[List["Image"]]] = relationship("Image", back_populates="use_cases")


class ContributionMixin:
    ambertokens_issued: Mapped[List["AmberToken"]] = relationship("AmberToken", back_populates="contributions")
    # noinspection PyMethodParameters
    @declared_attr
    def contributors(cls):
        """
        A declared attribute that dynamically creates a relationship for contributors.

        This attribute establishes a many-to-many relationship between the current
        class and the `Contributor` class using the specified secondary table and backref
        name. The class must define `__contribution_table__` and `__contribution_backref__`
        as attributes to specify the mapping table and the backref configuration,
        respectively. If these attributes are not implemented, an error will be raised.

        :return: A dynamic relationship to `Contributor` using the specified
                 secondary table and backref.
        :rtype: sqlalchemy.orm.RelationshipProperty

        :raises NotImplementedError: If the class does not define both
                                      `__contribution_table__` and
                                      `__contribution_backref__`.
        """
        table = getattr(cls, "__contribution_table__", None)
        backref_name = getattr(cls, "__contribution_backref__", None)

        if not table or not backref_name:
            raise NotImplementedError(
                f"{cls.__name__} must define a __contribution_table__ and __contribution_backref__ class attribute"
            )
        return relationship(
            "Contributor",
            secondary=table,
            backref=backref(backref_name, lazy="dynamic"),
        )


class PeriodMixin:
    start_time: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)


class LibraryMixin:
    libraries: Mapped[List["Library"]] = relationship("Library", back_populates="owner")


class ListMixin:
    scrolls: Mapped[List["Scroll"]] = relationship("Scroll", back_populates="list")


class MarkMixin:
    tags: Mapped[Optional[list["Tag"]]] = relationship("Tag", back_populates="marked")
    keywords: Mapped[Optional[list["Keyword"]]] = relationship("Keyword", back_populates="marked")
    languages: Mapped[Optional[list["Language"]]] = relationship("Language", back_populates="marked")
    themes: Mapped[Optional[list["Theme"]]] = relationship("Theme", back_populates="marked")
    genres: Mapped[Optional[list["Genre"]]] = relationship("Genre", back_populates="marked")
    countries: Mapped[Optional[list["Country"]]] = relationship("Country", back_populates="marked")
    nationalities: Mapped[Optional[list["Nationality"]]] = relationship("Nationality", back_populates="marked")
    eras: Mapped[Optional[list["Era"]]] = relationship("Period", back_populates="marked")
    anchors: Mapped[Optional[list["Anchor"]]] = relationship("Anchor", back_populates="marked")


class CliqueMixin:
    agents: List["User"] = relationship("User", back_populates="cliques")
    clique_type: Mapped[CliqueTypeEnum] = mapped_column(SQLAlchemyEnum(CliqueTypeEnum), nullable=False)
    roles: Mapped[dict] = mapped_column(JSONB, default={})


class HiveMixin(LibraryMixin):
    logo_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("logos.id"), default=None, nullable=False)
    logo: Mapped["Logo"] = relationship(back_populates="use_cases", uselist=False)
    boards: Mapped[List["BoardMixin"]] = relationship("BoardMixin", back_populates="hive")
    walls: Mapped[List["WallMixin"]] = relationship("WallMixin", back_populates="hive")
    join_rules: Mapped[Optional[dict]] = mapped_column(JSONB, default={})
    tiers: Mapped[List["Tier"]] = relationship("Tier", back_populates="hive")


class FanMixin:
    fandom_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("fandoms.id"), default=None)
    fandom: Mapped["Fandom"] = relationship("Fandom", back_populates="entity")


class ContentMixin:
    content_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    content_type: Mapped[ContentTypeEnum] = mapped_column(SQLAlchemyEnum(ContentTypeEnum), nullable=False)


class SharableMixin:
    views: Mapped[int] = mapped_column(Integer, default=0)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    shares: Mapped[int] = mapped_column(Integer, default=0)
    comments: Mapped[int] = mapped_column(Integer, default=0)


class AuthoredMixin:
    publish_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    status: Mapped[ArticleReportStatusEnum] = mapped_column(SQLAlchemyEnum, default=ArticleReportStatusEnum.UNPUBLISHED)
    visibility: Mapped[VisibilityEnum] = mapped_column(SQLAlchemyEnum, default=VisibilityEnum.PUBLIC)
    content: Mapped[str] = mapped_column(Text, nullable=False, info={"rich_text": "ckeditor"})
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    revision_history: Mapped[list[dict]] = mapped_column(JSONB, default=[])
    thread: Mapped["Thread"] = relationship("Thread", back_populates="topic")
    thread_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("threads.id"))


class PerksMixin:
    tiers: Mapped[List["Tier"]] = relationship("Tier", back_populates="perks")


class BoardMixin:
    hive_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    hive: Mapped["HiveMixin"] = relationship(HiveMixin, foreign_keys=[hive_id], back_populates="boards")
    hive_type: Mapped[HiveTypeEnum] = mapped_column(SQLAlchemyEnum(HiveTypeEnum), nullable=False)
    moderators: Mapped[List["Moderator"]] = relationship("Moderator", back_populates="boards")


class WallMixin:
    hive_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    hive: Mapped["HiveMixin"] = relationship(HiveMixin, foreign_keys=[hive_id], back_populates="walls")
    hive_type: Mapped[HiveTypeEnum] = mapped_column(SQLAlchemyEnum(HiveTypeEnum), nullable=False)
    moderators: Mapped[List["Moderator"]] = relationship("Moderator", back_populates="walls")


class WatchListMixin(ListMixin, MarkMixin):
    films: Mapped[List["Film"]] = relationship("Film", back_populates="watchlists")


class ScrollItemMixin:
    scroll_entries: Mapped[List["ScrollEntry"]] = relationship("ScrollEntry", back_populates="scroll_item")
    scrollpoints: Mapped[int] = mapped_column(Integer, default=0)


class MediaMixin:
    keywords: Mapped[Optional[list["Keyword"]]] = relationship("Keyword", back_populates="marked")
    anchors: Mapped[Optional[list["Anchor"]]] = relationship("Anchor", back_populates="marked")
    url: Mapped[str] = mapped_column(String, nullable=False)
    use_cases: Mapped[Optional[List[ModelMixin]]] = relationship("ModelMixin", back_populates="media")
    alt_text: Mapped[Optional[str]] = mapped_column(String)
    asset_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id"))
    asset: Mapped[Optional["Asset"]] = relationship("Asset", back_populates="media")


class ChartMixin:
    data_sets: Mapped[List["DataSet"]] = relationship("DataSet", back_populates="graphs_charts")


class CreatedMixin: # asset, poster
    creators: Mapped[List["Creator"]] = relationship("Creator", back_populates="creations")


class AnalyzedMixin:
    analysts: Mapped[List["Analyst"]] = relationship("Analyst", back_populates="hives")


class FoundedMixin:
    founders: Mapped[List["Founder"]] = relationship("Founder", back_populates="foundlings")


class OwnedMixin:
    owners: Mapped[List["Owner"]] = relationship("Owner", back_populates="holdings")


class PartnerLinksMixin:
    links: Mapped[Optional[List["Link"]]] = relationship("Link", back_populates="partner")
