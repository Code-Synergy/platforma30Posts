import os

class Config:
    DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://username:password@localhost/mydatabase')
