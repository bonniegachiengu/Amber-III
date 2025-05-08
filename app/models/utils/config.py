from enum import Enum

class FilmType(Enum):
    """
    Represents the different types of films or videos that can be categorized.

    This enumeration helps to classify various forms of film or video content into
    predefined categories, making it easier to organize, filter, and manage them
    within the application.

    :cvar MOVIE: Represents a full-length movie.
    :cvar TV_EPISODE: Represents an episode of a television series.
    :cvar YOUTUBE_VIDEO: Represents a video hosted on YouTube.
    :cvar SHORT: Represents a short film or video.
    """
    MOVIE = "Movie"
    TV_EPISODE = "TV Episode"
    YOUTUBE_VIDEO = "YouTube Video"
    SHORT = "Short"


class RelationshipType(Enum):
    """
    Represents different types of familial or relational connections.

    This enumeration consists of various relationship types often used in
    family trees, genealogy software, and applications dealing with relational
    dynamics. It encapsulates relationships such as familial bonds (e.g.,
    parent-child relationships, sibling relationships), marital statuses (e.g.,
    spouse, ex-spouse, partner), and extended family ties (e.g., grandparent,
    grandchild, uncle, aunt).

    :ivar SIBLING: Refers to a sibling relationship.
    :type SIBLING: str
    :ivar PARENT: Represents a parent relationship.
    :type PARENT: str
    :ivar CHILD: Refers to a child relationship.
    :type CHILD: str
    :ivar STEPPARENT: Represents a stepparent relationship.
    :type STEPPARENT: str
    :ivar STEPSIBLING: Refers to a stepsibling relationship.
    :type STEPSIBLING: str
    :ivar COUSIN: Indicates a cousin relationship.
    :type COUSIN: str
    :ivar SPOUSE: Represents a marital relationship.
    :type SPOUSE: str
    :ivar EX_SPOUSE: Represents a dissolved marital relationship.
    :type EX_SPOUSE: str
    :ivar UNCLE: Indicates an uncle relationship.
    :type UNCLE: str
    :ivar AUNT: Indicates an aunt relationship.
    :type AUNT: str
    :ivar NEPHEW: Represents a nephew relationship.
    :type NEPHEW: str
    :ivar NIECE: Represents a niece relationship.
    :type NIECE: str
    :ivar GRANDPARENT: Refers to a grandparent relationship.
    :type GRANDPARENT: str
    :ivar GRANDCHILD: Refers to a grandchild relationship.
    :type GRANDCHILD: str
    :ivar GREAT_GRANDPARENT: Represents a great-grandparent relationship.
    :type GREAT_GRANDPARENT: str
    :ivar GREAT_GRANDCHILD: Represents a great-grandchild relationship.
    :type GREAT_GRANDCHILD: str
    :ivar PARTNER: Indicates a partner relationship.
    :type PARTNER: str
    """
    SIBLING = "Sibling"
    PARENT = "Parent"
    CHILD = "Child"
    STEPPARENT = "StepParent"
    STEPSIBLING = "StepSibling"
    COUSIN = "Cousin"
    SPOUSE = "Spouse"
    EX_SPOUSE = "Ex-Spouse"
    UNCLE = "Uncle"
    AUNT = "Aunt"
    NEPHEW = "Nephew"
    NIECE = "Niece"
    GRANDPARENT = "Grandparent"
    GRANDCHILD = "Grandchild"
    GREAT_GRANDPARENT = "Great-Grandparent"
    GREAT_GRANDCHILD = "Great-Grandchild"
    PARTNER = "Partner"



class EventType(Enum):
    """
    Enum representing various types of events.

    This enumeration defines a wide range of events that could occur across
    different contexts, such as movies, clubs, fandoms, market/merchandise, and
    general activities. Each item represents a specific kind of event, providing
    a structured way to categorize and handle them within an application.

    :ivar PREMIERE: Represents a movie or series première event.
    :ivar SCREENING: Represents a movie or series screening event.
    :ivar RELEASE_DATE: Represents an official release date for a movie or other forms of media.
    :ivar FESTIVAL_APPEARANCE: Represents a movie or series appearance in a festival.
    :ivar AWARD_NOMINATION: Represents an award nomination event.
    :ivar AWARD_WIN: Represents an award win event.
    :ivar RE_RELEASE: Represents a re-release of a previously released media.
    :ivar TRAILER_DROP: Represents the release of a trailer.
    :ivar STREAMING_RELEASE: Represents the release of a movie or series on streaming platforms.
    :ivar HOME_RELEASE: Represents the release of a movie or series for home viewing.
    :ivar WATCH_LOG: Represents a logged personal watch event.

    Album Events:
    :ivar CURATION_START: Event indicating the start of album curation.
    :ivar CURATION_LOCK: Event indicating the locking of album curation.
    :ivar PUBLIC_RELEASE: Event indicating public release of an album.
    :ivar UPDATE: Event indicating a general update related to an album.
    :ivar COLLABORATION_EVENT: Event indicating a collaborative album-related event.

    Fandom Events:
    :ivar FAN_EVENT: Represents a general fan-related event, such as meetups.
    :ivar WATCH_PARTY: Represents an organized fan watch party.
    :ivar COSPLAY_CONTEST: Represents a cosplay contest event.
    :ivar FAN_THEORY_DROP: Represents the event of releasing a fan theory.
    :ivar ANNIVERSARY: Represents an anniversary of a movie, series, or event.

    Club Events:
    :ivar MEETING: Represents a club meeting event.
    :ivar SCREENING_SESSION: Represents a movie screening session conducted by a club.
    :ivar VOTE_START: Represents the start of a voting session.
    :ivar VOTE_DEADLINE: Represents the deadline for voting.
    :ivar CHALLENGE_LAUNCH: Represents the launch of a challenge.
    :ivar CHALLENGE_WRAPUP: Represents the wrap-up of a challenge.
    :ivar NEW_ROUND_ANNOUNCEMENT: Represents an announcement of a new round in a challenge.

    Arena Events:
    :ivar DEBATE: Represents a debate event.
    :ivar SHOWDOWN_START: Represents the start of a showdown event.
    :ivar SHOWDOWN_RESULT: Represents the result announcement of a showdown.
    :ivar POLL_OPEN: Represents the opening of a poll.
    :ivar POLL_CLOSE: Represents the closing of a poll.
    :ivar MATCHUP_ANNOUNCEMENT: Represents an announcement for a matchup.

    Journal / Magazine Events:
    :ivar COLUMN_PUBLISH: Represents the publishing of a journal or magazine column.
    :ivar ISSUE_RELEASE: Represents the release of a journal or magazine issue.
    :ivar SUBMISSION_DEADLINE: Represents a submission deadline for a journal or magazine.
    :ivar EDITORIAL_MEETING: Represents an editorial meeting event.
    :ivar REVIEW_SESSION: Represents a review session for journal or magazine content.
    :ivar FEATURE_ANNOUNCEMENT: Represents a feature announcement related to a journal or magazine.

    Market / Merch Events:
    :ivar DROP_ANNOUNCEMENT: Event announcing an upcoming product or merchandise drop.
    :ivar DROP_START: Event indicating the start of a merchandise drop.
    :ivar DROP_END: Event indicating the end of a merchandise drop.
    :ivar RESTOCK: Event indicating a restocking of items.
    :ivar SALE_EVENT: Represents a sale event.
    :ivar AUCTION_OPEN: Represents the opening of an auction.
    :ivar AUCTION_CLOSE: Represents the closing of an auction.
    :ivar NEW_LISTING: Represents a newly listed product or item.

    General Events:
    :ivar ANNOUNCEMENT: Represents a generic announcement event.
    :ivar MAINTENANCE: Represents a maintenance-related event.
    :ivar COMMUNITY_EVENT: Represents a community-oriented event.
    :ivar MILESTONE: Represents the achievement of a milestone.
    :ivar CAMPAIGN_LAUNCH: Represents the launch of a campaign.
    """
    PREMIERE = "premiere"
    SCREENING = "screening"
    RELEASE_DATE = "release_date"
    FESTIVAL_APPEARANCE = "festival_appearance"
    AWARD_NOMINATION = "award_nomination"
    AWARD_WIN = "award_win"
    RE_RELEASE = "re_release"
    TRAILER_DROP = "trailer_drop"
    STREAMING_RELEASE = "streaming_release"
    HOME_RELEASE = "home_release"
    WATCH_LOG = "watch_log"
    # --- Album Events ---
    CURATION_START = "curation_start"
    CURATION_LOCK = "curation_lock"
    PUBLIC_RELEASE = "public_release"
    UPDATE = "update"
    COLLABORATION_EVENT = "collaboration_event"
    # --- Fandom Events ---
    FAN_EVENT = "fan_event"
    WATCH_PARTY = "watch_party"
    COSPLAY_CONTEST = "cosplay_contest"
    FAN_THEORY_DROP = "fan_theory_drop"
    ANNIVERSARY = "anniversary"
    # --- Club Events ---
    MEETING = "meeting"
    SCREENING_SESSION = "screening_session"
    VOTE_START = "vote_start"
    VOTE_DEADLINE = "vote_deadline"
    CHALLENGE_LAUNCH = "challenge_launch"
    CHALLENGE_WRAPUP = "challenge_wrapup"
    NEW_ROUND_ANNOUNCEMENT = "new_round_announcement"
    # --- Arena Events ---
    DEBATE = "debate"
    SHOWDOWN_START = "showdown_start"
    SHOWDOWN_RESULT = "showdown_result"
    POLL_OPEN = "poll_open"
    POLL_CLOSE = "poll_close"
    MATCHUP_ANNOUNCEMENT = "matchup_announcement"
    # --- Journal / Magazine Events ---
    COLUMN_PUBLISH = "column_publish"
    ISSUE_RELEASE = "issue_release"
    SUBMISSION_DEADLINE = "submission_deadline"
    EDITORIAL_MEETING = "editorial_meeting"
    REVIEW_SESSION = "review_session"
    FEATURE_ANNOUNCEMENT = "feature_announcement"
    # --- Market / Merch Events ---
    DROP_ANNOUNCEMENT = "drop_announcement"
    DROP_START = "drop_start"
    DROP_END = "drop_end"
    RESTOCK = "restock"
    SALE_EVENT = "sale_event"
    AUCTION_OPEN = "auction_open"
    AUCTION_CLOSE = "auction_close"
    NEW_LISTING = "new_listing"
    # --- General Events ---
    ANNOUNCEMENT = "announcement"
    MAINTENANCE = "maintenance"
    COMMUNITY_EVENT = "community_event"
    MILESTONE = "milestone"
    CAMPAIGN_LAUNCH = "campaign_launch"


class EventRepeat(Enum):
    """
    Enumeration representing various repetition modes for events.

    This class defines different constants that indicate how an event
    can repeat over time. It is used to categorize events based on their
    repetition frequency, such as daily, weekly, monthly, etc.

    :ivar ONCE: Represents an event that occurs only once.
    :type ONCE: str
    :ivar DAILY: Represents an event that recurs daily.
    :type DAILY: str
    :ivar WEEKLY: Represents an event that recurs weekly.
    :type WEEKLY: str
    :ivar MONTHLY: Represents an event that recurs monthly.
    :type MONTHLY: str
    :ivar YEARLY: Represents an event that recurs yearly.
    :type YEARLY: str
    :ivar NONE: Represents an event that does not repeat.
    :type NONE: str
    """
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    NONE = "none"


class EventStatus(Enum):
    """
    Represents the statuses an event can have.

    This enumeration defines four different statuses for an event to indicate
    its current state in the event lifecycle. It is useful for organizing and
    handling events in scheduling systems, ticketing applications, or any
    context where event tracking is required.

    :ivar UPCOMING: Status indicating the event is scheduled but has not yet started.
    :type UPCOMING: str
    :ivar ONGOING: Status indicating the event is currently happening.
    :type ONGOING: str
    :ivar COMPLETED: Status indicating the event has finished.
    :type COMPLETED: str
    :ivar CANCELLED: Status indicating the event was cancelled and will not take place.
    :type CANCELLED: str
    """
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SubmissionStatus(Enum):
    """
    Enumeration representing the various states of a submission.

    Used to indicate the current status of a submission in a workflow or system.
    Provides predefined statuses, such as 'DRAFT', 'PENDING', 'APPROVED',
    'REJECTED', and 'DELETED'.

    :ivar DRAFT: Represents a submission in draft state and not yet
        finalized.
    :type DRAFT: str
    :ivar PENDING: Indicates a submission awaiting review or approval.
    :type PENDING: str
    :ivar APPROVED: Indicates that a submission has been reviewed and approved.
    :type APPROVED: str
    :ivar REJECTED: Indicates that a submission has been reviewed and rejected.
    :type REJECTED: str
    :ivar DELETED: Represents a submission that has been removed or deleted.
    :type DELETED: str
    """
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DELETED = "deleted"


class OrderStatus(Enum):
    """
    Represents the status of an order.

    This Enum defines the possible states that an order can have during its
    lifecycle. It allows for clear and consistent representation of the order's
    current status. This class is used to manage statuses of orders in systems
    where such states need to be tracked.

    :ivar PENDING: Indicates that the order is still pending and not yet processed.
    :type PENDING: str
    :ivar COMPLETED: Indicates that the order has been successfully completed.
    :type COMPLETED: str
    :ivar CANCELLED: Indicates that the order has been cancelled and will not be
        processed further.
    :type CANCELLED: str
    """
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TransactionStatus(Enum):
    """
    Represents the status of a transaction in a financial or e-commerce system.

    This enumeration provides various status values that a transaction might
    have during its lifecycle. It helps in categorizing and managing the state
    of a transaction, allowing for smoother handling of financial operations.

    :cvar SUCCESS: Represents a successfully completed transaction.
    :cvar FAILED: Indicates a transaction that has failed to process.
    :cvar CANCELLED: Denotes a transaction cancelled by the user or provider.
    :cvar PENDING: Refers to a transaction still in progress or awaiting confirmation.
    :cvar REJECTED: Marks a transaction that has been explicitly rejected.
    :cvar EXPIRED: Represents a transaction not completed within allowable time limits.
    :cvar REFUNDED: Denotes a transaction for which the payment has been returned to the user.
    :cvar PENDING_REFUND: Indicates a transaction awaiting the initiation of a refund.
    :cvar REFUNDED_WITH_CREDIT: Specifies a transaction refunded through a credit balance.
    :cvar REFUNDED_WITH_DEBIT: Specifies a transaction refunded through a debit balance.
    """
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PENDING = "pending"
    REJECTED = "rejected"
    EXPIRED = "expired"
    REFUNDED = "refunded"
    PENDING_REFUND = "pending_refund"
    REFUNDED_WITH_CREDIT = "refunded_with_credit"
    REFUNDED_WITH_DEBIT = "refunded_with_debit"

class TransactionType(Enum):
    """
    Represents the different types of financial transactions.

    This enumeration defines the possible transaction types that can occur in
    a financial system. Each type corresponds to a specific purpose or action
    associated with monetary operations.

    :ivar PURCHASE: Represents a transaction where goods or services are bought.
    :type PURCHASE: str
    :ivar REFUND: Represents a transaction where money is returned to the buyer.
    :type REFUND: str
    :ivar EXCHANGE: Indicates a transaction where items are substituted or swapped.
    :type EXCHANGE: str
    :ivar TIP: Indicates an optional additional amount given, often to service providers.
    :type TIP: str
    :ivar DEPOSIT: Represents a transaction where money is added to an account.
    :type DEPOSIT: str
    :ivar WITHDRAW: Represents a transaction that deducts money from an account.
    :type WITHDRAW: str
    :ivar CREDIT: Represents a transaction that increases the account's credit balance.
    :type CREDIT: str
    :ivar DEBIT: Represents a transaction that decreases the account's balance.
    :type DEBIT: str
    :ivar PAYMENT: Represents a transaction that settles a debt or fee.
    :type PAYMENT: str
    """
    PURCHASE = "purchase"
    REFUND = "refund"
    EXCHANGE = "exchange"
    TIP = "tip"
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    CREDIT = "credit"
    DEBIT = "debit"
    PAYMENT = "payment"


class Visibility(Enum):
    """
    Enumeration of visibility levels.

    This class defines the possible visibility levels that can be used to control
    access or exposure within an application. It provides predefined constants
    that correspond to specific visibility states.

    :ivar PUBLIC: Represents public visibility where content is accessible to
        everyone.
    :type PUBLIC: str
    :ivar PRIVATE: Represents private visibility where content is accessible
        only to the owner.
    :type PRIVATE: str
    :ivar FOLLOWERS: Represents visibility restricted to followers of the owner.
    :type FOLLOWERS: str
    :ivar HIVE: Represents visibility limited to a specific group/community
        called a "hive".
    :type HIVE: str
    :ivar CLIQUE: Represents visibility restricted to a smaller, more intimate
        group, referred to as a "clique".
    :type CLIQUE: str
    """
    PUBLIC = "public"
    PRIVATE = "private"
    FOLLOWERS = "followers"
    HIVE = "hive"
    CLIQUE = "clique"


class TicketType(Enum):
    """
    Represents types of tickets available for an event.

    This class is an enumeration that defines two types of tickets:
    GENERAL_ADMISSION and VIP. It is used to categorize ticket types
    and provide a simple way to differentiate ticket levels in an
    event management system.

    :ivar GENERAL_ADMISSION: Represents a general admission ticket type.
    :type GENERAL_ADMISSION: str
    :ivar VIP: Represents a VIP ticket type.
    :type VIP: str
    """
    FREE = "free"
    GENERAL_ADMISSION = "general_admission"
    VIP = "vip"


class TicketStatus(Enum):
    """
    Represents various statuses for tickets.

    This class is an enumeration that defines a set of symbolic names for
    different ticket statuses such as availability, sold out, reserved, and
    cancelled. It can be used to standardize the representation of these
    statuses across an application or program.

    :cvar AVAILABLE: Represents a ticket status indicating that the ticket
        is available for purchase.
    :cvar SOLD_OUT: Represents a ticket status indicating that all tickets
        are sold out.
    :cvar RESERVED: Represents a ticket status indicating that the ticket
        has been reserved.
    :cvar CANCELLED: Represents a ticket status indicating that the ticket
        has been cancelled.
    """
    AVAILABLE = "available"
    SOLD_OUT = "sold_out"
    RESERVED = "reserved"
    CANCELLED = "cancelled"


class RecommendationType(Enum):
    """
    Represents the type of recommendations categorized as OLD or NEW.

    This Enum class is used to define and enforce specific recommendation
    types within a system or application, ensuring consistency and avoiding
    the use of arbitrary strings or values.

    :ivar OLD: Represents the 'old' type recommendation.
    :type OLD: str
    :ivar NEW: Represents the 'new' type recommendation.
    :type NEW: str
    """
    OLD = "old"
    NEW = "new"


class ContentType(Enum):
    """
    Enumeration of various content types.

    This class represents a list of predefined content types that can
    be used to identify or categorize different pieces of content.
    Each content type is mapped to a specific string identifier.

    :ivar FILM: Represents a film content type.
    :type FILM: str
    :ivar ALBUM: Represents an album content type.
    :type ALBUM: str
    :ivar HITLIST: Represents a hitlist content type.
    :type HITLIST: str
    :ivar ARTICLE: Represents an article content type.
    :type ARTICLE: str
    :ivar POST: Represents a 'post' content type.
    :type POST: str
    :ivar CLIP: Represents a clip content type.
    :type CLIP: str
    :ivar REPORT: Represents a report content type.
    :type REPORT: str
    :ivar MAGAZINE: Represents a magazine content type.
    :type MAGAZINE: str
    :ivar PERSON: Represents a 'person' content type.
    :type PERSON: str
    :ivar COLUMN: Represents a column content type.
    :type COLUMN: str
    :ivar FANDOM: Represents a fandom content type.
    :type FANDOM: str
    :ivar CLUB: Represents a club content type.
    :type CLUB: str
    :ivar LISTING: Represents a listing content type.
    :type LISTING: str
    """
    FILM = "film"
    ALBUM = "album"
    HITLIST = "hitlist"
    ARTICLE = "article"
    POST = "post"
    CLIP = "clip"
    REPORT = "report"
    MAGAZINE = "magazine"
    PERSON = "person"
    COLUMN = "column"
    FANDOM = "fandom"
    CLUB = "club"
    LISTING = "listing"
