import uuid
from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..extensions import db
from .associations import fandom_contributors, club_contributors
from .mixins import (
    EntityMixin, HiveMixin, CliqueMixin, CreatedMixin, ListMixin, ScrollItemMixin, OwnedMixin, ContentMixin, FanMixin,
    FoundedMixin, ModelMixin, PerksMixin, BoardMixin, WallMixin, MarkMixin, ContributionMixin, AnalyzedMixin
)

if TYPE_CHECKING:
    from user import User
    from .library import Library, Win
    from .commerce import Fund
    from .calendar import Event


class Arena(db.Model, ModelMixin, EntityMixin, HiveMixin):
    """
    Represents an arena with specific properties and behaviors, including moderators.

    This class interacts with the database and provides functionality for managing
    the arena's data and related entities. It incorporates features and behaviors
    from the `db.Model`, `ModelMixin`, `EntityMixin`, and `HiveMixin` classes or
    mixins. The arena includes a relationship with the `Moderator` entity, allowing
    for bidirectional management of moderators associated with the arena.

    :ivar moderators: A list of moderators associated with the arena. This
        relationship is maintained with the `Moderator` entity and is
        bidirectionally linked through the `hive` attribute in `Moderator`.
    :type moderators: List[Moderator]
    """
    __tablename__ = "arena"
    moderators: Mapped[List["Moderator"]] = relationship("Moderator", back_populates="hive")


class Club(
    db.Model, ModelMixin, EntityMixin, HiveMixin, ContributionMixin, MarkMixin, FoundedMixin, OwnedMixin,
    AnalyzedMixin, CreatedMixin, FanMixin
):
    """
    A class representing a Club entity.

    The `Club` class is a data model associated with a database table named "clubs". It integrates
    with various mixins to provide extended functionality, including contributions handling,
    ownership, fan interactions, moderation, and more. Clubs can have moderators who are
    associated with them through defined relationships.

    :ivar moderators: List of Moderator entities associated with the club via a relationship.
    :type moderators: List[Moderator]
    """
    __tablename__ = "clubs"
    __contribution_table__ = club_contributors
    __contribution_backref__ = "club_contributions"
    moderators: Mapped[List["Moderator"]] = relationship("Moderator", back_populates="hive")


class Fandom(
    db.Model, ModelMixin, EntityMixin, HiveMixin, ContributionMixin, MarkMixin, FoundedMixin, AnalyzedMixin,
    CreatedMixin
):
    """
    Represents a Fandom within the application.

    The Fandom class models a community or group of individuals with shared interests.
    It serves as a way to organize and track contributions, events, and members like
    fans or moderators. Fandoms are uniquely identified by an entity ID and are linked
    to various other entities within the system.

    :ivar fans: List of fans associated with the fandom.
    :type fans: Optional[List[Fan]]
    :ivar moderators: List of moderators who manage the fandom.
    :type moderators: List[Moderator]
    :ivar entity_id: Unique identifier of the fandom entity.
    :type entity_id: uuid.UUID
    :ivar entity: Generic fan-related data linked to the fandom.
    :type entity: FanMixin
    """
    __tablename__ = "fandoms"
    __contribution_table__ = fandom_contributors
    __contribution_backref__ = "fandom_contributions"
    fans: Mapped[Optional[List["Fan"]]] = relationship("Fan", back_populates="fandom")
    moderators: Mapped[List["Moderator"]] = relationship("Moderator", back_populates="hive")
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    entity: Mapped["FanMixin"] = relationship("FanMixin", back_populates="fandom")


class Fan(db.Model, ModelMixin, CliqueMixin):
    """
    Represents a Fan within a specific fandom.

    This class is used to establish a many-to-many relationship between fans and
    the fandoms they are a part of. Each instance uniquely associates a fan with
    a particular fandom. It leverages SQLAlchemy for ORM and provides additional
    mixins for extended functionalities.

    :ivar fandom_id: Unique identifier for the fandom associated with the fan.
    :type fandom_id: uuid.UUID
    :ivar fan_id: Unique identifier for the fan within the context of the library.
    :type fan_id: uuid.UUID
    :ivar fandom: Relationship to the associated Fandom object, which represents
        the fandom details.
    :type fandom: Fandom
    :ivar fan: Relationship to the associated Library object, which represents
        the fan's details or membership library.
    :type fan: Library
    """
    __tablename__ = "fans"
    fandom_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("fandoms.id"), primary_key=True)
    fan_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), primary_key=True)
    fandom: Mapped["Fandom"] = relationship("Fandom", back_populates="fans")
    fan: Mapped["Library"] = relationship("Library", back_populates="fandoms")


class Thread(db.Model, ModelMixin):
    """
    Represents a discussion thread in a forum or messaging application.

    This class models a thread that belongs to a specific topic, with
    participants that engage in the discussion and associated messages
    that are exchanged within the thread.

    :ivar topic_id: Unique identifier of the topic associated with the thread.
    :type topic_id: uuid.UUID
    :ivar participants: List of users who are participants in the thread.
    :type participants: List[User]
    :ivar messages: Collection of messages exchanged in the thread.
    :type messages: List[Message]
    """
    __tablename__ = "threads"
    topic_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    participants: Mapped[List["User"]] = relationship("User", secondary="threads")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="thread")


class Message(db.Model, ModelMixin):
    """
    Represents a message in a conversation thread.

    The Message class is used to handle individual messages within a conversation
    thread. Each message is associated with a thread and has a sender. It is used
    to store and manage the content of the message and its relationships to
    other related entities such as replies and reactions.

    :ivar thread_id: The unique identifier of the thread this message belongs
        to.
    :type thread_id: uuid.UUID
    :ivar sender_id: The unique identifier of the user who sent the message.
    :type sender_id: uuid.UUID
    :ivar message: The content of the message, restricted to a maximum of 500
        characters.
    :type message: str
    :ivar thread: The thread object that this message is part of.
    :type thread: Thread
    :ivar sender: The sender of the message, represented as a User object.
    :type sender: User
    :ivar replies: A list of Reply objects associated with this message.
    :type replies: List[Reply]
    :ivar reactions: A list of Reaction objects associated with this message.
    :type reactions: List[Reaction]
    """
    __tablename__ = "messages"
    thread_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("threads.topic_id"), primary_key=True)
    sender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    message: Mapped[str] = mapped_column(String(500))
    thread: Mapped["Thread"] = relationship("Thread", back_populates="messages")
    sender: Mapped["User"] = relationship("User", foreign_keys=[sender_id])
    replies: Mapped[List["Reply"]] = relationship("Reply", back_populates="parent_message")
    reactions: Mapped[List["Reaction"]] = relationship("Reaction", back_populates="message")

    __mapper_args__ = {
        "polymorphic_identity": "message",
        "polymorphic_on": type,
    }


class Reply(db.Model, ModelMixin, Message):
    """
    Represents a reply to a message in the system.

    This class models the reply entity, which is associated with a parent message.
    It manages the reply content and provides relationships to its parent message.
    It extends `db.Model`, `ModelMixin`, and `Message` to integrate with the database
    and existing message-related functionalities.

    :ivar parent_message_id: The ID of the parent message to which this reply belongs.
    :type parent_message_id: uuid.UUID
    :ivar parent_message: The parent message object that this reply references.
    :type parent_message: Message
    :ivar reply: The textual content of the reply, with a maximum length of 500 characters.
    :type reply: str
    """
    parent_message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("messages.id"), primary_key=True)
    parent_message: Mapped["Message"] = relationship("Message", foreign_keys=[parent_message_id], back_populates="replies")
    reply: Mapped[str] = mapped_column(String(500))

    __mapper_args__ = {
        "polymorphic_identity": "reply",
    }


class Reaction(db.Model, ModelMixin, Message):
    """
    Represents a reaction to a message in the system.

    This class defines a Reaction model that associates a specific reaction with a
    parent message. It also serves as an extension of the base Message class,
    enabling polymorphic behavior and integration with the database. Reactions
    can be used to represent user interactions such as likes, emojis, or
    other forms of responses to a message.

    :ivar parent_message_id: The unique identifier of the parent message this
                            reaction is associated with.
    :type parent_message_id: uuid.UUID
    :ivar parent_message: The parent message entity linked to this reaction.
    :type parent_message: Message
    :ivar reaction: The type or content of the reaction (e.g., emoji or text
                    describing the reaction).
    :type reaction: str
    """
    parent_message_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("messages.id"), primary_key=True)
    parent_message: Mapped["Message"] = relationship("Message", foreign_keys=[parent_message_id], back_populates="reactions")
    reaction: Mapped[str] = mapped_column(String(100))

    __mapper_args__ = {
        "polymorphic_identity": "reaction",
    }


class Contributor(db.Model, ModelMixin):
    """
    Represents a contributor to a specific fund, linking libraries with their respective funds.

    This class serves as the database model for the relationship between a library and a
    fund, identifying which library makes contributions to a specific fund. It facilitates
    bidirectional relationships with the `Library` and `Fund` models for managing data.

    :ivar contributor_id: Unique identifier for the contributor, referencing a library ID.
    :type contributor_id: uuid.UUID
    :ivar contributions_fund_id: Unique identifier for the fund being contributed to, referencing a fund ID.
    :type contributions_fund_id: uuid.UUID
    :ivar contributor: Represents the relation to the `Library` model, linking a contributor entity.
    :type contributor: Library
    :ivar contributions_fund: Represents the relation to the `Fund` model, linking the associated fund.
    :type contributions_fund: Fund
    """
    __tablename__ = "contributors"
    contributor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), primary_key=True)
    contributions_fund_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("funds.id"), primary_key=True)
    contributor: Mapped["Library"] = relationship(back_populates="contributions")
    contributions_fund: Mapped["Fund"] = relationship("Fund")


class Subscriber(db.Model, ModelMixin, CliqueMixin):
    """
    Represents a subscription relationship between tiers and libraries.

    This class defines a mapping for the "subscribers" table, which links tiers to
    libraries, representing a subscriber relationship. It uses SQLAlchemy's ORM
    capabilities to define the relationships between the 'Tier' and 'Library' models.
    This helps manage the subscriptions and provides mechanisms to query and manipulate
    subscriber data in the database effectively.

    :ivar tier_id: ID of the tier being subscribed to.
    :type tier_id: uuid.UUID
    :ivar subscriber_id: ID of the subscriber (library).
    :type subscriber_id: uuid.UUID
    :ivar tier: Relationship to the ``Tier`` model, back-referencing the ``subscribers``
        relationship on ``Tier``.
    :type tier: Tier
    :ivar subscriber: Relationship to the ``Library`` model, back-referencing the
        ``subscriptions`` relationship on ``Library``.
    :type subscriber: Library
    """
    __tablename__ = "subscribers"
    tier_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tiers.hive_id"), primary_key=True)
    subscriber_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), primary_key=True)
    tier: Mapped["Tier"] = relationship("Tier", back_populates="subscribers")
    subscriber: Mapped["Library"] = relationship("Library", back_populates="subscriptions")


class Moderator(db.Model, ModelMixin, CliqueMixin):
    """
    Represents a Moderator entity, with attributes and relationships.

    The Moderator class is a data model representing moderators in the system. It
    includes relationships to other entities such as hives, boards, and walls. This
    class is a part of a relational database schema and leverages SQLAlchemy for
    ORM mapping. It is designed to be used in conjunction with certain mixins
    (ModelMixin and CliqueMixin) to extend functionality and behavior as required.

    :ivar hive_id: Unique identifier of the hive that the moderator belongs to.
    :type hive_id: uuid.UUID
    :ivar hive: The HiveMixin instance representing the hive connected to this
        moderator.
    :type hive: HiveMixin
    :ivar boards: A list of BoardMixin instances associated with the moderator.
    :type boards: List[BoardMixin]
    :ivar walls: A list of WallMixin instances associated with the moderator.
    :type walls: List[WallMixin]
    """
    __tablename__ = "moderators"
    hive_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    hive: Mapped["HiveMixin"] = relationship(HiveMixin, back_populates="moderators")
    boards: Mapped[List["BoardMixin"]] = relationship("BoardMixin", back_populates="moderators")
    walls: Mapped[List["WallMixin"]] = relationship("WallMixin", back_populates="moderators")


class Creator(db.Model, ModelMixin, CliqueMixin):
    """
    Represents a class that models creators within the database.

    This class is a database model that handles creators, their related creations,
    and associated licenses. It integrates functionality from database base models
    as well as mixins for additional functionalities. It defines relationships
    between creators and their creations. The license attribute stores specific
    licensing information in a JSONB field format.

    :ivar creations: A list relationship mapping the creations associated with
        the creator.
    :type creations: List[CreatedMixin]
    :ivar licenses: A dictionary column storing license metadata for the creator.
        Defaults to an empty dictionary.
    :type licenses: dict
    """
    __tablename__ = "creators"
    creations: Mapped[List["CreatedMixin"]] = relationship("CreatedMixin", back_populates="creators")
    licenses: Mapped[dict] = mapped_column(JSONB, default={})


class Owner(db.Model, ModelMixin, CliqueMixin):
    """
    Represents an Owner entity within the database.

    The Owner class serves as a model for the "owners" table, handling database
    interactions related to owner entries. It facilitates relationships between
    owners and instances of OwnedMixin via the `holdings` attribute.

    :ivar holdings: List of associated `OwnedMixin` entities. Represents the
        relationship where an owner can have multiple holdings.
    :type holdings: List[OwnedMixin]
    """
    __tablename__ = "owners"
    holdings: Mapped[List["OwnedMixin"]] = relationship("OwnedMixin", back_populates="owners")


class Founder(db.Model, ModelMixin, CliqueMixin):
    """
    Represents a Founder entity within the system.

    This class inherits from `db.Model`, `ModelMixin`, and `CliqueMixin`, providing database
    management and additional functionality. The class is connected to `FoundedMixin`
    via a relationship, enabling interaction and navigation between related entities in the system.

    :ivar foundlings: List of `FoundedMixin` instances associated with the founder.
    :type foundlings: List[FoundedMixin]
    """
    __tablename__ = "founders"
    foundlings: Mapped[List["FoundedMixin"]] = relationship("FoundedMixin", back_populates="founders")


class Tier(db.Model, ModelMixin):
    """
    Represents a Tier in a system, which includes relationships to other entities
    and contains attributes associated with the tier functionality.

    The Tier class models tiers in a hierarchy, providing attributes for the
    associated hive, perks belonging to the tier, subscribers, and members. It
    establishes relationships to multiple other models, representing the
    connection between tiers and various system components.

    :ivar hive_id: The unique identifier of the hive associated with this tier.
    :type hive_id: uuid.UUID
    :ivar hive: The hive entity associated with this tier.
    :type hive: HiveMixin
    :ivar perks: The list of perks associated with this tier.
    :type perks: List[PerksMixin]
    :ivar subscribers: The list of subscribers related to this tier, if any.
    :type subscribers: Optional[List[Subscriber]]
    :ivar members: The list of members associated with this tier, if any.
    :type members: Optional[List[Member]]
    """
    __tablename__ = "tiers"
    hive_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    hive: Mapped["HiveMixin"] = relationship(HiveMixin, back_populates="tiers")
    perks: Mapped[List["PerksMixin"]] = relationship("PerksMixin", back_populates="tier")
    subscribers: Mapped[Optional[List["Subscriber"]]] = relationship("Subscriber", back_populates="tier")
    members: Mapped[Optional[List["Member"]]] = relationship("Member", back_populates="tier")


class Member(db.Model, ModelMixin, CliqueMixin):
    """
    Represents a Member entity within the database.

    The Member class serves as a representation of a membership-binding entity.
    Each instance links a library to a tier, forming connections that define
    group memberships and their associated tiers. This class also supports
    object-relational mapping using SQLAlchemy, ensuring seamless integration
    with the database schema.

    :ivar tier_id: The unique identifier of the associated tier for the member.
    :type tier_id: uuid.UUID
    :ivar member_id: The unique identifier of the library/member.
    :type member_id: uuid.UUID
    :ivar tier: Relationship to the Tier entity, indicating the tier associated
        with this member.
    :type tier: Tier
    :ivar member: Relationship to the Library entity, indicating the library
        associated with this membership.
    :type member: Library
    """
    __tablename__ = "members"
    tier_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tiers.hive_id"), primary_key=True)
    member_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), primary_key=True)
    tier: Mapped["Tier"] = relationship("Tier", back_populates="members")
    member: Mapped["Library"] = relationship("Library", back_populates="memberships")


class Organizer(db.Model, ModelMixin, CliqueMixin):
    """
    Represents an organized entity within the system.

    This class is designed to function as part of the database model for organizers. It integrates
    with SQLAlchemy and custom mixins to handle data persistence and enhance functionality. Each
    organizer can have multiple associated events, represented with a one-to-many relationship.

    :ivar __tablename__: Name of the corresponding database table.
    :type __tablename__: str
    :ivar events: List of events related to the organizer.
    :type events: List[Event]
    """
    __tablename__ = "organizers"
    events: Mapped[List["Event"]] = relationship("Event", back_populates="organizers")


class Reward(db.Model, ModelMixin, PerksMixin):
    """
    Represents a reward in the system.

    This class is used to define a reward object with its associated data and
    relationships. It is a database model that integrates with SQLAlchemy to handle
    database interactions. Rewards may have associated wins that are linked through
    a relationship, allowing for efficient query capabilities. This model is
    integrated with other mixins for extended functionalities.

    :ivar reward_data: JSON representation of reward-specific data.
    :type reward_data: dict
    :ivar wins: List of Win objects associated with this reward.
    :type wins: List[Win]
    """
    __tablename__ = "rewards"
    reward_data: Mapped[dict] = mapped_column(JSONB, default={})
    wins: Mapped[List["Win"]] = relationship("Win", back_populates="reward")


class Pins(db.Model, ModelMixin, BoardMixin):
    """
    Represents a board containing multiple pins.

    This class is a representation of a board in the system, which can hold a list
    of pins. It is designed to work with SQLAlchemy as a database model and includes
     a mixin functionality to provide additional board-specific and model-related
    features. The class establishes a one-to-many relationship where a board can
    be associated with multiple pins. Each pin is linked back to its respective board.

    :ivar pins: A relationship that represents the list of pins associated with this
        board. Each pin in the relationship will have a reference back to the board.
    :type pins: List[Pin]
    """
    __tablename__ = "pin_boards"
    pins: Mapped[List["Pin"]] = relationship("Pin", back_populates="board")


class Pin(db.Model, ModelMixin, ContentMixin, MarkMixin):
    """
    Represents the Pin model for managing pin data in the database.

    This class is used to define the structure of the Pin object, including its
    attributes and relationships with other database entities. It provides an
    interface to store and interact with data related to individual pins within
    a broader application context.

    :ivar board_id: A unique identifier for the board associated with the pin.
    :type board_id: uuid.UUID
    :ivar board: A relationship to the associated board, enabling
        navigation between pins and their parent board.
    :type board: Pins
    :ivar content: A JSON field to store additional information or metadata
        about the pin.
    :type content: dict
    """
    __tablename__ = "pins"
    board_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("pin_boards.id"), primary_key=True)
    board: Mapped["Pins"] = relationship("Pins", back_populates="pins")
    content: Mapped[dict] = mapped_column(JSONB, default={})


class Updates(db.Model, ModelMixin, BoardMixin):
    """
    Represents the Updates board model in the database.

    This class manages relationships and data regarding the boards of updates. It
    is part of the database ORM model, inheriting from base model classes and
    providing functionality to work with associated updates. The use of mixins
    enriches this class with additional features that are required to facilitate
    data handling and behavior specific to update boards.

    :ivar updates: A list of updates associated with the update board.
    :type updates: List[Update]
    """
    __tablename__ = "update_boards"
    updates: Mapped[List["Update"]] = relationship("Update", back_populates="board")


class Update(db.Model, ModelMixin, ContentMixin, MarkMixin):
    """
    Represents an update entity in the database.

    This class is used for managing and handling updates associated with a board. It
    provides a mapping to the database table `updates` and integrates mixins for content
    management, marking, and typical model operations. Each update is linked to a specific
    board using a foreign key relationship.

    :ivar board_id: The unique identifier of the associated board.
    :type board_id: uuid.UUID
    :ivar board: The board object associated with this update, represented as a
        relationship with the `Updates` model.
    :type board: Updates
    :ivar content: The content of the update, stored as a JSONB field. Defaults to an
        empty dictionary.
    :type content: dict
    """
    __tablename__ = "updates"
    board_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("update_boards.id"), primary_key=True)
    board: Mapped["Updates"] = relationship("Updates", back_populates="updates")
    content: Mapped[dict] = mapped_column(JSONB, default={})


class Issues(db.Model, ModelMixin, BoardMixin, ListMixin):
    """
    Represents a board for tracking issues.

    This class is a database model for managing issue boards. It provides
    relationships necessary for associating multiple issues with a single
    board. The table is represented in the database as "issue_boards".

    :ivar issues: List of issues associated with this board.
    :type issues: List[Issue]
    """
    __tablename__ = "issue_boards"
    issues: Mapped[List["Issue"]] = relationship("Issue", back_populates="board")


class Issue(db.Model, ModelMixin, ScrollItemMixin, MarkMixin, ContentMixin):
    """
    Represents an issue within a system.

    This class is used to manage data and relationships related to issues, which
    are part of a larger issue tracking board. It provides persistence using a
    database model and includes features for content management, scrolling,
    marking, and other supported behaviors. Content for each issue is stored
    in JSON format and can be customized.

    :ivar board_id: Unique identifier tied to the board this issue belongs to.
    :type board_id: uuid.UUID
    :ivar board: Relationship reference to the parent board that contains this issue.
    :type board: Issues
    :ivar content: JSON-structured content associated with the issue.
    :type content: dict
    """
    __tablename__ = "issues"
    board_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("issue_boards.id"), primary_key=True)
    board: Mapped["Issues"] = relationship("Issues", back_populates="issues")
    content: Mapped[dict] = mapped_column(JSONB, default={})


class Posts(db.Model, ModelMixin, WallMixin):
    """
    Represents a collection of posts associated with a specific wall.

    This class serves as a model for a database table that organizes posts into
    collections designated as "walls". It manages relationships with individual
    posts and uses multiple mixins to integrate functionality for database
    operations and wall-related behavior.

    :ivar posts: A list of posts associated with this wall.
    :type posts: list[Post]
    """
    __tablename__ = "post_walls"
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="wall")


class Post(db.Model, ModelMixin):
    """
    Represents a Post in the application.

    This class models a post-entity with attributes for an associated wall,
    content stored as JSON data, and mechanisms for database relationships.

    :ivar wall_id: The unique identifier for the wall to which the post belongs.
    :type wall_id: uuid.UUID
    :ivar wall: The relationship linking to the wall entity associated with the post.
    :type wall: Posts
    :ivar content: The content of the post is represented as a JSON object.
    :type content: dict
    """
    __tablename__ = "posts"
    wall_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("post_walls.id"), primary_key=True)
    wall: Mapped["Posts"] = relationship("Posts", back_populates="posts")
    content: Mapped[dict] = mapped_column(JSONB, default={})


class Clips(db.Model, ModelMixin, WallMixin):
    """
    Represents a database model for clip walls.

    This class is an SQLAlchemy ORM model used to define and interact with the
    clip walls table in the database. It provides relationships and methods
    to manage associated clips efficiently.

    :ivar clips: List of clips associated with the clip wall.
    :type clips: List[Clip]
    """
    __tablename__ = "clip_walls"
    clips: Mapped[List["Clip"]] = relationship("Clip", back_populates="wall")


class Clip(db.Model, ModelMixin):
    """
    Represents a Clip model that interacts with the database, enabling storage and
    retrieval of clip-related data.

    This class is designed to represent clips and their properties, facilitating
    their integration with a broader system. It defines the relationships between
    a clip and its associated wall and manages the clip's contents represented
    as JSON data.

    :ivar wall_id: Unique identifier of the wall associated with the clip.
    :type wall_id: uuid.UUID
    :ivar wall: Relationship to the associated wall object.
    :type wall: Clips
    :ivar content: JSON representation of the clip's content data. Defaults to an
        empty dictionary.
    :type content: dict
    """
    __tablename__ = "clips"
    wall_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clip_walls.id"), primary_key=True)
    wall: Mapped["Clips"] = relationship("Clips", back_populates="clips")
    content: Mapped[dict] = mapped_column(JSONB, default={})

