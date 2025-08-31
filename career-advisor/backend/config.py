# Configuration file for Career Advisor Backend
import os
from decouple import config

# OpenAI API Configuration
OPENAI_API_KEY = config('OPENAI_API_KEY', default='')

# Django Settings
DEBUG = config('DEBUG', default=True, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='django-insecure-0%)3wz4v&l54syi(bbeyl5(kh3r48gtvx87odur5na8hag4veq')

# Database Configuration
DATABASE_URL = config('DATABASE_URL', default='sqlite:///db.sqlite3')

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
]

# Assessment Configuration
MAX_QUESTIONS_PER_ASSESSMENT = 50
MIN_RESPONSES_FOR_COMPLETION = 10
