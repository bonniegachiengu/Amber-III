from sqlalchemy import Table, Column, ForeignKey

from ..extensions import db

# Association table for films and contributors
film_contributors = Table(
    "film_contributors",
    db.metadata,
    Column("film_id", ForeignKey("films.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for persons and contributors
person_contributors = Table(
    "person_contributors",
    db.metadata,
    Column("person_id", ForeignKey("persons.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for markets and contributors
market_contributors = Table(
    "market_contributors",
    db.metadata,
    Column("market_id", ForeignKey("markets.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for customtokens and contributors
customtoken_contributors = Table(
    "customtoken_contributors",
    db.metadata,
    Column("customtoken_id", ForeignKey("customtoken.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for funds and contributors
fund_contributors = Table(
    "fund_contributors",
    db.metadata,
    Column("fund_id", ForeignKey("funds.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for listings and contributors
listing_contributors = Table(
    "listing_contributors",
    db.metadata,
    Column("listing_id", ForeignKey("listings.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for orders and contributors
order_contributors = Table(
    "order_contributors",
    db.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for transactions and contributors
transaction_contributors = Table(
    "transaction_contributors",
    db.metadata,
    Column("transaction_id", ForeignKey("transactions.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for discounts and contributors
discount_contributors = Table(
    "discount_contributors",
    db.metadata,
    Column("discount_id", ForeignKey("discounts.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for events and contributors
event_contributors = Table(
    "event_contributors",
    db.metadata,
    Column("event_id", ForeignKey("events.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for tickets and contributors
ticket_contributors = Table(
    "ticket_contributors",
    db.metadata,
    Column("ticket_id", ForeignKey("tickets.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)
