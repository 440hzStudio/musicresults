# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flaskext.mysql import MySQL

db_session = None
Base = declarative_base()


def init_db(app):
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models

    global db_session
    global Base

    if app.config.get('DATABASE') == 'mysql':
        mysql = MySQL()
        mysql.init_app(app)
        engine = create_engine(
            'mysql+pymysql://%s:%s@%s/musicresults?charset=utf8' % (
                app.config.get('DB_USER'),
                app.config.get('DB_PASSWORD'),
                app.config.get('DB_HOST')),
            encoding='utf-8')
    elif app.config.get('DATABASE') == 'sqlite':
        engine = create_engine('sqlite:///musicresults.db', convert_unicode=True)

    db_session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        ))
    Base.metadata.create_all(bind=engine)
    Base.query = db_session.query_property()
