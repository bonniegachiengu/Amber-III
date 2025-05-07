from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.extensions import db

def make_contribution_table(model_name: str, target_tablename: str) -> Table:
    """
    Generates an SQLAlchemy ` Table ` object that defines a contribution table for the
    specified model and target table. The table is dynamically configured based on
    the provided model name and target table name. It contains two primary key
    columns: one referencing the portfolio ID and the other referencing the ID of
    the specified model.

    :param model_name: The name of the model (e.g., 'User', 'Project'). This will be
        used to customize the table and column names dynamically.
    :param target_tablename: The name of the target table to which the second
        primary key column will reference.
    :return: A dynamically created SQLAlchemy `Table` object specifying the
        contribution table structure.
    :rtype: sqlalchemy.sql.schema.Table
    """
    return Table(
        f"{model_name.lower()}_contributors",
        db.metadata,
        Column("portfolio_id", ForeignKey("portfolio.id"), primary_key=True),
        Column(f"{model_name.lower()}_id", ForeignKey(f"{target_tablename}.id"), primary_key=True),
    )
