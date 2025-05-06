from sqlalchemy import Table, Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID
from ..extensions import db


#------------------------ EVENT MODEL --------------------------------------------------------

# Association table for Event <-> User (Guests)
event_guests = Table(
    'event_guests',
    db.Column('event_id', UUID, db.ForeignKey('events.id'), primary_key=True),
    db.Column('user_id', UUID, db.ForeignKey('users.id'), primary_key=True)
)

# Association table for Event <-> Clique (Moderators)
event_moderators = Table(
    'event_moderators',
    db.Column('event_id', UUID, db.ForeignKey('events.id'), primary_key=True),
    db.Column('clique_id', UUID, db.ForeignKey('cliques.id'), primary_key=True)
)

#------------------------ "" MODEL --------------------------------------------------------
