"""
Image Generator Tool - Nano Banana (Gemini Image) Wrapper
Generates photorealistic room renderings based on analysis and design brief
"""
import google.generativeai as genai
from typing import Dict, Any, Optional
import config
import base64
import io
from PIL import Image

class ImageGenerator:
    """Generates photorealistic room renderings using Google's Image Generation"""

    def __init__(self):
        genai.configure(api_key=config.GOOGLE_API_KEY)
        # Use text model for generating descriptions, vision model for analyzing images
        self.text_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.vision_model = genai.GenerativeModel(config.GEMINI_VISION_MODEL)

        # Initialize Nano Banana for actual image generation
        try:
            from tools.nano_banana_generator import NanoBananaGenerator
            self.nano_banana = NanoBananaGenerator()
            self.image_gen_available = True
            print("✅ Nano Banana image generation available!")
        except Exception as e:
            self.image_gen_available = False
            self.nano_banana = None
            print(f"⚠️ Nano Banana not available: {e}")

    def _check_imagen_availability(self):
        """Check if Imagen/image generation is available"""
        try:
            # Try to import imagen or check for image generation models
            from google.generativeai import ImageGenerationModel
            return True
        except (ImportError, AttributeError):
            # Imagen not available in this version
            return False

    def _generate_image_with_imagen(self, prompt: str, reference_image_path: Optional[str] = None):
        """Generate actual image using Google's Imagen"""
        try:
            from google.generativeai import ImageGenerationModel
            import requests
            from datetime import datetime

            # Initialize Imagen model
            imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

            # Generate image
            if reference_image_path:
                # Use reference image if provided
                with open(reference_image_path, 'rb') as f:
                    reference_img = Image.open(f)
                    images = imagen_model.edit_image(
                        prompt=prompt,
                        base_image=reference_img,
                        number_of_images=1
                    )
            else:
                # Generate from scratch
                images = imagen_model.generate_images(
                    prompt=prompt,
                    number_of_images=1
                )

            # Save generated image
            os.makedirs("output/rendered_images", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = f"output/rendered_images/transformation_{timestamp}.png"

            images[0].save(image_path)

            return {
                "success": True,
                "image_path": image_path,
                "method": "imagen"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "method": "imagen"
            }

    def generate_rendering(
        self,
        room_analysis: Dict[str, Any],
        design_brief: str,
        style: str = "modern minimalist",
        reference_image_path: Optional[str] = None,
        custom_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a photorealistic rendering of the renovated room

        Args:
            room_analysis: Analysis from ImageAnalyzer
            design_brief: Description of desired changes
            style: Target design style
            reference_image_path: Optional reference photo to maintain room structure
            custom_prompt: Optional custom user prompt for specific design vision

        Returns:
            Dictionary containing:
            - success: bool
            - rendering_description: Text description of the rendering
            - prompt_used: The prompt sent to the model
            - image_data: Base64 encoded image (when Imagen API available)
            - image_url: URL to generated image (when Imagen API available)
        """
        try:
            # Build comprehensive prompt for photorealistic rendering
            room_type = room_analysis.get('room_type', 'room')
            features = room_analysis.get('features', [])
            dimensions = room_analysis.get('dimensions_estimate', 'medium')

            prompt = f"""Generate a photorealistic interior design rendering of a {room_type}.

ROOM SPECIFICATIONS:
- Size: {dimensions}
- Key features to maintain: {', '.join(features) if features else 'standard room features'}

DESIGN BRIEF:
{design_brief}

TARGET STYLE: {style}

REQUIREMENTS:
- Photorealistic quality
- Maintain the room's structural features (windows, doors, layout)
- {style} aesthetic
- Professional interior design quality
- Warm, inviting atmosphere
- Proper lighting and shadows
- Realistic materials and textures

Create a stunning, magazine-quality rendering that the homeowner can use to make confident purchasing decisions."""

            # Note: Current implementation generates detailed text descriptions
            # When Imagen-3 API is available, this will generate actual images

            if reference_image_path:
                # Use vision model to analyze reference image and create enhanced design
                img = Image.open(reference_image_path)

                # Incorporate custom prompt if provided
                user_vision = f"\n\nUSER'S SPECIFIC VISION:\n{custom_prompt}\n" if custom_prompt else ""

                # Create enhanced prompt that asks model to analyze the image and provide TEXT description
                enhanced_prompt = f"""You are an expert interior designer viewing a photograph of a real {room_type}.

CURRENT ROOM ANALYSIS:
- Size: {dimensions}
- Current features: {', '.join(features) if features else 'standard room features'}
- Current condition: Needs transformation

YOUR TASK:
Analyze this room photo carefully and write a detailed TEXT description of how this EXACT room would look after a complete {style} transformation.

{design_brief}{user_vision}

IMPORTANT: Provide a DETAILED TEXT DESCRIPTION ONLY. Do NOT generate or return images.

In your TEXT description, include:
1. VISUAL TRANSFORMATION: Describe exactly how the room would look, referencing the current layout and features you see
2. COLOR PALETTE: Specific paint colors (with brand names if possible), textile colors, and accent colors
3. FURNITURE PLACEMENT: How to arrange or replace furniture you see in the image
4. LIGHTING DESIGN: Specific lighting fixtures and their exact placement
5. MATERIALS & TEXTURES: Flooring type, wall treatments, fabrics, and finishes
6. DECORATIVE ELEMENTS: Specific art pieces, plants, accessories, and styling details
7. SPATIAL IMPROVEMENTS: How to maximize the existing space and layout
8. SHOPPING GUIDE: Specific product recommendations with approximate prices

Make this description so detailed and vivid that someone could visualize the transformed room perfectly and use it to make confident purchasing decisions. Reference specific elements you see in the current photo.

Write at least 500 words."""

                # Configure to return text only
                response = self.vision_model.generate_content(
                    [enhanced_prompt, img],
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="text/plain"
                    )
                )

                # Extract text from response, handling potential inline_data
                rendering_text = ""
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'text') and part.text:
                        rendering_text += part.text

                if not rendering_text:
                    raise ValueError("No text content received from vision model")
            else:
                # Use text model for pure text generation without reference
                response = self.text_model.generate_content(prompt)
                rendering_text = response.text

            # Try to generate actual image using Nano Banana
            generated_image_path = None
            image_generation_note = "Text description only"

            if self.image_gen_available and self.nano_banana:
                print("\n🎨 Generating actual transformed image with Nano Banana...")

                # Use the room analysis and reference image to generate transformation
                nano_result = self.nano_banana.generate_room_transformation(
                    room_analysis=room_analysis,
                    style=style,
                    custom_prompt=custom_prompt,
                    reference_image_path=reference_image_path
                )

                if nano_result.get("success"):
                    generated_image_path = nano_result.get("image_path")
                    image_generation_note = f"✅ Image generated with Nano Banana (Gemini 2.5 Flash Image)"
                    print(f"✅ Transformed image saved to: {generated_image_path}")
                else:
                    image_generation_note = f"⚠️ Image generation failed: {nano_result.get('error')}"
                    print(image_generation_note)
            else:
                print("\n⚠️ Nano Banana not available - generating text description only")
                image_generation_note = "Text description only - Nano Banana initialization failed"

            return {
                "success": True,
                "rendering_description": rendering_text,
                "prompt_used": prompt if not reference_image_path else enhanced_prompt,
                "style": style,
                "custom_prompt": custom_prompt,
                "used_reference_image": reference_image_path is not None,
                "note": image_generation_note,
                "room_type": room_type,
                "image_path": generated_image_path,
                "image_url": None,  # Local file path used instead
                "image_gen_available": self.image_gen_available
            }

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            return {
                "success": False,
                "error": str(e),
                "error_details": error_details,
                "prompt_used": prompt if 'prompt' in locals() else None
            }

    def refine_rendering(
        self,
        previous_rendering: Dict[str, Any],
        refinement_request: str
    ) -> Dict[str, Any]:
        """
        Refine an existing rendering based on natural language feedback

        Args:
            previous_rendering: Previous rendering result
            refinement_request: Natural language description of changes

        Returns:
            Refined rendering
        """
        try:
            prompt = f"""You previously generated this interior design rendering:

{previous_rendering.get('rendering_description', '')}

The user requests the following changes:
{refinement_request}

Generate an updated photorealistic rendering incorporating these changes while maintaining the overall design vision."""

            response = self.text_model.generate_content(prompt)

            return {
                "success": True,
                "rendering_description": response.text,
                "refinement_applied": refinement_request,
                "version": previous_rendering.get('version', 1) + 1,
                "note": "Image generation will be enabled when Imagen-3 API is available."
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
