from sqlalchemy import Table, Column, ForeignKey

from ..extensions import db

# Association table for films and contributors
film_contributors = Table(
    "film_contributors",
    db.metadata,
    Column("film_id", ForeignKey("films.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
    # Column("role", db.Enum("owner", "editor", "writer", "chief_editor", "correspondent", "editor-in-chief", "analyst", name="contributor_role")),
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

# Association table for clubs and contributors
club_contributors = Table(
    "club_contributors",
    db.metadata,
    Column("club_id", ForeignKey("clubs.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for fandoms and contributors
fandom_contributors = Table(
    "fandom_contributors",
    db.metadata,
    Column("fandom_id", ForeignKey("fandoms.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for magazines and contributors
magazine_contributors = Table(
    "magazine_contributors",
    db.metadata,
    Column("magazine_id", ForeignKey("magazines.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for columns and contributors
column_contributors = Table(
    "column_contributors",
    db.metadata,
    Column("column_id", ForeignKey("columns.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for articles and contributors
article_contributors = Table(
    "article_contributors",
    db.metadata,
    Column("article_id", ForeignKey("articles.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for reports and contributors
report_contributors = Table(
    "report_contributors",
    db.metadata,
    Column("report_id", ForeignKey("reports.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for scrolls and contributors
scroll_contributors = Table(
    "scroll_contributors",
    db.metadata,
    Column("scroll_id", ForeignKey("scrolls.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association table for subtitles and contributors
subtitle_contributors = Table(
    "subtitle_contributors",
    db.metadata,
    Column("subtitle_id", ForeignKey("subtitles.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association tables for dashboard_templates and contributors
dashboard_template_contributors = Table(
    "dashboard_template_contributors",
    db.metadata,
    Column("dashboard_template_id", ForeignKey("dashboard_templates.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association tables for wiki_templates and contributors
wiki_template_contributors = Table(
    "wiki_template_contributors",
    db.metadata,
    Column("wiki_template_id", ForeignKey("wiki_templates.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association tables for tags and contributors
tag_contributors = Table(
    "tag_contributors",
    db.metadata,
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association tables for languages and contributors
language_contributors = Table(
    "language_contributors",
    db.metadata,
    Column("language_id", ForeignKey("languages.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association tables for countries and contributors
country_contributors = Table(
    "country_contributors",
    db.metadata,
    Column("country_id", ForeignKey("countries.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association tables for nationalities and contributors
nationality_contributors = Table(
    "nationality_contributors",
    db.metadata,
    Column("nationality_id", ForeignKey("nationalities.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association tables for periods and contributors
period_contributors = Table(
    "period_contributors",
    db.metadata,
    Column("period_id", ForeignKey("periods.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association tables for genres and contributors
genre_contributors = Table(
    "genre_contributors",
    db.metadata,
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association tables for themes and contributors
theme_contributors = Table(
    "theme_contributors",
    db.metadata,
    Column("theme_id", ForeignKey("themes.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association tables for keywords and contributors
keyword_contributors = Table(
    "keyword_contributors",
    db.metadata,
    Column("keyword_id", ForeignKey("keywords.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association tables for report_templates and contributors
report_template_contributors = Table(
    "report_template_contributors",
    db.metadata,
    Column("report_template_id", ForeignKey("report_templates.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)

# Association tables for verifications and contributors
verification_contributors = Table(
    "verification_contributors",
    db.metadata,
    Column("verification_id", ForeignKey("verifications.id"), primary_key=True),
    Column("contributor_id", ForeignKey("contributors.id"), primary_key=True),
)
