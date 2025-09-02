import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class settings:
    # Database settings - CRITICAL: Use the exact names Flask-SQLAlchemy expects
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() == 'true'
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False').lower() == 'true'
    
    # Individual DB components (optional, for reference)
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'recipe_recommender')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    
    # App settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'  # Changed to FLASK_DEBUG
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    RECIPES_PER_PAGE = int(os.getenv('RECIPES_PER_PAGE', 10))
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # IntaSend Configuration (note: your .env says INTASEND, not INSTASEND)
    INTASEND_SECRET_KEY = os.getenv('INTASEND_SECRET_KEY', '')
    INTASEND_PUBLISHABLE_KEY = os.getenv('INTASEND_PUBLISHABLE_KEY', '')
    
    # Application Settings
    DAILY_FREE_LIMIT = int(os.getenv('DAILY_FREE_LIMIT', 10))
    PREMIUM_PRICE = int(os.getenv('PREMIUM_PRICE', 100))
    CURRENCY = os.getenv('CURRENCY', 'KES')
    TIMEZONE = os.getenv('TIMEZONE', 'Africa/Nairobi')
    CALLBACK_BASE_URL = os.getenv('CALLBACK_BASE_URL', 'http://localhost:5000')
    
    # OpenAPI/Swagger Configuration
    OPENAPI_VERSION = os.getenv('OPENAPI_VERSION', '3.0.3')
    OPENAPI_TITLE = os.getenv('OPENAPI_TITLE', 'Recipe Recommender API')
    OPENAPI_DESCRIPTION = os.getenv('OPENAPI_DESCRIPTION', 'A smart recipe recommendation system')
    OPENAPI_CONTACT_NAME = os.getenv('OPENAPI_CONTACT_NAME', 'Recipe Team')
    OPENAPI_CONTACT_EMAIL = os.getenv('OPENAPI_CONTACT_EMAIL', 'recipes@example.com')
    OPENAPI_LICENSE_NAME = os.getenv('OPENAPI_LICENSE_NAME', 'MIT')
    OPENAPI_LICENSE_URL = os.getenv('OPENAPI_LICENSE_URL', 'https://opensource.org/licenses/MIT')
    
    # Validation methods
    def database_configured(self):
        """Check if database is properly configured"""
        return bool(self.SQLALCHEMY_DATABASE_URI)
    
    def openai_configured(self):
        """Check if OpenAI is properly configured"""
        return bool(self.OPENAI_API_KEY)
    
    def intasend_configured(self):
        """Check if IntaSend is properly configured"""
        return bool(self.INTASEND_SECRET_KEY and self.INTASEND_PUBLISHABLE_KEY)
    
    def openapi_info(self):
        """Return OpenAPI info dictionary for Swagger"""
        return {
            'openapi': self.OPENAPI_VERSION,
            'info': {
                'title': self.OPENAPI_TITLE,
                'description': self.OPENAPI_DESCRIPTION,
                'contact': {
                    'name': self.OPENAPI_CONTACT_NAME,
                    'email': self.OPENAPI_CONTACT_EMAIL
                },
                'license': {
                    'name': self.OPENAPI_LICENSE_NAME,
                    'url': self.OPENAPI_LICENSE_URL
                },
                'version': '1.0.0'
            }
        }

# Create an instance of the settings
config = settings()