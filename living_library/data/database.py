from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base

Base = declarative_base()
db = SQLAlchemy(model_class=Base)
db_session = db.session

def init_db(app):
    import living_library.data.models
    with app.app_context():
        db.create_all()