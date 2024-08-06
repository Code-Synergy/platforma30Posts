
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'yC/gjUgkVq7PMGyEGf0uecQxD+wgwBlbkR8uV5SIEczDHmRBksn1XaOAwyTInOavT7/941A6OIYO8d5AJxE6tw==')
    DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://postgres.urxsxcaesrhgtwwvxmku:3Bg810W7z4t7YtGA@aws-0-sa-east-1.pooler.supabase.com/postgres')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'yC/gjUgkVq7PMGyEGf0uecQxD+wgwBlbkR8uV5SIEczDHmRBksn1XaOAwyTInOavT7/941A6OIYO8d5AJxE6tw==')
