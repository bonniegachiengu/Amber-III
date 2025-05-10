from uuid import uuid4
from datetime import datetime
from typing import List, TYPE_CHECKING
from enum import Enum

from sqlalchemy import String, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..extensions import db
from .utils.config import OrderStatusEnum, TransactionStatusEnum, TransactionTypeEnum
from .mixins import (
    EntityMixin, HiveMixin, ModelMixin, ContributionMixin, PeriodMixin, FoundedMixin, CreatedMixin, AnalyzedMixin
)
from .associations import (
    market_contributors, customtoken_contributors, fund_contributors, listing_contributors, order_contributors,
    transaction_contributors, discount_contributors
)

if TYPE_CHECKING:
    from .library import Portfolio, Wallet, Merchandise, Asset


class Market(db.Model, ModelMixin, EntityMixin, HiveMixin, ContributionMixin, FoundedMixin, CreatedMixin, AnalyzedMixin):
    """
    Represents a Market entity within the application.

    This class defines the Market model, including its attributes and relationships.
    It is used to represent a market in the system and interacts with related
    entities like listings through ORM relationships.

    :ivar __tablename__: Specifies the name of the database table for the model.
    :type __tablename__: str
    :ivar listings: Defines the relationship to the Listing model, indicating
                    that a Market can have multiple associated listings.
    :type listings: sqlalchemy.orm.relationship
    """
    __tablename__ = "markets"
    __contribution_table__ = market_contributors
    __contribution_backref__ = "market_contributions"
    listings = relationship("Listing", back_populates="market")


class Token(db.Model, ModelMixin):
    """
    Represents a token stored in the database.

    This class maps to the 'tokens' table in the database and stores information
    about a specific token. It is used to manage and access the
    token's properties, including name, symbol, total supply, and its
    relationship with a ledger and currency. This class supports polymorphism
    with other types of tokens.

    :ivar type: Type of the token, used for polymorphism.
    :type type: str
    :ivar name: Name of the token.
    :type name: str
    :ivar symbol: Symbol representing the token, which is unique.
    :type symbol: str
    :ivar decimals: Number of decimal places the token uses.
    :type decimals: int
    :ivar total_supply: Total supply of the tokens, represented as a float with
        up to 20 digits and 4 decimal places.
    :type total_supply: float
    :ivar ledger_id: UUID of the associated ledger for the token.
    :type ledger_id: UUID
    :ivar ledger: Ledger object associated with the token.
    :type ledger: Ledger
    :ivar currency_id: UUID of the associated currency for the token.
    :type currency_id: UUID
    :ivar currency: Currency object associated with the token.
    :type currency: Currency
    """
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


class CustomToken(db.Model, ModelMixin, Token, ContributionMixin):
    """
    Defines a custom token class for use in a database model.

    This class represents a custom token with specific relationships and properties,
    inheriting behavior from several base classes. It includes a relationship to a
    creator portfolio and is identified polymorphically as "custom".

    :ivar creator_portfolio: Represents the user-related portfolio that created this token.
    :type creator_portfolio: Mapped["Portfolio"]
    """
    __tablename__ = "customtokens"
    __contribution_table__ = customtoken_contributors
    __contribution_backref__ = "customtoken_contributions"
    creator_portfolio: Mapped["Portfolio"] = relationship("User", back_populates="customtokens")
    asset_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("assets.id"), nullable=False)
    asset: Mapped["Asset"] = relationship("Asset", back_populates="customtoken")

    __mapper_args__ = {
        "polymorphic_identity": "custom",
    }


class AmberToken(db.Model, ModelMixin, Token):
    """
    Represents an AmberToken entity which extends the functionality of Token and integrates with
    database ORM support along with polymorphic identity for token inheritance.

    This class is used to handle AmberToken-specific functionality within the application.
    It maps to the "ambertokens" table in the database and ensures that each instance of
    AmberToken is uniquely identified by a UUID. It also utilizes polymorphic identity to
    support integration with a token inheritance model.

    :ivar id: A universally unique identifier (UUID) for each AmberToken instance.
    :type id: UUID
    """
    __tablename__ = "ambertokens"
    id: Mapped[UUID] = mapped_column(ForeignKey("tokens.id"), primary_key=True, default=uuid4)

    __mapper_args__ = {
        "polymorphic_identity": "amber",
    }


class Ledger(db.Model, ModelMixin, EntityMixin):
    """
    Represents a financial ledger.

    The Ledger class defines and manages the structure of financial ledgers in the database. It
    includes the name of the ledger, associated tokens, and transactions. It is designed to
    integrate with the database using SQLAlchemy and supports relationships to other entities such
    as Token and Transaction.

    :ivar name: The name of the ledger, which is a unique string identifier with
        a maximum length of 50 characters.
    :ivar tokens: A list of tokens associated with the ledger.
    :ivar transactions: A list of transactions associated with the ledger.
    """
    __tablename__ = "ledgers"
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    tokens: Mapped[List["Token"]] = relationship("Token", back_populates="ledger")
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="ledger")


class Fund(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a financial fund within the system.

    This class is a database model representing a fund entity. It includes
    fields to associate the fund with a specific wallet, a token, and various
    related financial transactions, conversions, orders, and balances. The class
    uses SQLAlchemy for database mapping and relationships.

    :ivar wallet_id: The unique identifier of the wallet linked to this fund.
    :type wallet_id: UUID
    :ivar token_id: The unique identifier of the token associated with this fund.
    :type token_id: UUID
    :ivar balance: The current balance of the fund, stored as a floating-point number
        with a precision of 4 decimal places.
    :type balance: float
    :ivar conversions: A list of conversion entities linked to this fund.
    :type conversions: list[Conversion]
    :ivar transactions: A list of transaction entities associated with this fund.
    :type transactions: list[Transaction]
    :ivar orders: A list of order entities related to this fund.
    :type orders: list[Order]
    :ivar token: The token entity linked to this fund.
    :type token: Token
    :ivar wallet: The wallet entity that this fund belongs to, with a back-population
        relationship defined.
    :type wallet: Wallet
    """
    __tablename__ = "funds"
    __contribution_table__ = fund_contributors
    __contribution_backref__ = "fund_contributions"
    wallet_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("wallets.id"))
    token_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("tokens.id"))
    balance: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    conversions: Mapped[List["Conversion"]] = relationship("Conversion")
    transactions: Mapped[List["Transaction"]] = relationship("Transaction")
    orders: Mapped[List["Order"]] = relationship("Order")
    token: Mapped["Token"] = relationship("Token")
    wallet: Mapped["Wallet"] = relationship("Wallet", back_populates="funds")


class Currency(db.Model, ModelMixin):
    """
    Represents a currency entity.

    This class models a currency with relevant information such as its code, name,
    exchange rates to USD and specific tokens, and relationships with other entities.
    It is mapped as a database model using SQLAlchemy ORM.

    :ivar code: The unique alphanumeric code representing the currency (e.g., USD, EUR).
    :ivar name: The name of the currency (e.g., United States Dollar, Euro).
    :ivar exchange_rate_to_usd: The exchange rate of this currency to USD. Defaults to 0.0.
    :ivar exchange_rate_to_ambertokens: The exchange rate of this currency to AmberTokens.
        Defaults to 0.0.
    :ivar tokens: A list of Token objects associated with this currency, representing
        the relationships defined in the database.
    """
    __tablename__ = "currencies"
    code: Mapped[str] = mapped_column(String(5), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    exchange_rate_to_usd: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    exchange_rate_to_ambertokens: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    tokens: Mapped[List["Token"]] = relationship("Token", back_populates="currency")


class Listing(db.Model, ModelMixin, EntityMixin, ContributionMixin):
    """
    Represents a listing entity within a marketplace system.

    The Listing class defines the schema of a marketplace listing and establishes
    relationships with other entities such as Market, Merchandise, and Order. It
    associates a specific merchandise item with a market and defines its price,
    while also maintaining references to related orders. This class is designed to
    be used within a database context for managing listings.

    :ivar market_id: Unique identifier of the associated market.
    :type market_id: UUID
    :ivar merchandise_id: Unique identifier of the associated merchandise.
    :type merchandise_id: UUID
    :ivar price: Price of the listed merchandise.
    :type price: float
    :ivar market: Related Market entity for the listing.
    :type market: Market
    :ivar merchandise: Related Merchandise entity for the listing.
    :type merchandise: Merchandise
    :ivar orders: List of related Order entities for the listing.
    :type orders: List[Order]
    """
    __tablename__ = "listings"
    __contribution_table__ = listing_contributors
    __contribution_backref__ = "listing_contributions"
    market_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("markets.id"))
    merchandise_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("merchandises.id"))
    price: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    market: Mapped["Market"] = relationship("Market", back_populates="listings")
    merchandise: Mapped["Merchandise"] = relationship("Merchandise", back_populates="listings")
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="listing")


class Order(db.Model, ModelMixin, ContributionMixin):
    """
    Represents an order entity in the database.

    This class is used to model an order that links a buyer's portfolio, a listing,
    and a fund while recording information about the quantity, total price, status,
    and timestamp of the order. It supports relationships with `Portfolio`, `Listing`,
    `Fund`, and `Transaction` entities for application-level interactions.

    :ivar buyer_portfolio_id: The unique identifier of the buyer's portfolio.
    :type buyer_portfolio_id: UUID
    :ivar listing_id: The unique identifier of the listing associated with the order.
    :type listing_id: UUID
    :ivar fund_id: The unique identifier of the fund associated with the order.
    :type fund_id: UUID
    :ivar quantity: The quantity of the items ordered. Defaults to 1.
    :type quantity: int
    :ivar total_price: The total price of the order. Defaults to 0.0.
    :type total_price: float
    :ivar status: The current status of the order, such as pending or completed.
    :type status: OrderStatusEnum
    :ivar timestamp: The time when the order was created. Defaults to the current time.
    :type timestamp: datetime
    :ivar buyer_portfolio: The portfolio entity associated with the order. Establishes
        a relationship with the Portfolio model.
    :type buyer_portfolio: Portfolio
    :ivar listing: The listing entity associated with the order. Establishes a
        relationship with the Listing model.
    :type listing: Listing
    :ivar fund: The fund entity associated with the order. Establishes a relationship
        with the Fund model.
    :type fund: Fund
    :ivar transactions: A list of transactions associated with the order. Establishes
        a relationship with the Transaction model.
    :type transactions: List[Transaction]
    """
    __tablename__ = "orders"
    __contribution_table__ = order_contributors
    __contribution_backref__ = "order_contributions"
    buyer_portfolio_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("portfolios.id"))
    listing_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("listings.id"))
    fund_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("funds.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    total_price: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    status: Mapped[OrderStatusEnum] = mapped_column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING)
    timestamp: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)
    buyer_portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="orders")
    listing: Mapped["Listing"] = relationship("Listing", back_populates="orders")
    fund: Mapped["Fund"] = relationship("Fund", back_populates="orders")
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="order")


class Conversion(db.Model, ModelMixin):
    """
    Represents a conversion entity for mapping and maintaining relationships between
    different funds and tokens with an associated conversion rate.

    The class is designed for use with a database, specifically leveraging SQLAlchemy's ORM.
    It holds references between funds and tokens, supporting conversion operations by providing
    a structural mapping of source and target entities via their respective IDs and relationships.
    This entity stores the conversion rate for transforming one asset to another.

    :ivar from_fund_id: ID of the originating fund for the conversion.
    :type from_fund_id: UUID
    :ivar to_fund_id: ID of the target fund for the conversion.
    :type to_fund_id: UUID
    :ivar from_token_id: ID of the originating token for the conversion.
    :type from_token_id: UUID
    :ivar to_token_id: ID of the target token for the conversion.
    :type to_token_id: UUID
    :ivar rate: The conversion rate from the originating token/fund to the target
        token/fund. Defaults to 0.0.
    :type rate: float
    :ivar from_fund: Relationship mapping to the originating fund.
    :type from_fund: Fund
    :ivar to_fund: Relationship mapping to the target fund.
    :type to_fund: Fund
    :ivar from_token: Relationship mapping to the originating token.
    :type from_token: Token
    :ivar to_token: Relationship mapping to the target token.
    :type to_token: Token
    """
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


class Transaction(db.Model, ModelMixin, EntityMixin, ContributionMixin):
    """
    Represents a financial transaction within the system.

    This class models the details of a financial transaction, such as its associated funds,
    status, type, and related entities like orders, ledgers, and currencies. It is designed to
    track monetary transfers between funds, including tolls and fees, and is associated with
    various other entities for better contextual information and processing.

    :ivar from_fund_id: Identifier of the fund from which the transaction originates.
    :type from_fund_id: UUID
    :ivar to_fund_id: Identifier of the fund to which the transaction is directed.
    :type to_fund_id: UUID
    :ivar toll_fund: Identifier of the fund representing toll charges.
    :type toll_fund: UUID
    :ivar ledger_id: Identifier of the ledger associated with the transaction.
    :type ledger_id: UUID
    :ivar order_id: Identifier of the related order if applicable.
    :type order_id: UUID, optional
    :ivar currency_id: Identifier of the currency in which the transaction occurs.
    :type currency_id: UUID
    :ivar amount: Transaction amount excluding fees and tolls.
    :type amount: float
    :ivar fee: Fee associated with the transaction.
    :type fee: float
    :ivar total_amount: Total transaction amount, including fees and tolls.
    :type total_amount: float
    :ivar status: Status of the transaction (e.g., pending, completed, failed).
    :type status: TransactionStatusEnum
    :ivar type: Type/category of the transaction.
    :type type: TransactionTypeEnum
    :ivar ledger: Relationship to the associated ledger.
    :type ledger: Ledger
    :ivar from_fund: Relationship to the originating fund.
    :type from_fund: Fund
    :ivar to_fund: Relationship to the destination fund.
    :type to_fund: Fund
    :ivar order: Relationship to the associated order.
    :type order: Order
    :ivar currency: Relationship to the transaction currency.
    :type currency: Currency
    :ivar timestamp: Timestamp when the transaction is created.
    :type timestamp: datetime
    """
    __tablename__ = "transactions"
    __contribution_table__ = transaction_contributors
    __contribution_backref__ = "transaction_contributions"
    from_fund_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("funds.id"))
    to_fund_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("funds.id"))
    toll_fund: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("funds.id"))
    ledger_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("ledgers.id"))
    order_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("orders.id"), nullable=True)
    currency_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("currencies.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    fee: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    total_amount: Mapped[float] = mapped_column(Numeric(20, 4), default=0.0)
    status: Mapped[TransactionStatusEnum] = mapped_column(Enum(TransactionStatusEnum), default=TransactionStatusEnum.PENDING)
    type: Mapped[TransactionTypeEnum] = mapped_column(Enum(TransactionTypeEnum), nullable=False)
    ledger: Mapped["Ledger"] = relationship("Ledger", back_populates="transactions")
    from_fund: Mapped["Fund"] = relationship("Fund", foreign_keys=[from_fund_id], back_populates="transactions")
    to_fund: Mapped["Fund"] = relationship("Fund", foreign_keys=[to_fund_id], back_populates="transactions")
    order: Mapped["Order"] = relationship("Order", back_populates="transactions")
    currency: Mapped["Currency"] = relationship("Currency")
    timestamp: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)


class Discount(db.Model, ModelMixin, EntityMixin, PeriodMixin, ContributionMixin):
    """
    Represents the discount applied to a merchandise item.

    The Discount class is tied to a specific merchandise item and defines
    the percentage of the discount. It is stored within the database with
    a foreign key reference to the related merchandise entry.

    :ivar merchandise_id: The unique identifier of the associated
        merchandise item.
    :ivar percentage: The percentage of the discount applied. Defaults
        to 0.0.
    :ivar merchandise: The related Merchandise object to which this
        discount applies.
    """
    __tablename__ = "discounts"
    __contribution_table__ = discount_contributors
    __contribution_backref__ = "discount_contributions"
    merchandise_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), db.ForeignKey("merchandises.id"))
    percentage: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0)
    merchandise: Mapped["Merchandise"] = relationship("Merchandise", back_populates="discounts")
