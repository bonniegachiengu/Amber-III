import uuid
from typing import List, TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..extensions import db
from .mixins import ContributionMixin, ModelMixin, ListMixin, ScrollItemMixin
from .associations import scroll_contributors, scroll_entry_contributors

if TYPE_CHECKING:
    from .library import Portfolio


class Scroll(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a scroll object within an application.

    This class defines a `Scroll` model with attributes and relationships that allow for the
    representation of a scroll entity. It supports contributors, associations to a reviewer,
    and related list information. Additionally, this model can hold entries that are associated
    with a scroll and manage them as part of the entity. The scroll is capable of determining
    ranked films through its associated entries.

    :ivar reviewer_id: Unique identifier of the reviewer associated with this scroll. Can be null.
    :type reviewer_id: uuid.UUID
    :ivar list_id: Identifier for the list associated with this scroll. Can be null.
    :type list_id: uuid.UUID
    :ivar is_aggregate: Indicates whether this scroll is an aggregate of other data. Defaults to False.
    :type is_aggregate: bool
    :ivar reviewer: Relationship to the Portfolio entity representing the reviewer. Links to the "Portfolio" model.
    :type reviewer: Portfolio
    :ivar list: Relationship to the ListMixin entity representing the associated list. Links to the "ListMixin" model.
    :type list: ListMixin
    :ivar entries: List of ScrollEntry objects associated with this scroll. Entries define individual elements of the scroll.
    :type entries: List[ScrollEntry]
    """
    __tablename__ = "scrolls"
    __contribution_table__ = scroll_contributors
    __contribution_backref__ = "scroll_contributions"
    reviewer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("libraries.id"), nullable=True)
    list_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    is_aggregate: Mapped[bool] = mapped_column(Boolean, default=False)
    reviewer: Mapped["Portfolio"] = relationship("Portfolio", back_populates="reviewed_scrolls")
    list: Mapped["ListMixin"] = relationship("ListMixin", back_populates="scrolls")
    entries: Mapped[List["ScrollEntry"]] = relationship("ScrollEntry", back_populates="scroll", cascade="all, delete-orphan")

    def get_ranked_films(self) -> List["ScrollEntry"]:
        """
        Sorts and retrieves a list of item entries based on their rank in ascending order.

        This function assumes that the attribute `entries` is a collection of item objects
        or dictionaries that include a `rank` attribute or key. The ranked list is sorted
        using the ranks of the item entries where the lowest rank comes first.

        :raises AttributeError: If the ` entries ` attribute is not defined in the instance
            or if entries do not include a `rank` attribute or key.
        :return: A list of item entries sorted by their rank in ascending order.
        :rtype: list
        """
        return sorted(self.entries, key=lambda e: e.rank)


class ScrollEntry(db.Model, ModelMixin, ContributionMixin):
    """
    Represents a scroll entry in the system.

    This class models an entry in a scroll and includes its associated attributes,
    such as the rank and relationships to other database models like `Scroll` and
    `ScrollItemMixin`. It also provides methods and properties for computing scroll
    points and contextual points, though the latter is currently a placeholder.

    :ivar scroll_id: The unique identifier of the scroll this entry belongs to.
    :type scroll_id: uuid.UUID
    :ivar item_id: The unique identifier of the item in this entry.
    :type item_id: uuid.UUID
    :ivar rank: The rank of the entry within the scroll. Higher ranks may correspond
        to lower numeric values and determine the order of entries.
    :type rank: int
    :ivar scroll: The `Scroll` relationship associated with this entry. This allows
        accessing data related to the parent scroll.
    :type scroll: Scroll
    :ivar scroll_item: The `ScrollItemMixin` relationship associated with this entry.
        This represents the specific item within the scroll entry.
    :type scroll_item: ScrollItemMixin
    """
    __tablename__ = "scroll_entries"
    __contribution_table__ = scroll_entry_contributors
    __contribution_backref__ = "scroll_entry_contributions"
    scroll_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scrolls.id"), primary_key=True)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    scroll: Mapped["Scroll"] = relationship("Scroll", back_populates="entries")
    scroll_item: Mapped["ScrollItemMixin"] = relationship("ScrollItemMixin", back_populates="scroll_entries")

    def scroll_points(self) -> int:
        """
        Calculate the scroll points based on the number of entries in the scroll
        and the rank.

        The scroll points are determined as the difference between the total number
        of entries in the scroll and the rank, adjusted by adding one to the result.
        This calculation is useful for ranking or leaderboard systems.

        :return: The calculated scroll points.
        :rtype: int
        """
        return (len(self.scroll.entries) - self.rank) + 1

    @property
    def contextual_points(self) -> dict:
        """
        A property to represent contextual points derived from specific attributes such
        as markers, metadata clusters, tags, or keywords. Currently, the property serves
        as a placeholder and always returns an empty dictionary. The logic for its
        calculation or retrieval is planned for future implementation.

        :return: An empty dictionary representing the contextual points.
        :rtype: dict
        """
        # Placeholder: in the future, calculate based on markers (tags, keywords, ers, etc.)/metadata clusters
        return {}

# TODO: Scroll
# - Add utility methods for aggregating scrollpoints.
# - Add logic for contextual points (genre, year, etc.)
# - Consider caching points for efficiency.
# - Explore storing Scroll->Tag, Scroll->Metadata associations.
