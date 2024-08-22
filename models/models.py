import psycopg2
from flask import g


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            host="3Bg810W7z4t7YtGA@aws-0-sa-east-1.pooler.supabase.com",
            database="postgres",
            user="postgres.urxsxcaesrhgtwwvxmku",
            password="3Bg810W7z4t7YtGA"
        )
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

#DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://postgres.urxsxcaesrhgtwwvxmku:3Bg810W7z4t7YtGA@aws-0-sa-east-1.pooler.supabase.com/postgres')
