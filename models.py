# -*- coding: utf-8 -*-
# pylint: disable=C0103
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Float, Table
from sqlalchemy.orm import relationship
from database import BASE as ORM_BASE


# http://stackoverflow.com/questions/5756559/how-to-build-many-to-many-relations-using-sqlalchemy-a-good-example
SET_PIECE_LIST = Table(
    'setpiecelist', ORM_BASE.metadata,
    Column('contest_id', Integer, ForeignKey('contests.id')),
    Column('set_piece_id', Integer, ForeignKey('test_pieces.id')))


class Constant(object):
    BAND_TYPE = ['社會業餘', '大專', '高中職', '國中', '國小']


class Area(ORM_BASE):
    __tablename__ = 'areas'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)


class Band(ORM_BASE):
    __tablename__ = 'bands'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    location = relationship('Location')
    band_type = Column(String(50))
    website = Column(Text)
    facebook = Column(Text)
    description = Column(Text)


class Contest(ORM_BASE):
    __tablename__ = 'contests'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    contest_type_id = Column(Integer, ForeignKey('contest_types.id'))
    contest_type = relationship('ContestType')
    name_prefix = Column(String(50))
    area_id = Column(Integer, ForeignKey('areas.id'))
    area = relationship('Area')
    category = Column(String(50))
    venue_id = Column(Integer, ForeignKey('venues.id'))
    venue = relationship('Venue')
    band_type = Column(String(50))
    set_pieces = relationship('TestPiece', secondary=SET_PIECE_LIST, backref='Contest')

    def get_fullname(self, prefix: bool = True, ctype: bool = True, area: bool = True, category: bool = True, band_type: bool = True) -> str:
        return '{}{}{}{}{}'.format(
            self.name_prefix if prefix else '',
            self.contest_type.name if ctype else '',
            self.area.name if area else '',
            self.band_type if band_type else '',
            ' {} 組'.format(self.category) if category else '')


class ContestDetail(ORM_BASE):
    __tablename__ = 'contest_details'
    id = Column(Integer, primary_key=True)
    band_id = Column(Integer, ForeignKey('bands.id'))
    band = relationship('Band')
    contest_id = Column(Integer, ForeignKey('contests.id'))
    contest = relationship('Contest')
    position = Column(Integer)
    points = Column(Float)
    playing_order = Column(Integer)
    ranking_id = Column(Integer, ForeignKey('rankings.id'))
    ranking = relationship('Ranking')
    conductor_id = Column(Integer, ForeignKey('persons.id'))
    conductor = relationship('Person')
    set_piece_id = Column(Integer, ForeignKey('test_pieces.id'))
    set_piece = relationship('TestPiece', foreign_keys=[set_piece_id])
    set_piece_recording = Column(String(100))
    own_choice_id = Column(Integer, ForeignKey('test_pieces.id'))
    own_choice = relationship('TestPiece', foreign_keys=[own_choice_id])
    own_choice_recording = Column(String(100))
    misc = Column(Text)


class ContestType(ORM_BASE):
    __tablename__ = 'contest_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    parent_id = Column(Integer, ForeignKey('contest_types.id'))
    parent = relationship('ContestType')


class Location(ORM_BASE):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)


class Person(ORM_BASE):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    biography = Column(Text)


class Ranking(ORM_BASE):
    __tablename__ = 'rankings'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    priority = Column(Integer)


class TestPiece(ORM_BASE):
    __tablename__ = 'test_pieces'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    composer_id = Column(Integer, ForeignKey('persons.id'))
    composer = relationship('Person', foreign_keys=[composer_id])
    arranger_id = Column(Integer, ForeignKey('persons.id'))
    arranger = relationship('Person', foreign_keys=[arranger_id])
    year = Column(Integer)
    description = Column(Text)
    misc = Column(Text)
    contests = relationship('Contest', secondary=SET_PIECE_LIST, backref='TestPiece')


class Venue(ORM_BASE):
    __tablename__ = 'venues'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    location = relationship('Location')
    address = Column(Text)


class User(ORM_BASE):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    realname = Column(String(50))
    password = Column(String(65))
    email = Column(String(120), unique=True)

    create_time = Column(DateTime)
    user_type = Column(String(50))
    active = Column(Boolean)

    def __init__(self, username: str = None, email: str = None) -> None:
        self.username = username
        self.email = email

    def __repr__(self) -> str:
        return '<User %r>' % (self.username)

    def is_admin(self) -> bool:
        return self.type == 'admin'

    # - for flask-login - #
    @property
    def is_active(self) -> bool:
        return self.is_active

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    # def get_id(self):
    #     return 'user_' + self.username
