from flask_sqlalchemy import SQLAlchemy

import click
import os
from flask import current_app, app

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine('sqlite:///living-library.sqlite')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import living_library.data.models
    Base.metadata.create_all(bind=engine)

# def get_db():
#     if 'db' not in g:
#         g.db = SQLAlchemy(current_app, model_class=Base)

#     return g.db

# def close_db(e=None):
#     db = g.pop('db', None)

#     if db is not None:
#         db.close()

# def init_db():
#     db = get_db()

#     with current_app.app_context():
#         db.create_all()

# @click.command('init-db')
# def init_db_command():
#     """Clear the existing data and create new tables"""
#     init_db()
#     click.echo('Initializing the database.')

# def init_app(app):
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(init_db_command)

# # sqlite3.register_converter(
# #     "timestamp", lambda v: datetime.fromisoformat(v.decode())
# # )