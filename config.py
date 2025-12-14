"""
Configuration for Home Design POC
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Set environment variable for LiteLLM to use Google AI Studio (not Vertex AI)
if GOOGLE_API_KEY:
    os.environ['GEMINI_API_KEY'] = GOOGLE_API_KEY

# Model Configuration
GEMINI_VISION_MODEL = 'gemini-2.5-flash-image'
GEMINI_IMAGE_MODEL = 'gemini-2.5-flash-image'  # Will use imagen-3.0-generate-001 when available

# POC Settings
MAX_PHOTOS = 5
OUTPUT_DIR = 'output'
TEST_PHOTOS_DIR = 'test_photos'

# Success Metrics
TARGET_LATENCY_SECONDS = 60
TARGET_COST_PER_RUN = 2.0
TARGET_ACCURACY = 0.8
