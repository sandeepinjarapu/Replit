import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import inspect

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import your models here
from models import Leader, Project, Collaborator, Content

def check_table_structure():
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print("Tables in the database:")
        for table in tables:
            print(f"\nTable: {table}")
            columns = inspector.get_columns(table)
            for column in columns:
                print(f"  - {column['name']} ({column['type']})")

def apply_migrations():
    with app.app_context():
        from flask import current_app
        from flask_migrate import upgrade
        with current_app.app_context():
            upgrade()

if __name__ == '__main__':
    print("Current database structure:")
    check_table_structure()

    print("\nApplying migrations...")
    apply_migrations()

    print("\nDatabase structure after applying migrations:")
    check_table_structure()