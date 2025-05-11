from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..library import Film, Album, Hitlist, Person
    from ..commerce import Listing, Merchandise
    from ..journal import (
        Writer, Analyst, Columnist, Correspondent, Editor, ChiefEditor, ChiefCorrespondent, ChiefAnalyst,
        ExecutiveEditor, EditorInChief, Magazine, Report, Article, Column, Journal
    )
    from ..community import (
        Fan, Subscriber, Member, Organizer, Creator, Post, Clip, Fandom, Club, Arena
    )


class FilmTypeEnum(Enum):
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
    MINISERIES_EPISODE = "MiniSeries Episode"
    YOUTUBE_VIDEO = "YouTube Video"
    SHORT = "Short"


class RelationshipTypeEnum(Enum):
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



class EventTypeEnum(Enum):
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


class EventRepeatEnum(Enum):
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


class EventStatusEnum(Enum):
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


class SubmissionStatusEnum(Enum):
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


class OrderStatusEnum(Enum):
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


class TransactionStatusEnum(Enum):
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

class TransactionTypeEnum(Enum):
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


class VisibilityEnum(Enum):
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


class TicketTypeEnum(Enum):
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


class TicketStatusEnum(Enum):
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


class RecommendationTypeEnum(Enum):
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


class ContentTypeEnum(Enum):
    """
    Enumeration for various content types.

    This enumeration defines a set of content types used to categorize different
    kinds of content into specific categories. Each member of the enumeration
    represents a unique category that can be assigned to content within a
    structured application context.

    :ivar FILM: Represents a film category.
    :ivar ALBUM: Represents an album category.
    :ivar HITLIST: Represents a hitlist category.
    :ivar ARTICLE: Represents an article category.
    :ivar POST: Represents a post-category.
    :ivar CLIP: Represents a clip category.
    :ivar REPORT: Represents a report category.
    :ivar MAGAZINE: Represents a magazine category.
    :ivar PERSON: Represents a person category.
    :ivar COLUMN: Represents a column category.
    :ivar FANDOM: Represents a fandom category.
    :ivar CLUB: Represents a club category.
    :ivar LISTING: Represents a listing category.
    :ivar MERCHANDISE: Represents a merchandise category.
    :type FILM: ContentTypeEnum
    :type ALBUM: ContentTypeEnum
    :type HITLIST: ContentTypeEnum
    :type ARTICLE: ContentTypeEnum
    :type POST: ContentTypeEnum
    :type CLIP: ContentTypeEnum
    :type REPORT: ContentTypeEnum
    :type MAGAZINE: ContentTypeEnum
    :type PERSON: ContentTypeEnum
    :type COLUMN: ContentTypeEnum
    :type FANDOM: ContentTypeEnum
    :type CLUB: ContentTypeEnum
    :type LISTING: ContentTypeEnum
    :type MERCHANDISE: ContentTypeEnum
    """
    FILM = Film
    ALBUM = Album
    HITLIST = Hitlist
    ARTICLE = Article
    POST = Post
    CLIP = Clip
    REPORT = Report
    MAGAZINE = Magazine
    PERSON = Person
    COLUMN = Column
    FANDOM = Fandom
    CLUB = Club
    LISTING = Listing
    MERCHANDISE = Merchandise


class ArticleReportStatusEnum(Enum):
    """
    Defines the various statuses an article report can have.

    This class contains a set of constants that represent the possible
    statuses for an article report. These statuses can be used to
    track the state of an article over its lifecycle within a system
    that manages article publishing.

    :ivar UNPUBLISHED: Indicates that the article has not been published yet.
    :type UNPUBLISHED: str
    :ivar PUBLISHED: Indicates that the article has been published.
    :type PUBLISHED: str
    :ivar REJECTED: Indicates that the article has been rejected during review.
    :type REJECTED: str
    :ivar APPROVED: Indicates that the article has been approved but not
        yet published.
    :type APPROVED: str
    :ivar SCHEDULED: Indicates that the article publication is scheduled for
        a later time.
    :type SCHEDULED: str
    :ivar DELETED: Indicates that the article has been deleted or removed.
    :type DELETED: str
    """
    UNPUBLISHED = "unpublished"
    PUBLISHED = "published"
    REJECTED = "rejected"
    APPROVED = "approved"
    SCHEDULED = "scheduled"
    DELETED = "deleted"


class CliqueTypeEnum(Enum):
    """
    Enumeration for different types within a clique.

    Provides a structured representation of various roles or designations
    that can exist within a group or organization. Can be utilized to
    categorize, differentiate, or apply specific logic based on these roles.

    :ivar FAN: A fan.
    :ivar SUBSCRIBER: A subscriber.
    :ivar MEMBER: A member.
    :ivar ORGANIZER: An organizer.
    :ivar WATCHER: A watcher.
    :ivar TRACKER: A tracker.
    :ivar CREATOR: A creator.
    :ivar COLLECTOR: A collector.
    :ivar WRITER: A writer.
    :ivar ANALYST: An analyst.
    :ivar COLUMNIST: A columnist.
    :ivar CORRESPONDENT: A correspondent.
    :ivar EDITOR: An editor.
    :ivar CHIEF_EDITOR: A chief editor.
    :ivar CHIEF_CORRESPONDENT: A chief correspondent.
    :ivar CHIEF_ANALYST: A chief analyst.
    :ivar EXECUTIVE_EDITOR: An executive editor.
    :ivar EDITOR_IN_CHIEF: An editor-in-chief.
    """
    FAN = Fan
    SUBSCRIBER = Subscriber
    MEMBER = Member
    ORGANIZER = Organizer
    WATCHER = Watcher
    TRACKER = Tracker
    CREATOR = Creator
    COLLECTOR = Collector
    WRITER = Writer
    ANALYST = Analyst
    COLUMNIST = Columnist
    CORRESPONDENT = Correspondent
    EDITOR = Editor
    CHIEF_EDITOR = ChiefEditor
    CHIEF_CORRESPONDENT =  ChiefCorrespondent
    CHIEF_ANALYST = ChiefAnalyst
    EXECUTIVE_EDITOR = ExecutiveEditor
    EDITOR_IN_CHIEF =  EditorInChief


class HiveTypeEnum(Enum):
    """
    Represents an enumeration of various Hive types.

    This class is used to define specific types of Hives that can be used
    in different contexts. Each member of this enumeration represents a
    distinct Hive type.

    :ivar ARENA: Represents the Arena type of Hive.
    :ivar CLUB: Represents the Club type of Hive.
    :ivar MAGAZINE: Represents the Magazine type of Hive.
    :ivar COLUMN: Represents the Column type of Hive.
    :ivar FANDOM: Represents the Fandom type of Hive.
    :ivar JOURNAL: Represents the Journal type of Hive.
    """
    ARENA = Arena
    CLUB = Club
    MAGAZINE = Magazine
    COLUMN = Column
    FANDOM = Fandom
    JOURNAL = Journal


class ColumnStatusEnum(Enum):
    """
    Represents the status of a column in an enumeration format.

    This enumeration contains predefined values to categorize the state
    of a column. It is primarily used to standardize the status
    designation across different parts of a system and promote
    consistency in column state management.

    :cvar ACTIVE: Represents a column that is currently active and in use.
    :type ACTIVE: str
    :cvar ARCHIVED: Represents a column that is archived and no longer actively used.
    :type ARCHIVED: str
    """
    ACTIVE = "active"
    ARCHIVED = "archived"


# noinspection SpellCheckingInspection
class ExtensionTypeEnum(Enum):
    """
    Represents an enumeration of various file extension types.

    This class defines a set of common file extensions categorized under different types
    such as audio, video, document, image, subtitle, and more. Each enumerator corresponds
    to a specific file extension string value. The purpose is to provide a convenient
    and centralized way to handle these file extensions in code.

    :ivar MP3: Represents the file extension for MP3 audio files.
    :ivar MP4: Represents the file extension for MP4 video files.
    :ivar AVI: Represents the file extension for AVI video files.
    :ivar WMV: Represents the file extension for WMV video files.
    :ivar MOV: Represents the file extension for MOV video files.
    :ivar FLV: Represents the file extension for FLV video files.
    :ivar MKV: Represents the file extension for MKV video files.
    :ivar WEBM: Represents the file extension for WEBM video files.
    :ivar OGG: Represents the file extension for OGG audio files.
    :ivar WMA: Represents the file extension for WMA audio files.
    :ivar AAC: Represents the file extension for AAC audio files.
    :ivar FLAC: Represents the file extension for FLAC audio files.
    :ivar WAV: Represents the file extension for WAV audio files.
    :ivar AIF: Represents the file extension for AIF audio files.
    :ivar AIFC: Represents the file extension for AIFC audio files.
    :ivar AIFF: Represents the file extension for AIFF audio files.
    :ivar PCM: Represents the file extension for PCM audio files.
    :ivar VORBIS: Represents the file extension for VORBIS audio files.
    :ivar ALAC: Represents the file extension for ALAC audio files.
    :ivar SRT: Represents the file extension for SRT subtitle files.
    :ivar TXT: Represents the file extension for TXT text files.
    :ivar HTML: Represents the file extension for HTML web files.
    :ivar CSS: Represents the file extension for CSS style files.
    :ivar JS: Represents the file extension for JavaScript files.
    :ivar XSL: Represents the file extension for XSL stylesheets.
    :ivar XSLT: Represents the file extension for XSLT files.
    :ivar XML: Represents the file extension for XML files.
    :ivar JSON: Represents the file extension for JSON files.
    :ivar CSV: Represents the file extension for CSV spreadsheet files.
    :ivar XLS: Represents the file extension for XLS Excel files.
    :ivar XLSX: Represents the file extension for XLSX Excel files.
    :ivar PPT: Represents the file extension for PPT PowerPoint files.
    :ivar PPTX: Represents the file extension for PPTX PowerPoint files.
    :ivar DOCX: Represents the file extension for DOCX Word document files.
    :ivar RTF: Represents the file extension for RTF Word document files.
    :ivar PDF: Represents the file extension for PDF files.
    :ivar ZIP: Represents the file extension for ZIP archived files.
    :ivar RAR: Represents the file extension for RAR archived files.
    :ivar M4V: Represents the file extension for M4V video files.
    :ivar VTT: Represents the file extension for VTT subtitle files.
    :ivar IMG: Represents the file extension for IMG image files.
    :ivar PNG: Represents the file extension for PNG image files.
    :ivar JPG: Represents the file extension for JPG image files.
    :ivar GIF: Represents the file extension for GIF image files.
    :ivar BMP: Represents the file extension for BMP image files.
    :ivar TIFF: Represents the file extension for TIFF image files.
    :ivar SVG: Represents the file extension for SVG image files.
    :ivar PSD: Represents the file extension for PSD design files.
    :ivar PPTA: Represents the file extension for PPTA PowerPoint files.
    :ivar PPTM: Represents the file extension for PPTM PowerPoint files.
    :ivar PPS: Represents the file extension for PPS PowerPoint slide files.
    :ivar PPSM: Represents the file extension for PPSM PowerPoint slide files.
    :ivar PPSX: Represents the file extension for PPSX PowerPoint slide files.
    :ivar PPSXM: Represents the file extension for PPSXM PowerPoint slide files.
    :ivar DOCM: Represents the file extension for DOCM Word document files.
    :ivar DOCMX: Represents the file extension for DOCMX Word document files.
    :ivar DOCXM: Represents the file extension for DOCXM Word document files.
    :ivar DOCXB: Represents the file extension for DOCXB Word document files.
    :ivar MPEG: Represents the file extension for MPEG video files.
    :ivar ASS: Represents the file extension for ASS subtitle files.
    :ivar SSA: Represents the file extension for SSA subtitle files.
    :ivar SUB: Represents the file extension for SUB subtitle files.
    :ivar DTT: Represents the file extension for DTT data files.
    :ivar DTTX: Represents the file extension for DTTX data files.
    :ivar DTTM: Represents the file extension for DTTM data files.
    :ivar IDX: Represents the file extension for IDX files associated with subtitles.
    :ivar ITA: Represents the file extension for ITA data files.
    :ivar JTA: Represents the file extension for JTA data files.
    :ivar MTA: Represents the file extension for MTA data files.
    :ivar OTHER: Represents the file extension for other file types.
    """
    MP3 = ".mp3"
    MP4 = ".mp4"
    AVI = ".avi"
    WMV = ".wmv"
    MOV = ".mov"
    FLV = ".flv"
    MKV = ".mkv"
    WEBM = ".webm"
    OGG = ".ogg"
    WMA = ".wma"
    AAC = ".aac"
    FLAC = ".flac"
    WAV = ".wav"
    AIF = ".aif"
    AIFC = ".aifc"
    AIFF = ".aiff"
    PCM = ".pcm"
    VORBIS = ".vorbis"
    ALAC = ".alac"
    SRT = ".srt"
    TXT = ".txt"
    HTML = ".html"
    CSS = ".css"
    JS = ".js"
    XSL = ".xsl"
    XSLT = ".xslt"
    XML = ".xml"
    JSON = ".json"
    CSV = ".csv"
    XLS = ".xls"
    XLSX = ".xlsx"
    PPT = ".ppt"
    PPTX = ".pptx"
    DOCX = ".docx"
    RTF = ".rtf"
    PDF = ".pdf"
    ZIP = ".zip"
    RAR = ".rar"
    M4V = ".m4v"
    VTT = ".vtt"
    IMG = ".img"
    PNG = ".png"
    JPG = ".jpg"
    GIF = ".gif"
    BMP = ".bmp"
    TIFF = ".tiff"
    SVG = ".svg"
    PSD = ".psd"
    PPTA = ".ppta"
    PPTM = ".pptm"
    PPS = ".pps"
    PPSM = ".ppsm"
    PPSX = ".ppsx"
    PPSXM = ".ppsxm"
    DOCM = ".docm"
    DOCMX = ".docmx"
    DOCXM = ".docxm"
    DOCXB = ".docxb"
    MPEG = ".mpeg"
    ASS = ".ass"
    SSA = ".ssa"
    SUB = ".sub"
    DTT = ".dtt"
    DTTX = ".dttx"
    DTTM = ".dttm"
    IDX = ".idx"
    ITA = ".ita"
    JTA = ".jta"
    MTA = ".mta"
    OTHER = ""


class AlbumTypeEnum(Enum):
    """
    Represents enumeration of different album types.

    This class defines various album types typically used in
    entertainment or media classification, such as cast albums,
    crew albums, studio albums, etc. It provides a fixed set
    of string values that can be used to categorize albums.

    :ivar CAST: Album type corresponding to cast-related albums.
    :type CAST: str
    :ivar CREW: Album type corresponding to crew-related albums.
    :type CREW: str
    :ivar STUDIO: Album type corresponding to studio-related albums.
    :type STUDIO: str
    :ivar FRANCHISE: Album type corresponding to franchise-related albums.
    :type FRANCHISE: str
    :ivar CINEMATIC_UNIVERSE: Album type corresponding to cinematic universe-related albums.
    :type CINEMATIC_UNIVERSE: str
    :ivar TV_SHOW: Album type corresponding to TV show-related albums.
    :type TV_SHOW: str
    :ivar MINISERIES: Album type corresponding to miniseries-related albums.
    :type MINISERIES: str
    :ivar SEASON: Album type corresponding to season-related albums.
    :type SEASON: str
    """
    CAST = "cast"
    CREW = "crew"
    STUDIO = "studio"
    FRANCHISE = "franchise"
    CINEMATIC_UNIVERSE = "cinematic_universe"
    TV_SHOW = "tv-show"
    MINISERIES = "miniseries"
    SEASON = "season"


class CrewTypeEnum(Enum):
    """
    An enumeration defining various crew roles in film production.

    This class defines a set of constants representing different crew
    roles across various departments in film production, such as direction,
    writing, camera, art, costume, post-production, sound, stunts, casting,
    and locations. Each constant is a string value denoting a specific role.

    :ivar EXECUTIVE_PRODUCER: Represents the role of an executive producer.
    :type EXECUTIVE_PRODUCER: str
    :ivar PRODUCER: Represents the role of a producer.
    :type PRODUCER: str
    :ivar LINE_PRODUCER: Represents the role of a line producer.
    :type LINE_PRODUCER: str
    :ivar UNIT_PRODUCTION_MANAGER: Represents the role of a unit production manager.
    :type UNIT_PRODUCTION_MANAGER: str
    :ivar DIRECTOR: Represents the role of a director.
    :type DIRECTOR: str
    :ivar FIRST_ASSISTANT_DIRECTOR: Represents the role of a first assistant director.
    :type FIRST_ASSISTANT_DIRECTOR: str
    :ivar SECOND_ASSISTANT_DIRECTOR: Represents the role of a second assistant director.
    :type SECOND_ASSISTANT_DIRECTOR: str
    :ivar SCRIPT_SUPERVISOR: Represents the role of a script supervisor.
    :type SCRIPT_SUPERVISOR: str
    :ivar PRODUCTION_ASSISTANT: Represents the role of a production assistant.
    :type PRODUCTION_ASSISTANT: str
    :ivar WRITER: Represents the role of a writer.
    :type WRITER: str
    :ivar CINEMATOGRAPHER: Represents the role of a cinematographer (Director
                          of Photography).
    :type CINEMATOGRAPHER: str
    :ivar GAFFER: Represents the role of a gaffer.
    :type GAFFER: str
    :ivar GRIP: Represents the role of a grip.
    :type GRIP: str
    :ivar BEST_BOY: Represents the role of a best boy.
    :type BEST_BOY: str
    :ivar PRODUCTION_DESIGNER: Represents the role of a production designer.
    :type PRODUCTION_DESIGNER: str
    :ivar ART_DIRECTOR: Represents the role of an art director.
    :type ART_DIRECTOR: str
    :ivar SET_DECORATOR: Represents the role of a set decorator.
    :type SET_DECORATOR: str
    :ivar PROP_MASTER: Represents the role of a prop master.
    :type PROP_MASTER: str
    :ivar COSTUME_DESIGNER: Represents the role of a costume designer.
    :type COSTUME_DESIGNER: str
    :ivar MAKEUP_ARTIST: Represents the role of a makeup artist.
    :type MAKEUP_ARTIST: str
    :ivar HAIR_STYLIST: Represents the role of a hair stylist.
    :type HAIR_STYLIST: str
    :ivar EDITOR: Represents the role of an editor.
    :type EDITOR: str
    :ivar VISUAL_EFFECTS_SUPERVISOR: Represents the role of a visual effects
                                     supervisor.
    :type VISUAL_EFFECTS_SUPERVISOR: str
    :ivar SPECIAL_EFFECTS_COORDINATOR: Represents the role of a special effects
                                       coordinator.
    :type SPECIAL_EFFECTS_COORDINATOR: str
    :ivar SOUND_DESIGNER: Represents the role of a sound designer.
    :type SOUND_DESIGNER: str
    :ivar COMPOSER: Represents the role of a composer.
    :type COMPOSER: str
    :ivar MUSIC_SUPERVISOR: Represents the role of a music supervisor.
    :type MUSIC_SUPERVISOR: str
    :ivar STUNT_COORDINATOR: Represents the role of a stunt coordinator.
    :type STUNT_COORDINATOR: str
    :ivar CASTING_DIRECTOR: Represents the role of a casting director.
    :type CASTING_DIRECTOR: str
    :ivar LOCATION_MANAGER: Represents the role of a location manager.
    :type LOCATION_MANAGER: str
    """
    # Executives & Producers
    EXECUTIVE_PRODUCER = "executive_producer"
    PRODUCER = "producer"
    LINE_PRODUCER = "line_producer"
    UNIT_PRODUCTION_MANAGER = "unit_production_manager"
    # Direction Department
    DIRECTOR = "director"
    FIRST_ASSISTANT_DIRECTOR = "first_assistant_director"
    SECOND_ASSISTANT_DIRECTOR = "second_assistant_director"
    SCRIPT_SUPERVISOR = "script_supervisor"
    PRODUCTION_ASSISTANT = "production_assistant"
    # Writing & Story
    WRITER = "writer"
    # Camera & Electrical
    CINEMATOGRAPHER = "cinematographer"  # aka Director of Photography
    GAFFER = "gaffer"
    GRIP = "grip"
    BEST_BOY = "best_boy"
    # Art Department
    PRODUCTION_DESIGNER = "production_designer"
    ART_DIRECTOR = "art_director"
    SET_DECORATOR = "set_decorator"
    PROP_MASTER = "prop_master"
    # Costume & Makeup
    COSTUME_DESIGNER = "costume_designer"
    MAKEUP_ARTIST = "makeup_artist"
    HAIR_STYLIST = "hair_stylist"
    # Post-Production
    EDITOR = "editor"
    VISUAL_EFFECTS_SUPERVISOR = "visual_effects_supervisor"
    SPECIAL_EFFECTS_COORDINATOR = "special_effects_coordinator"
    # Sound & Music
    SOUND_DESIGNER = "sound_designer"
    COMPOSER = "composer"
    MUSIC_SUPERVISOR = "music_supervisor"
    # Stunts
    STUNT_COORDINATOR = "stunt_coordinator"
    # Casting & Locations
    CASTING_DIRECTOR = "casting_director"
    LOCATION_MANAGER = "location_manager"

