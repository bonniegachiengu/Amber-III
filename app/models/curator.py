from typing import List

from sqlalchemy import String, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..extensions import db
from .utils.config import RecommendationTypeEnum
from .mixins import EntityMixin, ModelMixin, ContentMixin



class Curator(db.Model, ModelMixin, EntityMixin):
    """
    Represents a curator entity in the database.

    This class defines the blueprint for a curator, including its relationships
    with recommendations and exhibitions. It integrates functionalities provided
    by `db.Model`, `ModelMixin`, and `EntityMixin`. Instances of this class will
    typically represent a curator in the persistence layer, with relationships
    established to manage associations with related entities.

    :ivar recommendations: A list of recommendations associated with the curator.
    :type recommendations: List[RecommendationItem]
    :ivar exhibitions: A list of exhibitions associated with the curator.
    :type exhibitions: List[Exhibition]
    """
    __tablename__ = "curators"
    recommendations: Mapped[List["RecommendationItem"]] = relationship("RecommendationItem", back_populates="curator")
    exhibitions: Mapped[List["Exhibition"]] = relationship("Exhibition", back_populates="curator")


class RecommendationItem(db.Model, ModelMixin, ContentMixin):
    """
    Represents a recommendation item and its associated data stored in the database.

    This class serves as a database model for recommendations. Each recommendation is
    associated with a curator, has a specific type, and includes relationships to other
    related entities. It is used for managing recommendation items within the system.

    :ivar curator_id: Unique identifier for the curator associated with the recommendation.
    :type curator_id: UUID
    :ivar type: Type of the recommendation. This is represented using the RecommendationType enum.
    :type type: RecommendationTypeEnum
    :ivar curator: Relationship to the Curator entity. Represents the curator who created
        this recommendation.
    :type curator: Curator
    """
    __tablename__ = "recommendations"
    curator_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("curators.id"), nullable=False)
    type: Mapped[RecommendationTypeEnum] = mapped_column(SQLAlchemyEnum(RecommendationTypeEnum), nullable=False)
    curator: Mapped["Curator"] = relationship("Curator", back_populates="recommendations")


class Exhibition(db.Model, ModelMixin):
    """
    Represents a library exhibition in the system.

    This class is a database model that stores information about an exhibition, such as its title, filters,
    and associated curator. It is used for managing exhibitions and their attributes in the database.
    It includes relationships to other models, such as the "Curator" model.

    :ivar curator_id: The unique identifier of the curator managing this exhibition.
    :type curator_id: UUID
    :ivar title: The title of the exhibition.
    :type title: str
    :ivar filters: A dictionary containing filters for the exhibition, such as genres or minimum ratings.
    :type filters: dict
    :ivar curator: The relationship to the Curator model, allowing access to information about the curator.
    :type curator: Curator
    """
    __tablename__ = "exhibitions"
    curator_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("curators.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    filters: Mapped[dict] = mapped_column(JSONB, nullable=False) # e.g. {"genres": ["Sci-Fi"], "min_rating": 7}
    curator: Mapped["Curator"] = relationship("Curator", back_populates="exhibitions")
