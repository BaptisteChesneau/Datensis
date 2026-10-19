
from flask import current_app
from sqlalchemy import create_engine, inspect

from app import create_app


app = create_app()

with app.app_context():
    url = current_app.config["SQLALCHEMY_DATABASE_URI"]

    engine = create_engine(url)

    try:
        tables = inspect(engine).get_table_names()

        print("=" * 50)
        print("DATENSIS - TEST SQLITE")
        print("=" * 50)

        print("Connexion SQLite : OK")
        print("Nombre de tables :", len(tables))

        for numero, table in enumerate(tables, start=1):
            print(f"{numero:02d}. {table}")

        if len(tables) == 27:
            print("\nSUCCES : les 27 tables sont accessibles.")
        else:
            print("\nATTENTION : nombre de tables inattendu.")

    finally:
        engine.dispose()
