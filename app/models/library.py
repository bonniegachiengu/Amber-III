from uuid import uuid4
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, Boolean, ForeignKey, JSONB, Date, Integer, Float, Text, ARRAY, Numeric, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from associations import film_contributors, person_contributors, album_contributors, hitlist_contributors
from ..extensions import db
from .utils.config import (
    ExtensionTypeEnum, AlbumTypeEnum, FilmTypeEnum, RelationshipTypeEnum, SubmissionStatusEnum, CrewTypeEnum
)
from .mixins import (
    EntityMixin, HiveMixin, LibraryMixin, ScrollItemMixin, FanMixin, MarkMixin, ModelMixin, WatchListMixin,
    PeriodMixin, ContributionMixin, OwnedMixin, CreatedMixin, PartnerLinksMixin
)


if TYPE_CHECKING:
    from .scrolls import Scroll
    from .user import User
    from .journal import Magazine, Article, Report, Column
    from .community import Fan, Member, Subscriber, Reward
    from .calendar import Calendar, Ticket
    from .player import Bookmark, PlaybackSession, Subtitle
    from .commerce import Listing, Order, Market, Discount, CustomToken, Fund
    from .common import Verification, Preferences, Notification, Link


def generate_uuid():
    return str(uuid4())


class Library(db.Model, ModelMixin, EntityMixin):
    __tablename__ = 'libraries'
    local_libraries: Mapped[List["Library"]] = relationship("Library", back_populates="library", cascade="all, delete-orphan")
    owner: Mapped["LibraryMixin"] = relationship("LibraryMixin", back_populates="libraries", uselist=False)
    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="library", uselist=False, cascade="all, delete-orphan")
    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="library", uselist=False, cascade="all, delete-orphan")
    collections: Mapped[List["Collection"]] = relationship("Collection", back_populates="library", cascade="all, delete-orphan")
    shops: Mapped[List["Shop"]] = relationship("Shop", back_populates="library", cascade="all, delete-orphan")
    markets: Mapped[List["Market"]] = relationship("Market", back_populates="library", cascade="all, delete-orphan")
    watch_history: Mapped[List["WatchHistory"]] = relationship("WatchHistory", back_populates="library", cascade="all, delete-orphan")
    playback_sessions: Mapped[List["PlaybackSession"]] = relationship("PlaybackSession", back_populates="library", cascade="all, delete-orphan")
    preferences: Mapped[List["Preferences"]] = relationship("Preferences", back_populates="library", cascade="all, delete-orphan")
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="recipient", cascade="all, delete-orphan")
    sent_notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="sender", cascade="all, delete-orphan")
    fandoms: Mapped[List["Fan"]] = relationship("Fan", back_populates="library", cascade="all, delete-orphan")
    subscriptions: Mapped[List["Subscriber"]] = relationship("Subscriber", back_populates="library", cascade="all, delete-orphan")
    memberships: Mapped[List["Member"]] = relationship("Member", back_populates="library", cascade="all, delete-orphan")


class Collection(db.Model, ModelMixin):
    __tablename__ = 'collections'
    library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("libraries.id"), nullable=False)
    library: Mapped["Library"] = relationship("library", back_populates="collections")
    collected_albums: Mapped[List["Album"]] = relationship("Album", back_populates="collectors")
    tracked_albums: Mapped[List["Album"]] = relationship("Album", back_populates="trackers")
    collected_films: Mapped[List["Film"]] = relationship("Film", back_populates="collectors")
    tracked_films: Mapped[List["Film"]] = relationship("Film", back_populates="trackers")
    collected_hitlists: Mapped[List["Hitlist"]] = relationship("Hitlist", back_populates="collectors")
    tracked_hitlists: Mapped[List["Hitlist"]] = relationship("Hitlist", back_populates="trackers")


class Portfolio(db.Model, ModelMixin):
    __tablename__ = "portfolios"
    library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("libraries.id"), nullable=False)
    library: Mapped["Library"] = relationship(back_populates="portfolio")
    created_magazines: Mapped[List["Magazine"]] = relationship("Magazine", back_populates="founders") # founder
    authored_articles: Mapped[List["Article"]] = relationship("Article", back_populates="authors") # writer
    authored_reports: Mapped[List["Report"]] = relationship("Report", back_populates="authors") # analyst
    maintained_columns: Mapped[List["Column"]] = relationship("Column", back_populates="maintainers")
    reviewed_scrolls: Mapped[List["Scroll"]] = relationship("Scroll", back_populates="reviewer")
    distributed_albums: Mapped[List["Album"]] = relationship("Album", back_populates="distributors")
    distributed_films: Mapped[List["Film"]] = relationship("Film", back_populates="distributors")
    nominations: Mapped[List["Nomination"]] = relationship('Nomination', back_populates='nominees')
    wins: Mapped[list["Win"]] = relationship('Win', back_populates='winners')

    created_people: Mapped[List["Person"]] = relationship("Person", back_populates="creators")
    assets: Mapped[List["Asset"]] = relationship("Asset", back_populates="portfolio")
    owned_magazines: Mapped[List["Magazine"]] = relationship("Magazine", back_populates="owners") # owner
    owned_albums: Mapped[List["Album"]] = relationship("Album", back_populates="studios")
    owned_films: Mapped[List["Film"]] = relationship("Film", back_populates="studios")
    owned_hitlists: Mapped[List["Hitlist"]] = relationship("Hitlist", back_populates="creators")
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="buyer_portfolio")
    customtokens: Mapped[List["CustomToken"]] = relationship("CustomToken", back_populates="creator_portfolio")
    created_tickets: Mapped[List["Ticket"]] = relationship("Ticket", back_populates="creator_portfolio")
    bought_tickets: Mapped[List["Ticket"]] = relationship("Ticket", back_populates="buying_portfolios")
    verifications: Mapped[List["Verification"]] = relationship("Verification", back_populates="verifiers")



class WatchHistory(db.Model, ModelMixin):
    __tablename__ = "watch_histories"
    library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("libraries.id"), nullable=False)
    library: Mapped["Library"] = relationship(back_populates="watch_history")
    film_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("films.id"), nullable=False)
    film: Mapped["Film"] = relationship("Film", back_populates="watch_histories")
    watch_count: Mapped[int] = mapped_column(Integer, default=0)
    current_position: Mapped[float] = mapped_column(Float, default=0.0) # seconds
    last_watched: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)
    bookmarks: Mapped[List["Bookmark"]] = relationship(back_populates="watch_history")


class Film(db.Model, ModelMixin, EntityMixin, ContributionMixin, ScrollItemMixin, MarkMixin, FanMixin):
    __tablename__ = "films"
    __contribution_table__ = film_contributors
    __contribution_back_populates__ = "film_contributions"
    # Amber Film aspects
    title: Mapped[str] = mapped_column(String, nullable=False)
    original_title: Mapped[Optional[str]] = mapped_column(String)
    release_date: Mapped[Optional[datetime]] = mapped_column(Date)
    release_year: Mapped[Optional[int]] = mapped_column(Integer)
    runtime: Mapped[Optional[int]] = mapped_column(Integer)
    tagline: Mapped[Optional[str]] = mapped_column(String)
    synopsis: Mapped[Optional[str]] = mapped_column(Text)
    available_locally: Mapped[bool] = mapped_column(Boolean, default=False)
    submission_status: Mapped[SubmissionStatusEnum] = mapped_column(SQLAlchemyEnum(SubmissionStatusEnum), default=SubmissionStatusEnum.PENDING)
    # Relationships
    subtitles: Mapped[Optional[List["Subtitle"]]] = relationship("Subtitle", back_populates="film")
    watch_histories: Mapped[List["WatchHistory"]] = relationship("WatchHistory", back_populates="film")
    files: Mapped[List["File"]] = relationship("File", back_populates="film")
    streaming_links: Mapped[Optional[List[Link]]] = mapped_column("Link")
    trailer_links: Mapped[Optional[List[Link]]] = mapped_column("Link")
    nominations: Mapped[List["Nomination"]] = relationship('Nomination', back_populates='film')
    wins: Mapped[List["Win"]] = relationship('Win', back_populates='film')
    boxoffice: Mapped["BoxOffice"] = relationship("BoxOffice", back_populates="film")
    production_companies: Mapped[List["ProductionCompany"]] = relationship("ProductionCompany", back_populates="films")
    studios: Mapped[List["Studio"]] = relationship('Studio', back_populates='films')
    albums: Mapped[List["Album"]] = relationship('Album', back_populates='films')
    collectors: Mapped[List['Collection']] = relationship('Collection', back_populates='collected_films')
    trackers: Mapped[List['Collection']] = relationship('Collection', back_populates='tracked_films')
    distributors: Mapped[List['Portfolio']] = relationship('Portfolio', back_populates="distributed_films")
    characters: Mapped[List["Character"]] = relationship("Character", back_populates="films")
    gigs: Mapped[List["Gig"]] = relationship("Gig", back_populates="films")
    inspirations: Mapped[List["Inspiration"]] = relationship("Inspiration", back_populates="films")
    # External stats
    imdb_id: Mapped[Optional[str]] = mapped_column(String)
    tmdb_id: Mapped[Optional[int]] = mapped_column(Integer)
    imdb_rating: Mapped[Optional[float]] = mapped_column(Float)
    imdb_votes: Mapped[Optional[int]] = mapped_column(Integer)
    tmdb_rating: Mapped[Optional[float]] = mapped_column(Float)
    tmdb_votes: Mapped[Optional[int]] = mapped_column(Integer)
    rotten_tomatoes_rating: Mapped[Optional[float]] = mapped_column(Float)
    metascore: Mapped[Optional[int]] = mapped_column(Integer)
    awards_string: Mapped[Optional[str]] = mapped_column(String)
    # External data
    imdb_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    tmdb_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    omdb_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    # Amber aspects
    contributor_amber_points: Mapped[float] = mapped_column(Float, default=0.0)
    popularity_score: Mapped[float] = mapped_column(Float, default=0.0)
    total_watch_count: Mapped[int] = mapped_column(Integer, default=0)
    total_scroll_reviews: Mapped[int] = mapped_column(Integer, default=0)
    scroll_stats: Mapped[Optional[dict]] = mapped_column(JSONB, default={})
    film_type: Mapped[FilmTypeEnum] = mapped_column(SQLAlchemyEnum(FilmTypeEnum), nullable=False)


class Album(db.Model, ModelMixin, WatchListMixin, EntityMixin):
    __tablename__ = 'albums'
    __contribution_table = album_contributors
    __contribution_back_populates = "album_contributions"
    album_type: Mapped[AlbumTypeEnum] = relationship(SQLAlchemyEnum(AlbumTypeEnum), nullable=False)
    films: Mapped[List["Film"]] = relationship('Film', back_populates='albums')
    collectors: Mapped[List['Collection']] = relationship('Collection', back_populates='collected_albums')
    trackers: Mapped[List['Collection']] = relationship('Collection', back_populates='tracked_albums')
    distributors: Mapped[List['Portfolio']] = relationship('Portfolio', back_populates="distributed_albums")
    boxoffice: Mapped[Optional["BoxOffice"]] = relationship("BoxOffice", back_populates="album")
    studios: Mapped[List["Studio"]] = relationship('Studio', back_populates='albums')
    inspirations: Mapped[List["Inspiration"]] = relationship("Inspiration", back_populates="albums")


class Hitlist(db.Model, ModelMixin, WatchListMixin, EntityMixin):
    __tablename__ = 'hitlists'
    __contribution_table = hitlist_contributors
    __contribution_back_populates = "hitlist_contributions"
    collectors: Mapped[List['Collection']] = relationship('Collection', back_populates='collected_hitlists')
    trackers: Mapped[List['Collection']] = relationship('Collection', back_populates='tracked_hitlists')
    films: Mapped[List["Film"]] = relationship('Film', back_populates='hitlists')


class Person(db.Model, ModelMixin, EntityMixin, ContributionMixin, FanMixin, MarkMixin):
    __tablename__ = 'people'
    __contribution_table__ = person_contributors
    __contribution_back_populates__ = "person_contributions"
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String)
    aliases: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    date_of_birth: Mapped[Optional[datetime]] = mapped_column(Date)
    date_of_death: Mapped[Optional[datetime]] = mapped_column(Date, default=None)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    is_linked: Mapped[bool] = mapped_column(Boolean, default=False)
    claimed_by_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('users.id'))
    claimed_by: Mapped[Optional["User"]] = relationship('User', back_populates='claimed_person')
    profession_summary: Mapped[Optional[str]] = mapped_column(String)
    contributors: Mapped[List["User"]] = relationship('User', back_populates='contributions')
    careers: Mapped[List["Career"]] = relationship('Career', back_populates='person')
    relationships: Mapped[List["Relationship"]] = relationship('Relationship', back_populates='person')
    creators: Mapped[List["Portfolio"]] = relationship('Portfolio', back_populates='created_people')


class Career(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "careers"
    person_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=False)
    person: Mapped["Person"] = relationship("Person", back_populates="careers")
    characters: Mapped[Optional[List["Character"]]] = relationship("Character", back_populates="career", cascade="all, delete-orphan")
    gigs: Mapped[Optional[List["Gig"]]] = relationship("Gig", back_populates="career", cascade="all, delete-orphan")


class Gig(db.Model, ModelMixin, PeriodMixin):
    __tablename__ = "gigs"
    career_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("careers.id"), nullable=False)
    crew_type: Mapped[CrewTypeEnum] = mapped_column(SQLAlchemyEnum(CrewTypeEnum), nullable=False)
    episodes: Mapped[List["Film"] | None] = mapped_column(ARRAY(UUID(as_uuid=True)), default=list)
    notes: Mapped[str | None] = mapped_column(db.Text, nullable=True)
    is_primary_credit: Mapped[bool] = mapped_column(db.Boolean, default=False)
    career: Mapped["Career"] = relationship("Career", back_populates="gigs")
    films: Mapped["Film"] = relationship("Film", back_populates="gigs")


class Character(db.Model, ModelMixin, EntityMixin, PeriodMixin):
    __tablename__ = "characters"
    aliases: Mapped[list[str]] = mapped_column(ARRAY(db.String), default=list)
    career_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("careers.id"), nullable=False)
    start_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    episodes: Mapped[List["Film"] | None] = mapped_column(ARRAY(UUID(as_uuid=True)), default=list)
    notes: Mapped[str | None] = mapped_column(db.Text, nullable=True)
    career: Mapped["Career"] = relationship("Career", back_populates="characters")
    films: Mapped["Film"] = relationship("Film", back_populates="characters")


class Relationship(db.Model, ModelMixin):
    __tablename__ = "relationships"
    person_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=False)
    related_person_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=False)
    relationship_type: Mapped[RelationshipTypeEnum] = mapped_column(SQLAlchemyEnum(RelationshipTypeEnum), nullable=False)
    start_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    person = relationship("Person", foreign_keys=[person_id], back_populates="relationships")
    related_person = relationship("Person", foreign_keys=[related_person_id], back_populates="relationships")


class Shop(db.Model, ModelMixin, EntityMixin, HiveMixin):
    __tablename__ = "shops"
    library: Mapped["Library"] = relationship("Library", back_populates="shops")
    merchandise: Mapped[List["Merchandise"]] = relationship("Merchandise", back_populates="shop")


class Asset(db.Model, ModelMixin, EntityMixin, CreatedMixin, OwnedMixin):
    __tablename__ = "assets"
    portfolio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("portfolios.id"), nullable=False)
    token_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("customtokens.id"), nullable=False)
    merchandise_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("merchandises.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    customtoken: Mapped["CustomToken"] = relationship("CustomToken", back_populates="asset")
    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="assets")
    merchandise: Mapped["Merchandise"] = relationship("Merchandise", back_populates="asset")


class Merchandise(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "merchandises"
    asset_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("assets.id"), nullable=False)
    shop_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("shops.id"), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    inventory_count: Mapped[int] = mapped_column(Integer, default=0)
    inventory_limit: Mapped[int] = mapped_column(Integer, default=0)
    asset: Mapped["Asset"] = relationship("Asset", back_populates="merchandise")
    shop: Mapped["Shop"] = relationship("Shop", back_populates="merchandise")
    listings: Mapped[List["Listing"]] = relationship("Listing", back_populates="merchandise")
    discounts: Mapped[List["Discount"]] = relationship("Discount", back_populates="merchandise")


class Wallet(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "wallets"
    library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("libraries.id"), nullable=False)
    library: Mapped["Library"] = relationship(back_populates="wallet")
    funds: Mapped["Fund"] = relationship("Fund", back_populates="wallet")


class Accolade(db.Model, ModelMixin):
    __tablename__ = "accolades"
    title: Mapped[str] = mapped_column(String, nullable=False)
    calendar: Mapped["Calendar"] = relationship(back_populates="owner")
    wins: Mapped[list["Win"]] = relationship('Win', back_populates='accolade')


class Condition(db.Model, ModelMixin):
    __tablename__ = "conditions"


class Partners(db.Model, ModelMixin):
    __tablename__ = "partners"
    streaming_platforms: Mapped[List["StreamingPlatform"]] = relationship("StreamingPlatform")
    peers_platforms: Mapped[List["PeersPlatform"]] = relationship("PeersPlatform")
    social_platforms: Mapped[List["SocialPlatform"]] = relationship("SocialPlatform")
    websites: Mapped[List["Website"]] = relationship("Website")
    distributors: Mapped[List["Distributor"]] = relationship("Distributor")
    theatres: Mapped[List["Theatre"]] = relationship("Theatre")
    the_box_office_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("theboxoffices.id"), nullable=True)
    the_box_office: Mapped["TheBoxOffice"] = relationship("TheBoxOffice")
    studios: Mapped[List["Studio"]] = relationship("Studio")
    production_companies: Mapped[List["ProductionCompany"]] = relationship("ProductionCompany")


class ProductionCompany(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    __tablename__ = "production_companies"
    films: Mapped[List["Film"]] = relationship("Film", back_populates="production_companies")


class Studio(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    __tablename__ = "studios"
    films: Mapped[List["Film"]] = relationship("Film", back_populates="studios")
    albums: Mapped[List["Album"]] = relationship("Album", back_populates="studios")


class StreamingPlatform(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    __tablename__ = "streaming_platforms"


class PeersPlatform(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    __tablename__ = "peers_platforms"


class SocialPlatform(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    __tablename__ = "social_platforms"


class Website(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    __tablename__ = "websites"


class Distributor(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    __tablename__ = "distributors"


class Theatre(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    __tablename__ = "theatres"


class TheBoxOffice(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    __tablename__ = "theboxoffices"
    boxoffices: Mapped[List["BoxOffice"]] = relationship("BoxOffice", back_populates="theboxoffice")


class BoxOffice(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "boxoffices"
    film_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("films.id"), nullable=False)
    film: Mapped["Film"] = relationship("Film", back_populates="boxoffice")
    album_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("albums.id"), nullable=False)
    album: Mapped["Album"] = relationship("Album", back_populates="boxoffice")
    budget: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    revenue: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    theboxoffice_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("theboxoffices.id"), nullable=False)
    theboxoffice: Mapped["TheBoxOffice"] = relationship("TheBoxOffice", back_populates="boxoffices")


class AwardType(db.Model, ModelMixin, EntityMixin, PartnerLinksMixin):
    __tablename__ = "award_types"


class Award(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "awards"


class Win(db.Model, ModelMixin, EntityMixin, PeriodMixin):
    __tablename__ = "wins"
    reward_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("rewards.id"), nullable=True)
    reward: Mapped["Reward"] = relationship("Reward", back_populates="wins")
    award_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("awards.id"), nullable=True)
    award: Mapped["Award"] = relationship("Award", back_populates="nominations")
    accolade_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("accolades.id"), nullable=True)
    accolade: Mapped["Accolade"] = relationship("Accolade", back_populates="wins")
    film_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("films.id"), nullable=True)
    film: Mapped["Film"] = relationship("Film", back_populates="wins")
    album_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("albums.id"), nullable=True)
    album: Mapped["Album"] = relationship("Album", back_populates="wins")
    hitlist_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("hitlists.id"), nullable=True)
    hitlist: Mapped["Hitlist"] = relationship("Hitlist", back_populates="wins")
    person_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=True)
    person: Mapped["Person"] = relationship("Person", back_populates="wins")
    winners: Mapped[List["Portfolio"]] = relationship(back_populates="wins")


class Nomination(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "nominations"
    reward_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("rewards.id"), nullable=True)
    reward: Mapped["Reward"] = relationship("Reward", back_populates="wins")
    award_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("awards.id"), nullable=True)
    award: Mapped["Award"] = relationship("Award", back_populates="nominations")
    accolade_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("accolades.id"), nullable=True)
    accolade: Mapped["Accolade"] = relationship("Accolade", back_populates="wins")
    film_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("films.id"), nullable=True)
    film: Mapped["Film"] = relationship("Film", back_populates="wins")
    album_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("albums.id"), nullable=True)
    album: Mapped["Album"] = relationship("Album", back_populates="wins")
    hitlist_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("hitlists.id"), nullable=True)
    hitlist: Mapped["Hitlist"] = relationship("Hitlist", back_populates="wins")
    person_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=True)
    person: Mapped["Person"] = relationship("Person", back_populates="wins")
    nominees: Mapped[List["Portfolio"]] = relationship(back_populates="nominations")


class Inspiration(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "inspirations"
    films: Mapped[List["Film"]] = relationship("Film", back_populates="inspirations")
    albums: Mapped[List["Album"]] = relationship("Album", back_populates="inspirations")
    inspiration_source_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("inspiration_sources.id"), nullable=False)
    inspiration_source: Mapped["InspirationSource"] = relationship("InspirationSource", back_populates="inspirations")


class InspirationSource(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "inspiration_sources"
    inspirations: Mapped[List["Inspiration"]] = relationship("Inspiration", back_populates="inspiration_source")


class Release(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "releases"


class LocalLibrary(db.Model, ModelMixin):
    __tablename__ = "local_libraries"
    library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("libraries.id"))
    library: Mapped["Library"] = relationship("Library", back_populates="local_libraries")
    directories: Mapped[List["Directory"]] = relationship("Directory", back_populates="local_library")
    path: Mapped[str] = mapped_column(String, nullable=False)


class Directory(db.Model, ModelMixin):
    __tablename__ = "directories"
    local_library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("local_libraries.library_id"))
    local_library: Mapped["Library"] = relationship("Library", back_populates="directories")
    files: Mapped[List["File"]] = relationship("File", back_populates="directory")
    path: Mapped[str] = mapped_column(String, nullable=False)


class File(db.Model, ModelMixin):
    __tablename__ = "files"
    filepath: Mapped[str] = mapped_column(String, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    file_title: Mapped[str] = mapped_column(String, nullable=False)
    file_year: Mapped[Optional[int]] = mapped_column(Integer)
    file_resolution: Mapped[Optional[str]] = mapped_column(String)
    file_extension: Mapped[ExtensionTypeEnum] = mapped_column(SQLAlchemyEnum(ExtensionTypeEnum), nullable=False)
    file_codec: Mapped[Optional[str]] = mapped_column(String)
    file_bitrate: Mapped[Optional[int]] = mapped_column(Integer)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    directory_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("directories.id"))
    file_tag_set_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("file_tag_sets.id"))
    directory: Mapped["Directory"] = relationship("Directory", back_populates="files")
    file_tag_set: Mapped["FileTagSet"] = relationship("FileTagSet", back_populates="file")
    is_film: Mapped[bool] = mapped_column(Boolean, default=False)
    is_subtitle: Mapped[bool] = mapped_column(Boolean, default=False)
    is_media: Mapped[bool] = mapped_column(Boolean, default=False)
    film_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), db.ForeignKey("films.id"))
    film: Mapped["Film"] = relationship("Film", back_populates="files")


class FileTagSet(db.Model, ModelMixin):
    __tablename__ = "file_tag_sets"
    file_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("files.id"))
    film_directory_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("directories.id"))
    file: Mapped["File"] = relationship("File", back_populates="file_tag_set")
    film_directory: Mapped["Directory"] = relationship("Directory", foreign_keys=[film_directory_id])
    root_tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    type_tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    cate_genres: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    album_tags: Mapped[Optional[List[Album]]] = relationship("Album")
    studio_tags: Mapped[Optional[List[Studio]]] = relationship("Studio")
