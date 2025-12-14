"""
Image Analyzer Tool - Gemini Vision Wrapper
Analyzes room photos to extract room type, features, style, and dimensions
"""
import google.generativeai as genai
from PIL import Image
import json
from typing import Dict, Any
import config

class ImageAnalyzer:
    """Analyzes room images using Gemini Vision"""

    def __init__(self):
        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_VISION_MODEL)

    def analyze_room(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze a room photo and extract structured information

        Args:
            image_path: Path to the room photo

        Returns:
            Dictionary containing room analysis:
            - room_type: bedroom, living_room, kitchen, etc.
            - style: current design style
            - features: list of notable features (windows, doors, furniture)
            - dimensions_estimate: rough size estimate
            - lighting: lighting conditions
            - challenges: potential design challenges
        """
        try:
            # Load image
            img = Image.open(image_path)

            # Create detailed analysis prompt
            prompt = """Analyze this room photo and provide a detailed assessment in JSON format.

Please identify:
1. room_type: (bedroom, living_room, kitchen, bathroom, dining_room, office, other)
2. current_style: (modern, traditional, minimalist, industrial, farmhouse, eclectic, etc.)
3. features: List all notable features you see (windows, doors, built-ins, fireplace, etc.)
4. furniture: List current furniture pieces
5. colors: Dominant colors in the space
6. lighting: (natural, artificial, mixed, poor, good, excellent)
7. dimensions_estimate: (small <100sqft, medium 100-200sqft, large 200-400sqft, very_large >400sqft)
8. condition: (excellent, good, needs_refresh, needs_renovation)
9. challenges: List any design challenges (awkward layout, limited light, etc.)
10. opportunities: Design opportunities you see

Return ONLY valid JSON, no other text."""

            # Call Gemini Vision API
            response = self.model.generate_content([prompt, img])

            # Parse JSON response
            result_text = response.text.strip()

            # Remove markdown code blocks if present
            if result_text.startswith('```json'):
                result_text = result_text[7:]
            if result_text.startswith('```'):
                result_text = result_text[3:]
            if result_text.endswith('```'):
                result_text = result_text[:-3]

            analysis = json.loads(result_text.strip())

            # Add metadata
            analysis['image_path'] = image_path
            analysis['model_used'] = config.GEMINI_VISION_MODEL

            return analysis

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {response.text}")
            # Return structured error
            return {
                "error": "Failed to parse JSON response",
                "raw_response": response.text,
                "image_path": image_path
            }
        except Exception as e:
            return {
                "error": str(e),
                "image_path": image_path
            }
