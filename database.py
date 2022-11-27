"""
This poorly named module will represent the database schema for the junta app.

..module:: database
..modulauthor:: Richard
:synopsis: Database definition and schema
"""
import os

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

try:
    # I'm open to suggestions on how to better check for postgres availability
    # pylint: disable=unused-import
    import psycopg2

    # Hardcoding this, which may be wrong:
    CONN_STRING = f'postgresql+psycopg2://{os.environ["PG_USER"]}:{os.environ["PG_PASSWORD"]}/junta'
except ImportError:
    # Assume SQLite
    CONN_STRING = "sqlite:///junta.db"

# Thes two warnings are ignored due to standard SQLAlchemy convention
# pylint: disable=invalid-name
engine = create_engine(CONN_STRING)
# pylint: disable=invalid-name
Base = declarative_base()
# pylint: disable=invalid-name
Session = sessionmaker(bind=engine)

# This is due to the standard way that SQLAlchemy schemas are defined
# pylint: disable=too-few-public-methods
class User(Base):
    """
    This is a SQLAlchemy class which represents a user, who has preferences.
    """

    __tablename__ = "users"

    user_idx = Column(Integer, primary_key=True)
    name = Column(String)
    # TODO consider changing this to class-object derived
    preferences = relationship("Preference")


# This is due to the standard way that SQLAlchemy schemas are defined
# pylint: disable=too-few-public-methods
class Preference(Base):
    """
    This is a SQLAlchemy class which represents a user's preferences for
    restaurants.
    """

    __tablename__ = "preferences"

    pref_idx = Column(Integer, primary_key=True)
    user_idx = Column(Integer, ForeignKey("users.user_idx"))
    restaurant_idx = Column(Integer, ForeignKey("restaurants.rest_idx"))
    # TODO consider changing this to class-object derived
    restaurant = relationship("Restaurant")
    vote = Column(String)


# This is due to the standard way that SQLAlchemy schemas are defined
# pylint: disable=too-few-public-methods
class Restaurant(Base):
    """
    This is a SQLAlchemy class which represents a restaurant.
    """

    __tablename__ = "restaurants"

    rest_idx = Column(Integer, primary_key=True)
    name = Column(String)


def initialize_database():
    """
    This funtion will wipe out the existing database, create the schema, and
    (for now) inject some default values.
    """
    # Create the schema
    Base.metadata.create_all(engine)

    # Create a connection/database session
    session = Session()

    # Now, create a few restaurants:
    cupcake = Restaurant(name="Cupcakes")
    five_guys = Restaurant(name="Five Guys")
    ihop = Restaurant(name="IHOP")

    # And a few users:
    mike = User(name="Mike")
    ryan = User(name="Ryan")

    # And finally a few votes:
    mike.preferences.append(Preference(vote="+1", restaurant=five_guys))
    ryan.preferences.append(Preference(vote="+0", restaurant=five_guys))
    ryan.preferences.append(Preference(vote="-0", restaurant=cupcake))

    session.add(mike)
    session.add(ryan)
    session.add(ihop)

    session.commit()

    session.close()


if __name__ == "__main__":
    initialize_database()
