import os
import shutil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Detect Vercel / serverless environment
IS_VERCEL = bool(os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'))

if IS_VERCEL:
    TMP_DIR = '/tmp'
    DB_PATH = os.path.join(TMP_DIR, 'govpilot.db')
    
    # If source instance db exists in the repo, copy it to /tmp so seeded data is preserved
    source_db = os.path.join(BASE_DIR, 'instance', 'govpilot.db')
    if os.path.exists(source_db) and not os.path.exists(DB_PATH):
        try:
            shutil.copyfile(source_db, DB_PATH)
        except Exception:
            pass
            
    UPLOAD_DIR = os.path.join(TMP_DIR, 'uploads')
else:
    DB_PATH = os.path.join(BASE_DIR, 'instance', 'govpilot.db')
    UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'govpilot-secure-dev-key-2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        f"sqlite:///{DB_PATH}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = UPLOAD_DIR
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32 MB max upload
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'csv', 'xlsx', 'json'}

    # Demo mode flag
    DEMO_MODE = True

