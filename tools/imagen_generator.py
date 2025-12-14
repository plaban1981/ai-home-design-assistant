"""
Imagen Integration for Actual Image Generation
Uses Google's Imagen 4.0 to generate transformed room images
"""
import sys
import google.generativeai as genai
import config
from PIL import Image
import os
from datetime import datetime
from typing import Dict, Any, Optional
import base64
import io

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')

class ImagenGenerator:
    """Generate actual transformed room images using Imagen 4.0"""

    def __init__(self):
        genai.configure(api_key=config.GOOGLE_API_KEY)
        # Use Nano Banana (gemini-2.5-flash-image) as shown in the reference
        self.imagen_model_name = "gemini-2.5-flash-image"
        print(f"✅ Nano Banana (Gemini Image) initialized: {self.imagen_model_name}")

    def generate_transformed_image(
        self,
        prompt: str,
        aspect_ratio: str = "1:1",
        safety_filter_level: str = "block_some",
        person_generation: str = "dont_allow"
    ) -> Dict[str, Any]:
        """
        Generate a transformed room image using Imagen

        Args:
            prompt: Description of the desired room transformation
            aspect_ratio: Image aspect ratio (1:1, 16:9, 9:16, 4:3, 3:4)
            safety_filter_level: Safety filter level
            person_generation: Whether to allow people in images

        Returns:
            Dictionary with:
            - success: bool
            - image_path: Path to saved image
            - image_data: Base64 encoded image data
        """
        try:
            print(f"\n🎨 Generating image with Nano Banana (Gemini 2.5 Flash Image)...")
            print(f"📝 Prompt: {prompt[:100]}...")

            # Use the Gemini image model with response_modalities for IMAGE output
            model = genai.GenerativeModel(self.imagen_model_name)

            # CRITICAL: Use response_modalities to get IMAGE output
            # This is the key from the reference article!
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_modalities=["IMAGE"],  # Request IMAGE output!
                    temperature=0.4,
                )
            )

            # Extract image from response
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]

                # Check if response contains image data
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        # Check for inline_data (image)
                        if hasattr(part, 'inline_data') and part.inline_data:
                            # Get image data
                            image_data = part.inline_data.data

                            # Convert to PIL Image
                            image = Image.open(io.BytesIO(image_data))

                            # Save image
                            os.makedirs("output/rendered_images", exist_ok=True)
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            image_path = f"output/rendered_images/transformation_{timestamp}.png"

                            image.save(image_path)

                            print(f"✅ Image generated successfully!")
                            print(f"📁 Saved to: {image_path}")

                            # Encode to base64 for JSON storage
                            buffered = io.BytesIO()
                            image.save(buffered, format="PNG")
                            img_base64 = base64.b64encode(buffered.getvalue()).decode()

                            return {
                                "success": True,
                                "image_path": image_path,
                                "image_data": img_base64,
                                "model": self.imagen_model_name
                            }

            # If we get here, no image was generated - debug the response
            print(f"\n🔍 Debug: Response structure:")
            print(f"   Candidates: {len(response.candidates) if response.candidates else 0}")
            if response.candidates:
                print(f"   First candidate: {response.candidates[0]}")
                if hasattr(response.candidates[0], 'content'):
                    print(f"   Content: {response.candidates[0].content}")
                    if hasattr(response.candidates[0].content, 'parts'):
                        print(f"   Parts: {len(response.candidates[0].content.parts)}")
                        for i, part in enumerate(response.candidates[0].content.parts):
                            print(f"   Part {i}: {dir(part)}")

            return {
                "success": False,
                "error": "No image data in response",
                "response": str(response),
                "debug_info": {
                    "has_candidates": response.candidates is not None,
                    "num_candidates": len(response.candidates) if response.candidates else 0
                }
            }

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ Image generation failed: {str(e)}")
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
        """
        Generate a transformed room image based on analysis and style

        Args:
            room_analysis: Room analysis from visual assessor
            style: Target design style
            custom_prompt: Optional custom user prompt
            reference_image_path: Optional reference image (not used by Imagen directly)

        Returns:
            Dictionary with generation result
        """
        room_type = room_analysis.get('room_type', 'room')
        features = room_analysis.get('features', [])
        dimensions = room_analysis.get('dimensions_estimate', 'medium')

        # Build comprehensive prompt for Imagen
        imagen_prompt = f"""Photorealistic interior design photograph of a beautiful {style} {room_type}.

Room specifications:
- Size: {dimensions}
- Style: {style}"""

        if features:
            imagen_prompt += f"\n- Key features: {', '.join(features[:3])}"

        if custom_prompt:
            imagen_prompt += f"\n\nDesign vision: {custom_prompt}"

        imagen_prompt += """

Requirements:
- Professional interior photography quality
- Natural lighting
- High resolution and detailed
- Magazine-worthy composition
- Warm and inviting atmosphere
- Modern and stylish
- Clean and well-organized space"""

        # Generate the image
        return self.generate_transformed_image(imagen_prompt)


def test_imagen():
    """Test Imagen generation"""
    print("="*70)
    print("🧪 TESTING IMAGEN IMAGE GENERATION")
    print("="*70)

    generator = ImagenGenerator()

    # Simple test
    test_prompt = "A modern minimalist bedroom with white walls, natural wood furniture, soft ambient lighting, plants, clean lines, serene atmosphere, professional interior photography"

    result = generator.generate_transformed_image(test_prompt)

    if result['success']:
        print("\n✅ SUCCESS!")
        print(f"Image saved to: {result['image_path']}")
    else:
        print("\n❌ FAILED!")
        print(f"Error: {result.get('error')}")
        if 'error_details' in result:
            print(f"\nDetails:\n{result['error_details']}")

if __name__ == "__main__":
    test_imagen()
