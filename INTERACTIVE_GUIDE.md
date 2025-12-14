# Interactive Home Design Assistant

Transform your interior spaces with AI-powered design suggestions using custom prompts!

## Features

- **Upload Any Image**: Use photos of your room from any source
- **Custom Design Prompts**: Describe exactly how you want to transform your space
- **AI-Powered Analysis**: Get detailed room analysis and design recommendations
- **Budget Planning**: Choose your budget range and get cost estimates
- **Reference-Based Transformation**: The AI analyzes your actual room and provides specific recommendations

## Quick Start

### Run the Interactive Tool

```bash
python interactive_design.py
```

The tool will guide you through:
1. Selecting or uploading an image
2. Describing your design vision
3. Choosing your budget range
4. Generating a custom transformation plan

## How It Works

### 1. Image Analysis
The system uses Google's Gemini Vision AI to:
- Identify room type and current style
- Detect existing furniture and features
- Analyze colors, lighting, and space layout
- Identify challenges and opportunities

### 2. Custom Transformation
Based on your prompt, the AI creates:
- Detailed visual descriptions of the transformed space
- Specific product recommendations with prices
- Color palettes with paint brand names
- Furniture placement suggestions
- Lighting design recommendations

### 3. Project Planning
You receive:
- Complete budget breakdown
- Project timeline
- Contractor recommendations
- Prioritized shopping list with retailers

## Example Prompts

### Style-Focused
```
"Modern minimalist with warm wood tones and lots of plants"
"Cozy bohemian style with earthy colors and natural textures"
"Industrial loft with exposed brick, metal accents, and Edison bulbs"
```

### Color-Focused
```
"Bright and airy with white walls, light blue accents, and natural wood"
"Warm and inviting with terracotta, cream, and gold accents"
"Dramatic and moody with dark walls, brass fixtures, and velvet textures"
```

### Function-Focused
```
"Productive home office with ergonomic furniture and good task lighting"
"Relaxing bedroom retreat with soft textures and ambient lighting"
"Multi-functional guest room that also serves as a home gym"
```

### Detailed Vision
```
"Scandinavian-inspired bedroom with a platform bed, minimalist nightstands,
soft gray walls, white oak flooring, and lots of natural light. Add some
greenery with hanging plants and keep everything clutter-free."
```

## Image Generation (Future Feature)

### Current Capability
- ✅ Analyzes your reference image
- ✅ Generates detailed text descriptions
- ✅ Provides specific product recommendations
- ✅ Creates comprehensive project plans

### Coming Soon
- 🔜 Actual transformed images using Google Imagen API
- 🔜 Multiple design variations
- 🔜 Side-by-side before/after comparisons
- 🔜 Download high-resolution renderings

### How to Enable Image Generation

When Google's Imagen API becomes available, update `config.py`:

```python
# Image Generation Settings
ENABLE_IMAGE_GENERATION = True
IMAGEN_API_KEY = os.getenv('IMAGEN_API_KEY')
IMAGEN_MODEL = 'imagen-3.0-generate-001'
```

The system will automatically use Imagen to generate actual transformed images instead of text descriptions.

## Tips for Best Results

### 1. Image Quality
- Use well-lit photos
- Capture the entire room if possible
- Include multiple angles for better context
- Avoid heavily filtered or edited images

### 2. Prompts
- Be specific about what you want
- Mention colors, materials, and styles explicitly
- Include any must-keep items or features
- Specify your budget constraints

### 3. Budget Ranges
- **Low ($1,000 - $3,000)**: Basic refresh, paint, decor
- **Moderate ($3,000 - $7,000)**: New furniture, lighting, some renovations
- **High ($7,000+)**: Comprehensive transformation, high-end materials

## Output Files

Results are saved to `output/interactive_results_TIMESTAMP.json` containing:
- Original image path
- Your custom prompt
- Complete room analysis
- Transformation description
- Budget breakdown
- Project timeline
- Shopping list

## Troubleshooting

### "Could not find image"
- Check that the image file exists
- Use full path or place image in `test_photos/` folder
- Supported formats: JPG, JPEG, PNG

### "API quota exceeded"
- Wait for quota to reset (usually 24 hours)
- Upgrade to paid API tier for higher limits
- Use a different API key

### "No text content received"
- Image may be too complex or unclear
- Try a different, clearer photo
- Ensure good lighting in the image

## API Keys Required

Set these in your `.env` file:

```
GOOGLE_API_KEY=your_google_api_key_here
```

Get your API key at: https://makersuite.google.com/app/apikey

## Examples

### Example 1: Budget Bedroom Refresh
**Prompt**: "Cozy minimalist bedroom with soft pastels and natural wood"
**Budget**: Low ($1,000 - $3,000)

**Result**:
- Paint color recommendations (Benjamin Moore "Pale Oak")
- IKEA furniture suggestions
- Budget-friendly decor from Target
- DIY project ideas
- Total estimated cost: $2,400

### Example 2: Modern Living Room
**Prompt**: "Contemporary living room with neutral tones, statement lighting, and room for entertaining"
**Budget**: Moderate ($3,000 - $7,000)

**Result**:
- Modular sofa recommendations
- Designer lighting fixtures
- Gallery wall layout
- New flooring options
- Total estimated cost: $6,200

### Example 3: Home Office Transformation
**Prompt**: "Productive workspace with ergonomic furniture, plenty of storage, and motivating decor in blues and greens"
**Budget**: Moderate ($3,000 - $7,000)

**Result**:
- Standing desk recommendations
- Ergonomic chair options
- Storage solutions
- Lighting scheme for productivity
- Total estimated cost: $4,800

## Advanced Usage

### Batch Processing
Process multiple rooms:

```python
from interactive_design import run_interactive_design

rooms = [
    {"image": "living_room.jpg", "prompt": "Modern minimalist", "budget": "moderate"},
    {"image": "bedroom.jpg", "prompt": "Cozy bohemian", "budget": "low"},
]

for room in rooms:
    # Process each room...
```

### API Integration
Integrate into your own application:

```python
from agents.visual_assessor import VisualAssessor
from agents.project_coordinator import ProjectCoordinator

# Analyze image
assessor = VisualAssessor()
analysis = assessor.analyze("path/to/image.jpg")

# Generate transformation
coordinator = ProjectCoordinator()
plan = coordinator.generate_project_plan(
    room_analysis=analysis,
    design_style="your_style",
    budget_range="moderate",
    reference_image="path/to/image.jpg"
)
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review example prompts for inspiration
3. Ensure your API key is valid and has quota
4. Try with a different, clearer image

## Future Enhancements

- [ ] Multiple design variations from one image
- [ ] Virtual staging for empty rooms
- [ ] 3D room visualization
- [ ] AR preview on mobile devices
- [ ] Integration with shopping platforms
- [ ] Actual image generation with Imagen API
- [ ] Before/after image comparison
- [ ] Export to PDF reports
- [ ] Share designs on social media

---

**Note**: This tool currently generates detailed text descriptions of transformed spaces. Actual image generation will be available when Google's Imagen API is integrated.
