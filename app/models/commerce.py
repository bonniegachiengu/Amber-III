from uuid import uuid4
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from enum import Enum

from sqlalchemy import String, Boolean, ForeignKey, JSON, Date, Integer, Float, Text, ARRAY, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, relationships, declared_attr
from werkzeug.security import generate_password_hash, check_password_hash

from . import EraMixin
from ..extensions import db
from .utils.config import OrderStatus, TransactionStatus
from .mixins import (
    EntityMixin, HiveMixin, CliqueMixin, ModeratorMixin, CreatorMixin, OwnerMixin, AuthorMixin,
    ModelMixin
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


class Market(db.Model, ModelMixin, EntityMixin, HiveMixin):
    __tablename__ = "markets"
    listings = relationship("Listing", back_populates="market")


class Token(db.Model, ModelMixin):
    __tablename__ = "tokens"
    type: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    symbol: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    decimals: Mapped[int] = mapped_column(default=2)
    total_supply: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    ledger_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("ledgers.id"), nullable=False)
    ledger = relationship("Ledger", back_populates="tokens")
    currency_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("currencies.id"), nullable=False)
    currency = relationship("Currency", back_populates="tokens")

    __mapper_args__ = {
        "polymorphic_identity": "token",
        "polymorphic_on": type,
    }


class CustomToken(db.Model, ModelMixin, Token):
    __tablename__ = "customtokens"
    id: Mapped[UUID] = mapped_column(ForeignKey("tokens.id"), primary_key=True, default=uuid4)
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    creator = relationship("User", back_populates="custom_tokens")

    __mapper_args__ = {
        "polymorphic_identity": "custom",
    }


class AmberTokens(db.Model, ModelMixin, Token):
    __tablename__ = "ambertokens"
    id: Mapped[UUID] = mapped_column(ForeignKey("tokens.id"), primary_key=True, default=uuid4)

    __mapper_args__ = {
        "polymorphic_identity": "amber",
    }


class Ledger(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "ledgers"
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    tokens = relationship("Token", back_populates="ledger")
    transactions = relationship("Transaction", back_populates="ledger")


class Fund(db.Model, ModelMixin): # TODO: Add to canvas
    __tablename__ = "funds"
    wallet_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("wallets.id"))
    token_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("tokens.id"))
    balance: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    conversions = relationship("Conversion")
    transactions = relationship("Transaction")
    token = relationship("Token")
    wallet = relationship("Wallet", back_populates="funds")


class Currency(db.Model, ModelMixin):
    __tablename__ = "currencies"
    code: Mapped[str] = mapped_column(String(5), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    exchange_rate_to_usd: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    exchange_rate_to_ambertokens: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    tokens = relationship("Token", back_populates="currency")


class Listing(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "listings"
    market_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("markets.id"))
    merchandise_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("merchandises.id"))
    price: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    market = relationship("Market", back_populates="listings")
    merchandise = relationship("Merchandise", back_populates="listings")
    orders = relationship("Order", back_populates="listing")


class Order(db.Model, ModelMixin):
    __tablename__ = "orders"
    buyer_portfolio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("portfolios.id"))
    listing_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("listings.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    total_price: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)
    timestamp: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)
    buyer_portfolio = relationship("Portfolio", back_populates="orders")
    listing = relationship("Listing", back_populates="orders")
    transactions = relationship("Transaction", back_populates="order")


class Conversion(db.Model, ModelMixin):
    __tablename__ = "conversions"
    from_fund_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("funds.id"))
    to_fund_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("funds.id"))
    from_token_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("tokens.id"))
    to_token_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("tokens.id"))
    rate: Mapped[float] = mapped_column(Numeric(20, 8), default=0.0)
    from_fund = relationship("Fund", foreign_keys=[from_fund_id], back_populates="conversions")
    to_fund = relationship("Fund", foreign_keys=[to_fund_id], back_populates="conversions")
    from_token = relationship("Token", foreign_keys=[from_token_id])
    to_token = relationship("Token", foreign_keys=[to_token_id])



class Transaction(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "transactions"
    from_fund_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("funds.id"))
    to_fund_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("funds.id"))
    toll_fund: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("funds.id"))
    ledger_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("ledgers.id"))
    order_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("orders.id"))
    currency_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("currencies.id"))
    amount: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    fee: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    total_amount: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    ledger = relationship("Ledger", back_populates="transactions")
    from_fund = relationship("Fund", foreign_keys=[from_fund_id], back_populates="transactions")
    to_fund = relationship("Fund", foreign_keys=[to_fund_id], back_populates="transactions")
    order = relationship("Order", back_populates="transactions")
    currency = relationship("Currency")
    timestamp: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)


class Discount(db.Model, ModelMixin, EntityMixin, EraMixin):
    __tablename__ = "discounts"
    merchandise_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("merchandises.id"))
    percentage: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0)
    merchandise = relationship("Merchandise", back_populates="discounts")


# class Receipt(db.Model, ModelMixin):
#     pass
#
# class Inventory(db.Model, ModelMixin):
#     pass
