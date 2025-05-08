from uuid import uuid4
from datetime import datetime
from typing import List, TYPE_CHECKING
from enum import Enum

from sqlalchemy import String, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models import Merchandise
from app.models import Wallet
from . import EraMixin
from ..extensions import db
from .utils.config import OrderStatus, TransactionStatus, TransactionType
from .mixins import EntityMixin, HiveMixin, ModelMixin


if TYPE_CHECKING:
    from .library import Portfolio, Wallet, Merchandise


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
    ledger: Mapped["Ledger"] = relationship("Ledger", back_populates="tokens")
    currency_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("currencies.id"), nullable=False)
    currency: Mapped["Currency"] = relationship("Currency", back_populates="tokens")

    __mapper_args__ = {
        "polymorphic_identity": "token",
        "polymorphic_on": type,
    }


class CustomToken(db.Model, ModelMixin, Token):
    __tablename__ = "customtokens"
    creator_portfolio: Mapped["Portfolio"] = relationship("User", back_populates="customtokens")

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
    tokens: Mapped[List["Token"]] = relationship("Token", back_populates="ledger")
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="ledger")


class Fund(db.Model, ModelMixin): # TODO: Add to canvas
    __tablename__ = "funds"
    wallet_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("wallets.id"))
    token_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("tokens.id"))
    balance: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    conversions: Mapped[List["Conversion"]] = relationship("Conversion")
    transactions: Mapped[List["Transaction"]] = relationship("Transaction")
    orders: Mapped[List["Order"]] = relationship("Order")
    token: Mapped["Token"] = relationship("Token")
    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="funds")


class Currency(db.Model, ModelMixin):
    __tablename__ = "currencies"
    code: Mapped[str] = mapped_column(String(5), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    exchange_rate_to_usd: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    exchange_rate_to_ambertokens: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    tokens: Mapped[List["Token"]] = relationship("Token", back_populates="currency")


class Listing(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "listings"
    market_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("markets.id"))
    merchandise_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("merchandises.id"))
    price: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    market: Mapped["Market"] = relationship("Market", back_populates="listings")
    merchandise: Mapped["Merchandise"] = relationship("Merchandise", back_populates="listings")
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="listing")


class Order(db.Model, ModelMixin):
    __tablename__ = "orders"
    buyer_portfolio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("portfolios.id"))
    listing_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("listings.id"))
    fund_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("funds.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    total_price: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)
    timestamp: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)
    buyer_portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="orders")
    listing: Mapped["Listing"] = relationship("Listing", back_populates="orders")
    fund: Mapped["Fund"] = relationship("Fund", back_populates="orders")
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="order")


class Conversion(db.Model, ModelMixin):
    __tablename__ = "conversions"
    from_fund_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("funds.id"))
    to_fund_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("funds.id"))
    from_token_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("tokens.id"))
    to_token_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("tokens.id"))
    rate: Mapped[float] = mapped_column(Numeric(20, 8), default=0.0)
    from_fund: Mapped["Fund"] = relationship("Fund", foreign_keys=[from_fund_id], back_populates="conversions")
    to_fund: Mapped["Fund"] = relationship("Fund", foreign_keys=[to_fund_id], back_populates="conversions")
    from_token: Mapped["Token"] = relationship("Token", foreign_keys=[from_token_id])
    to_token: Mapped["Token"] = relationship("Token", foreign_keys=[to_token_id])



class Transaction(db.Model, ModelMixin, EntityMixin):
    __tablename__ = "transactions"
    from_fund_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("funds.id"))
    to_fund_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("funds.id"))
    toll_fund: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("funds.id"))
    ledger_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("ledgers.id"))
    order_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("orders.id"), nullable=True)
    currency_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("currencies.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    fee: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    total_amount: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)
    ledger: Mapped["Ledger"] = relationship("Ledger", back_populates="transactions")
    from_fund: Mapped["Fund"] = relationship("Fund", foreign_keys=[from_fund_id], back_populates="transactions")
    to_fund: Mapped["Fund"] = relationship("Fund", foreign_keys=[to_fund_id], back_populates="transactions")
    order: Mapped["Order"] = relationship("Order", back_populates="transactions")
    currency: Mapped["Currency"] = relationship("Currency")
    timestamp: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)


class Discount(db.Model, ModelMixin, EntityMixin, EraMixin):
    __tablename__ = "discounts"
    merchandise_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("merchandises.id"))
    percentage: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0)
    merchandise: Mapped["Merchandise"] = relationship("Merchandise", back_populates="discounts")

