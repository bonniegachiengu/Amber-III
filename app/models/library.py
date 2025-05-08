from uuid import uuid4
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, Boolean, ForeignKey, JSON, Date, Integer, Float, Text, ARRAY, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from utils.config import FilmType, RelationshipType, SubmissionStatus
from ..extensions import db
from .mixins import (
    EntityMixin, HiveMixin, LibraryMixin,
    ModelMixin, WatchListMixin, PartnerMixin, AwardMixin, AwardTypeMixin, EraMixin
)


if TYPE_CHECKING:
    from .scrolls import Scroll
    from .user import User
    from .journal import Magazine, Article
    from .community import Fandom
    from .calendar import Calendar, Ticket
    from .player import Bookmark, PlaybackSession
    from .commerce import Listing, Order, Market, Discount, CustomToken
    from .common import Genre, Language, Country, Keyword, Theme, Tag, Period, WikiTemplate, DashboardTemplate


def generate_uuid():
    return str(uuid4())


class Library(db.Model, ModelMixin, EntityMixin):
    __tablename__ = 'libraries'
    owner: Mapped["LibraryMixin"] = relationship("LibraryMixin" ,back_populates="libraries", uselist=False)
    wallet: Mapped["Wallet"] = relationship(back_populates="library", uselist=False, cascade="all, delete-orphan")
    portfolio: Mapped["Portfolio"] = relationship(back_populates="library", uselist=False, cascade="all, delete-orphan")
    collections: Mapped[List["Collection"]] = relationship(back_populates="library", cascade="all, delete-orphan")
    shops: Mapped[List["Shop"]] = relationship(back_populates="library", cascade="all, delete-orphan")
    markets: Mapped[List["Market"]] = relationship(back_populates="library", cascade="all, delete-orphan")
    watch_history: Mapped[List["WatchHistory"]] = relationship(back_populates="library", cascade="all, delete-orphan")
    playback_sessions: Mapped[List["PlaybackSession"]] = relationship(back_populates="library", cascade="all, delete-orphan")


class Collection(db.Model, ModelMixin):
    __tablename__ = 'collections'
    library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("libraries.id"), nullable=False)
    library: Mapped["Library"] = relationship(back_populates="collections")
    collected_albums: Mapped[List["Album"]] = relationship(backref="collectors")
    tracked_albums: Mapped[List["Album"]] = relationship(back_populates="trackers")
    collected_films: Mapped[List["Film"]] = relationship(back_populates="collectors")
    tracked_films: Mapped[List["Film"]] = relationship(back_populates="trackers")
    collected_hitlists: Mapped[List["Hitlist"]] = relationship(back_populates="collectors")
    tracked_hitlists: Mapped[List["Hitlist"]] = relationship(back_populates="trackers")
    distributed_films: Mapped[List["Film"]] = relationship(back_populates="distributors")


class Portfolio(db.Model, ModelMixin):
    __tablename__ = "portfolios"
    library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("libraries.id"), nullable=False)
    library: Mapped["Library"] = relationship(back_populates="portfolio")
    career: Mapped["Career"] = relationship(back_populates="portfolio")
    created_magazines: Mapped[List["Magazine"]] = relationship(back_populates="creator_portf")
    authored_articles: Mapped[List["Article"]] = relationship(back_populates="authors")
    ranked_scrolls: Mapped[List["Scroll"]] = relationship(back_populates="users")
    created_people: Mapped[List["Person"]] = relationship(back_populates="creator")
    assets: Mapped[List["Asset"]] = relationship(back_populates="portfolio")
    own_albums: Mapped[List["Album"]] = relationship(back_populates="creator")
    own_films: Mapped[List["Film"]] = relationship(back_populates="studios")
    own_hitlists: Mapped[List["Hitlist"]] = relationship(back_populates="creator")
    orders: Mapped[List["Order"]] = relationship(back_populates="buyer_portfolio")
    customtokens: Mapped[List["CustomToken"]] = relationship(back_populates="creator_portfolio")
    created_tickets: Mapped[List["Ticket"]] = relationship(back_populates="creator_portfolio")
    bought_tickets: Mapped[List["Ticket"]] = relationship(back_populates="buying_portfolios")


class WatchHistory(db.Model, ModelMixin):
    __tablename__ = "watch_histories"
    library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("libraries.id"), nullable=False)
    library: Mapped["Library"] = relationship(back_populates="watch_history")
    bookmarks: Mapped[List["Bookmark"]] = relationship(back_populates="watch_history")


class Film(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "films"
    __contribution_table__ = film_contributors
    __contribution_backref__ = "film_contributions"
    title: Mapped[str] = mapped_column(String, nullable=False)
    original_title: Mapped[Optional[str]] = mapped_column(String)
    release_date: Mapped[Optional[datetime]] = mapped_column(Date)
    runtime: Mapped[Optional[int]] = mapped_column(Integer)
    synopsis: Mapped[Optional[str]] = mapped_column(Text)
    poster_url: Mapped[Optional[str]] = mapped_column(String)
    backdrop_url: Mapped[Optional[str]] = mapped_column(String)
    available_locally: Mapped[bool] = mapped_column(Boolean, default=False)
    streaming_links: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    trailer_url: Mapped[Optional[str]] = mapped_column(String)
    local_file_url: Mapped[Optional[str]] = mapped_column(String)
    watch_count: Mapped[int] = mapped_column(Integer, default=0)
    average_progress: Mapped[float] = mapped_column(Float, default=0.0)
    popularity_score: Mapped[float] = mapped_column(Float, default=0.0)
    scroll_stats: Mapped[Optional[dict]] = mapped_column(JSON, default={})
    viewer_tags: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    subtitles: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))

    contributed_by_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('users.id'))

    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)

    contributor_amber_points: Mapped[float] = mapped_column(Float, default=0.0)

    submission_status: Mapped[SubmissionStatus] = mapped_column(db.Enum(SubmissionStatus), default=SubmissionStatus.PENDING)
    edit_history: Mapped[Optional[list[UUID]]] = mapped_column(ARRAY(UUID(as_uuid=True)))
    imdb_id: Mapped[Optional[str]] = mapped_column(String)
    tmdb_id: Mapped[Optional[int]] = mapped_column(Integer)
    imdb_rating: Mapped[Optional[float]] = mapped_column(Float)
    imdb_votes: Mapped[Optional[int]] = mapped_column(Integer)
    tmdb_rating: Mapped[Optional[float]] = mapped_column(Float)
    tmdb_votes: Mapped[Optional[int]] = mapped_column(Integer)
    rotten_tomatoes_rating: Mapped[Optional[float]] = mapped_column(Float)
    metascore: Mapped[Optional[int]] = mapped_column(Integer)
    awards_string: Mapped[Optional[str]] = mapped_column(String)

    content_rating: Mapped[Optional[str]] = mapped_column(String)
    budget: Mapped[Optional[int]] = mapped_column(Integer)
    revenue: Mapped[Optional[int]] = mapped_column(Integer)
    tagline: Mapped[Optional[str]] = mapped_column(String)
    box_office: Mapped[Optional[str]] = mapped_column(String)
    production_companies: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    spoken_languages: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    country_of_origin: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    imdb_data: Mapped[Optional[dict]] = mapped_column(JSON)
    tmdb_data: Mapped[Optional[dict]] = mapped_column(JSON)
    film_type: Mapped[FilmType] = mapped_column(db.Enum(FilmType), nullable=False)

    # Relationships # TODO: Review the Backrefs after creating models
    film_contributions: Mapped[list["Film"]] = relationship(secondary="film_contributors", backref="contributors")
    tags: Mapped[List["Tag"]] = relationship('Tag', backref='films')
    genres: Mapped[List["Genre"]] = relationship('Genre', backref='films')
    themes: Mapped[List["Theme"]] = relationship('Theme', backref='films')
    keywords: Mapped[List["Keyword"]] = relationship('Keyword', backref='films')
    studios: Mapped[List["Studio"]] = relationship('Studio', backref='films')
    languages: Mapped[List["Language"]] = relationship('Language', backref='films')
    countries: Mapped[List["Country"]] = relationship('Country', backref='films')
    periods: Mapped[List["Period"]] = relationship('Period', backref='films')
    careers: Mapped[List["Career"]] = relationship("Career", back_populates="film", cascade="all, delete-orphan")
    albums: Mapped[List["Album"]] = relationship('Album', backref='films')
    wins: Mapped[list["Win"]] = relationship('Win', backref='film')

    nominations: Mapped[List["Nomination"]] = relationship('Nomination', backref='film')


    collectors: Mapped[List['Collection']] = relationship('Collection', backref='collected_films')
    trackers: Mapped[List['Collection']] = relationship('Collection', backref='tracked_films')
    distributors: Mapped[List['Collection']] = relationship('Collection', backref="distributed_films")

    def __repr__(self):
        return f"<Film {self.title} ({self.release_date})>"

    def to_dict(self):
        return {

        }


class Album(db.Model, ModelMixin, WatchListMixin, EntityMixin):
    # __tablename__ = 'albums'
    #
    # id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    # title: Mapped[str] = mapped_column(String, nullable=False)
    # description: Mapped[Optional[str]] = mapped_column(Text)

    # Relationships
    films: Mapped[List["Film"]] = relationship('Film', backref='albums')

    def __repr__(self):
        return f"<Album {self.title}>"


class Hitlist(db.Model, ModelMixin, WatchListMixin, EntityMixin):
    pass


class Person(db.Model, ModelMixin, EntityMixin):
    # __tablename__ = 'people'
    # id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    # first_name: Mapped[str] = mapped_column(String, nullable=False)
    # last_name: Mapped[str] = mapped_column(String, nullable=False)
    # full_name: Mapped[Optional[str]] = mapped_column(String)
    # date_of_birth: Mapped[Optional[datetime]] = mapped_column(Date)
    # date_of_death: Mapped[Optional[datetime]] = mapped_column(Date, default=None)
    # avatar_url: Mapped[Optional[str]] = mapped_column(String)
    # bio: Mapped[Optional[str]] = mapped_column(Text)
    # nationality: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    # is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    # is_linked: Mapped[bool] = mapped_column(Boolean, default=False)
    # confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    # profession_summary: Mapped[Optional[str]] = mapped_column(String)
    # # TODO: Review the Backrefs after creating models
    # contributors: Mapped[List["User"]] = relationship('User', backref='contributions')
    # careers: Mapped[List["Career"]] = relationship('Career', back_populates='person')
    # relationships: Mapped[List["Relationship"]] = relationship('Relationship', back_populates='person')
    # fandoms: Mapped[List["Fandom"]] = relationship('Fandom', back_populates='members')
    # calendar: Mapped[Optional["Calendar"]] = relationship('Calendar', back_populates='person', uselist=False)
    # wiki: Mapped[Optional["WikiTemplate"]] = relationship('Wiki', back_populates='person', uselist=False)
    # dashboard: Mapped[Optional["DashboardTemplate"]] = relationship('Dashboard', back_populates='person', uselist=False)
    # created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)
    # updated_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    pass

    def __repr__(self):
        return f"<Person {self.full_name or f'{self.first_name} {self.last_name}'} {self.profession_summary}>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "date_of_death": self.date_of_death.isoformat() if self.date_of_death else None,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "nationality": self.nationality,
            "is_verified": self.is_verified,
            "is_linked": self.is_linked,
            "confidence_score": self.confidence_score,
            "profession_summary": self.profession_summary,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Career(db.Model, ModelMixin, EntityMixin):
    # __tablename__ = "careers"
    # id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # person_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=False)
    # # Relationships
    # person: Mapped["Person"] = relationship("Person", back_populates="careers")
    # characters: Mapped[List["Character"]] = relationship("Character", back_populates="career", cascade="all, delete-orphan")
    # gigs: Mapped[List["Gig"]] = relationship("Gig", back_populates="career", cascade="all, delete-orphan")
    # wiki: Mapped[Optional["WikiTemplate"]] = relationship('Wiki', back_populates='career', uselist=False)
    pass


    def __repr__(self):
        return f"<Career {self.id} for Person {self.person_id}>"

    def to_dict(self):
        return {
        }


class Gig(db.Model, ModelMixin):
    # __tablename__ = "gigs"
    # id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # film_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("films.id"), nullable=False)
    # career_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("careers.id"), nullable=False)
    # job_title: Mapped[str] = mapped_column(db.String(128), nullable=False)
    # start_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    # end_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    # episodes: Mapped[int | None] = mapped_column(db.Integer, nullable=True)
    # notes: Mapped[str | None] = mapped_column(db.Text, nullable=True)
    # is_primary_credit: Mapped[bool] = mapped_column(db.Boolean, default=False)
    # # TODO: Review these relationships
    # career = relationship("Career", back_populates="gigs")
    # film = relationship("Film", back_populates="gigs")
    pass

    def __repr__(self):
        return f"<Gig {self.job_title} in Film {self.film_id} by Career {self.career_id}>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "film_id": str(self.film_id),
            "career_id": str(self.career_id),
            "job_title": self.job_title,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "episodes": self.episodes,
            "notes": self.notes,
            "is_primary_credit": self.is_primary_credit
        }


class Character(db.Model, ModelMixin, EntityMixin):
    # __tablename__ = "characters"
    # id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # name: Mapped[str] = mapped_column(db.String(128), nullable=False)
    # aliases: Mapped[list[str]] = mapped_column(ARRAY(db.String), default=list)
    # description: Mapped[str | None] = mapped_column(db.Text, nullable=True)
    # film_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("films.id"), nullable=False)
    # career_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("careers.id"), nullable=False)
    # start_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    # end_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    # episodes: Mapped[int | None] = mapped_column(db.Integer, nullable=True)
    # notes: Mapped[str | None] = mapped_column(db.Text, nullable=True)
    # # TODO: Review these relationships
    # career = relationship("Career", back_populates="characters")
    # film = relationship("Film", back_populates="characters")

    def __repr__(self):
        return f"<Character {self.name} in Film {self.film_id} by Career {self.career_id}>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "aliases": self.aliases,
            "description": self.description,
            "film_id": str(self.film_id),
            "career_id": str(self.career_id),
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "episodes": self.episodes,
            "notes": self.notes
        }


class Studio(db.Model, ModelMixin, EntityMixin):
    pass


class Relationship(db.Model, ModelMixin):
    # __tablename__ = "relationships"
    # id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # person_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=False)
    # related_person_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=False)
    # relationship_type: Mapped[RelationshipType] = mapped_column(db.Enum(RelationshipType), nullable=False)
    # start_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    # end_date: Mapped[datetime | None] = mapped_column(db.Date, nullable=True)
    # # TODO: Review these relationships
    # person = relationship("Person", foreign_keys=[person_id], back_populates="relationships")
    # related_person = relationship("Person", foreign_keys=[related_person_id], back_populates="relationships")
    pass

    def __repr__(self):
        return f"<Relationship {self.relationship_type.value} between {self.person_id} and {self.related_person_id}>"

    def to_dict(self):
        return {
            "id": str(self.id),
            "person_id": str(self.person_id),
            "related_person_id": str(self.related_person_id),
            "relationship_type": self.relationship_type.value,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None
        }


class Shop(db.Model, ModelMixin, EntityMixin, HiveMixin):
    __tablename__ = "shops"
    merchandise: Mapped[List["Merchandise"]] = relationship("Merchandise", back_populates="shop")


class Asset(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "assets"
    portfolio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("portfolios.id"), nullable=False)
    token_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("tokens.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    token = relationship("Token")
    portfolio = relationship("Portfolio", back_populates="assets")


class Merchandise(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "merchandises"
    shop_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("shops.id"), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    inventory_count: Mapped[int] = mapped_column(Integer, default=0)
    shop = relationship("Shop", back_populates="merchandise")
    listings = relationship("Listing", back_populates="merchandise")
    discounts = relationship("Discount", back_populates="merchandise")


class Wallet(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "wallets"
    library_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("libraries.id"), nullable=False)
    library: Mapped["Library"] = relationship(back_populates="wallet")
    funds = relationship("Fund", back_populates="wallet")


class Accolade(db.Model, ModelMixin):
    title: Mapped[str] = mapped_column(String, nullable=False)
    calendar: Mapped["Calendar"] = relationship(back_populates="owner")
    wins: Mapped[list["Win"]] = relationship('Win', backref='accolade')


class Condition(db.Model, ModelMixin):
    pass


class Win(db.Model, ModelMixin, EntityMixin, EraMixin):
    # TODO: Ensure all back_populates are created and match
    award_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("awards.id"), nullable=True)
    award: Mapped["Award"] = relationship(back_populates="wins")
    accolade_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("accolades.id"), nullable=True)
    accolade: Mapped["Accolade"] = relationship(back_populates="wins")
    film_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("films.id"), nullable=True)
    film: Mapped["Film"] = relationship(back_populates="wins")
    album_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("albums.id"), nullable=True)
    album: Mapped["Album"] = relationship(back_populates="wins")
    hitlist_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("hitlists.id"), nullable=True)
    hitlist: Mapped["Hitlist"] = relationship(back_populates="wins")
    person_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("people.id"), nullable=True)
    person: Mapped["Person"] = relationship(back_populates="wins")


class Timeline(db.Model, ModelMixin):
    pass


class Filmography(db.Model, ModelMixin):
    pass


class StreamingPlatform(db.Model, ModelMixin, EntityMixin, PartnerMixin):
    pass


class PeersPlatform(db.Model, ModelMixin, EntityMixin, PartnerMixin):
    pass


class SocialPlatform(db.Model, ModelMixin, EntityMixin, PartnerMixin):
    pass


class Website(db.Model, ModelMixin, EntityMixin, PartnerMixin):
    pass


class AwardType(db.Model, ModelMixin, EntityMixin, AwardTypeMixin):
    pass


class Award(db.Model, ModelMixin, EntityMixin, AwardMixin):
    pass


class Nomination(db.Model, ModelMixin, EntityMixin, AwardMixin):
    pass


class BoxOffice(db.Model, ModelMixin, EntityMixin):
    pass


class TheBoxOffice(db.Model, ModelMixin, EntityMixin, PartnerMixin):
    pass


class Distributor(db.Model, ModelMixin, EntityMixin, PartnerMixin):
    pass


class Inspiration(db.Model, ModelMixin, EntityMixin):
    pass


class InspirationSource(db.Model, ModelMixin, EntityMixin):
    pass


class Theatre(db.Model, ModelMixin, EntityMixin, PartnerMixin):
    pass


class Release(db.Model, ModelMixin, EntityMixin):
    pass

