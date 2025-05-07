from enum import Enum

class FilmType(Enum):
    MOVIE = "Movie"
    TV_EPISODE = "TV Episode"
    YOUTUBE_VIDEO = "YouTube Video"
    SHORT = "Short"


class RelationshipType(Enum):
    """
    Enumeration for representing various types of relationships.

    This class provides a standardized set of values to classify different
    types of relationships within a domain model or relational data
    structures. It enables clear and consistent representation across
    applications that operate on relationship identification or analysis.
    """
    SIBLING = "Sibling"
    PARENT = "Parent"
    CHILD = "Child"
    STEP_PARENT = "Step-Parent"
    STEP_SIBLING = "Step-Sibling"
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
