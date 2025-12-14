"""
Nano Banana (Gemini 2.5 Flash Image) Integration
Based on: https://www.theunwindai.com/p/build-an-ai-home-renovation-planner-agent-using-nano-banana
"""
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional
from PIL import Image
import base64
import io

# Fix UTF-8 encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')

# Try to use google-genai (ADK) first, fallback to google-generativeai
try:
    from google import genai
    from google.genai import types
    USE_ADK = True
    print("✅ Using Google GenAI SDK (ADK)")
except ImportError:
    import google.generativeai as genai
    USE_ADK = False
    print("⚠️ Using google-generativeai (ADK not available)")

import config

class NanoBananaGenerator:
    """Generate transformed room images using Nano Banana (Gemini 2.5 Flash Image)"""

    def __init__(self):
        if USE_ADK:
            # Using ADK client
            self.client = genai.Client(api_key=config.GOOGLE_API_KEY)
            self.model_name = "gemini-2.5-flash-image"
        else:
            # Using standard generativeai
            genai.configure(api_key=config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel("gemini-2.5-flash-image")
            self.model_name = "gemini-2.5-flash-image"

        print(f"✅ Nano Banana initialized: {self.model_name}")

    def generate_image(self, prompt: str, reference_image_path: Optional[str] = None) -> Dict[str, Any]:
        """Generate image using Nano Banana with optional reference image for transformation"""
        try:
            print(f"\n🎨 Generating image with Nano Banana...")
            print(f"📝 Prompt: {prompt[:150]}...")

            if reference_image_path:
                print(f"🖼️ Using reference image: {reference_image_path}")

            if USE_ADK:
                # Use ADK approach from the article
                parts = [types.Part.from_text(text=prompt)]

                # Add reference image if provided
                if reference_image_path:
                    try:
                        with open(reference_image_path, 'rb') as f:
                            image_bytes = f.read()

                        # Add image to parts
                        parts.append(types.Part.from_bytes(
                            data=image_bytes,
                            mime_type="image/jpeg"
                        ))
                        print("✅ Reference image added to request")
                    except Exception as img_error:
                        print(f"⚠️ Could not load reference image: {img_error}")

                contents = [
                    types.Content(
                        role="user",
                        parts=parts,
                    ),
                ]

                config_obj = types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    temperature=0.4,
                )

                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=config_obj,
                )

            else:
                # Use standard generativeai approach
                content_parts = [prompt]

                # Add reference image if provided
                if reference_image_path:
                    try:
                        img = Image.open(reference_image_path)
                        content_parts.append(img)
                        print("✅ Reference image added to request")
                    except Exception as img_error:
                        print(f"⚠️ Could not load reference image: {img_error}")

                response = self.model.generate_content(
                    content_parts,
                    generation_config={
                        "temperature": 0.4,
                    }
                )

            # Extract image from response
            print("🔍 Parsing response...")

            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]

                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            # Check for inline_data (image)
                            if hasattr(part, 'inline_data') and part.inline_data:
                                print("✅ Found image data!")

                                # Get image bytes
                                if hasattr(part.inline_data, 'data'):
                                    image_bytes = part.inline_data.data
                                else:
                                    # Try different attribute names
                                    image_bytes = part.inline_data

                                # Convert to PIL Image
                                image = Image.open(io.BytesIO(image_bytes))

                                # Save image
                                os.makedirs("output/rendered_images", exist_ok=True)
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                image_path = f"output/rendered_images/nano_banana_{timestamp}.png"

                                image.save(image_path)

                                print(f"✅ Image generated successfully!")
                                print(f"📁 Saved to: {image_path}")
                                print(f"📏 Size: {image.size[0]}x{image.size[1]}")

                                # Encode to base64
                                buffered = io.BytesIO()
                                image.save(buffered, format="PNG")
                                img_base64 = base64.b64encode(buffered.getvalue()).decode()

                                return {
                                    "success": True,
                                    "image_path": image_path,
                                    "image_data": img_base64,
                                    "model": self.model_name,
                                    "size": image.size
                                }

            # No image found - return text response for debugging
            print("⚠️ No image data found in response")
            response_text = ""
            if hasattr(response, 'text'):
                response_text = response.text[:500]

            return {
                "success": False,
                "error": "No image data in response",
                "response_text": response_text,
                "model": self.model_name
            }

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ Error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "error_details": error_details
            }

    def generate_room_transformation(
        self,
        room_analysis: Dict[str, Any],
        style: str,
        custom_prompt: Optional[str] = None,
        reference_image_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate transformed room image based on analysis and optional reference image"""

        room_type = room_analysis.get('room_type', 'room')
        features = room_analysis.get('features', [])
        dimensions = room_analysis.get('dimensions_estimate', 'medium')
        colors = room_analysis.get('colors', [])

        # Build detailed prompt for Nano Banana
        if reference_image_path:
            # Image transformation prompt - tells the model to transform the uploaded image
            prompt = f"""Transform this room image into a beautifully renovated {style} {room_type} while KEEPING THE SAME ROOM LAYOUT, STRUCTURE, and PERSPECTIVE.

IMPORTANT: You are transforming the uploaded room image, NOT creating a new room from scratch.

TRANSFORMATION REQUIREMENTS:
- MAINTAIN the exact room dimensions and layout you see in the image
- PRESERVE the locations of windows, doors, and architectural features
- KEEP the same camera angle and perspective
- Only MODIFY the interior design elements (furniture, colors, decor, lighting)

TARGET STYLE: {style}

ROOM SIZE: {dimensions}"""

            if custom_prompt:
                prompt += f"\n\nDESIGN VISION:\n{custom_prompt}"

                # Extract specific items from custom prompt
                specific_items = self._extract_key_items(custom_prompt)
                if specific_items:
                    prompt += f"\n\nITEMS TO INCLUDE:"
                    for item in specific_items:
                        prompt += f"\n- {item}"

            prompt += f"""

DESIGN REQUIREMENTS:
- Transform the EXISTING room in the image into {style} style
- Professional interior design quality
- Natural, warm lighting that enhances the space
- Photorealistic textures and materials
- Clean, well-organized, and beautifully styled
- Maintain the room's structure while upgrading the aesthetic
- No text, watermarks, or overlays"""

        else:
            # Original prompt for generating from scratch (when no reference image)
            prompt = f"""Create a photorealistic interior design photograph of a beautifully renovated {style} {room_type}.

ROOM SPECIFICATIONS:
- Size: {dimensions} sized room
- Style: {style}
- Key architectural features to incorporate: {', '.join(features[:3]) if features else 'standard features'}"""

            if custom_prompt:
                # Extract specific items from custom prompt to emphasize them
                specific_items = self._extract_key_items(custom_prompt)

                prompt += f"\n\nDESIGN VISION:\n{custom_prompt}"

                if specific_items:
                    prompt += f"\n\n⚠️ CRITICAL ITEMS TO INCLUDE (MUST BE VISIBLE):"
                    for item in specific_items:
                        prompt += f"\n- {item} (clearly visible and prominent)"

            prompt += f"""

REQUIREMENTS:
- Professional interior photography quality
- Natural, warm lighting that enhances the space
- High resolution and sharp details
- Magazine-worthy composition
- Inviting and aspirational atmosphere
- Clean, well-organized, and styled
- Photorealistic textures and materials
- Proper depth of field and perspective
- ALL specified furniture and items must be clearly visible
- No text, watermarks, or overlays"""

        return self.generate_image(prompt, reference_image_path=reference_image_path)

    def _extract_key_items(self, prompt: str) -> list:
        """Extract specific furniture/item mentions from user prompt"""
        # Common furniture and item keywords to look for
        keywords = [
            'laptop', 'computer', 'desk', 'table', 'chair', 'sofa', 'couch',
            'bed', 'shelf', 'bookshelf', 'lamp', 'light', 'plant', 'rug',
            'tv', 'television', 'monitor', 'keyboard', 'ottoman', 'stool',
            'cabinet', 'dresser', 'nightstand', 'bench', 'mirror', 'artwork',
            'painting', 'clock', 'vase', 'cushion', 'pillow', 'blanket',
            'curtain', 'blinds', 'plant', 'coffee table', 'side table',
            'reading chair', 'armchair', 'bean bag', 'storage', 'shelving'
        ]

        prompt_lower = prompt.lower()
        found_items = []

        for keyword in keywords:
            if keyword in prompt_lower:
                # Try to get context around the keyword
                if keyword == 'laptop':
                    if 'laptop table' in prompt_lower or 'laptop on' in prompt_lower:
                        found_items.append('Laptop computer on table (open and visible)')
                    else:
                        found_items.append('Laptop computer (open and visible)')
                elif keyword == 'bookshelf' or keyword == 'shelf':
                    if 'books' in prompt_lower:
                        found_items.append('Bookshelf filled with books')
                    else:
                        found_items.append('Bookshelf')
                elif keyword == 'lamp':
                    if 'study lamp' in prompt_lower:
                        found_items.append('Study desk lamp (turned on)')
                    elif 'table lamp' in prompt_lower:
                        found_items.append('Table lamp')
                    else:
                        found_items.append('Lamp')
                elif keyword not in ' '.join(found_items).lower():
                    found_items.append(keyword.title())

        # Remove duplicates while preserving order
        seen = set()
        unique_items = []
        for item in found_items:
            item_lower = item.lower()
            if item_lower not in seen:
                seen.add(item_lower)
                unique_items.append(item)

        return unique_items


def test_nano_banana():
    """Test Nano Banana generation"""
    print("="*70)
    print("🧪 TESTING NANO BANANA (GEMINI 2.5 FLASH IMAGE)")
    print("="*70)

    generator = NanoBananaGenerator()

    # Test prompt
    test_prompt = """Create a photorealistic interior photograph of a modern minimalist bedroom.

Features:
- White walls with subtle texture
- Natural oak platform bed with white linen bedding
- Floating nightstands in matching oak
- Soft warm ambient lighting from hidden LED strips
- Large potted fiddle leaf fig in the corner
- Abstract minimalist art above the bed
- Sheer white curtains on large windows
- Clean lines and uncluttered aesthetic
- Professional interior photography quality
- Natural morning light"""

    result = generator.generate_image(test_prompt)

    print("\n" + "="*70)
    if result['success']:
        print("✅ SUCCESS!")
        print(f"📁 Image saved to: {result['image_path']}")
        print(f"📏 Image size: {result.get('size', 'Unknown')}")
    else:
        print("❌ FAILED!")
        print(f"Error: {result.get('error')}")
        if 'response_text' in result and result['response_text']:
            print(f"\nResponse text: {result['response_text']}")
    print("="*70)

if __name__ == "__main__":
    test_nano_banana()
