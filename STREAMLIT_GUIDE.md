# Streamlit AI Home Design Assistant

Beautiful web interface for transforming your space with AI!

## Quick Start

### Option 1: Double-click (Windows)
```
Double-click: run_app.bat
```

### Option 2: Command Line
```bash
streamlit run streamlit_app.py
```

The app will open automatically in your browser at: `http://localhost:8501`

## Features

### 🏠 Complete Workflow
1. **Upload Image** - Drag and drop your room photo
2. **Customize Settings** - Choose style, budget, and vision
3. **AI Analysis** - Get professional room assessment
4. **Image Generation** - See your transformed space with Nano Banana
5. **Project Plan** - Receive budget, timeline, and shopping list

### ⚙️ Customization Options

**Design Styles:**
- Modern Minimalist
- Cozy Bohemian
- Industrial Loft
- Scandinavian
- Contemporary
- Rustic Farmhouse
- Mid-Century Modern
- Coastal
- Traditional

**Budget Ranges:**
- Low ($1,000 - $3,000)
- Moderate ($3,000 - $7,000)
- High ($7,000+)

**Custom Prompt:**
Describe your ideal space in natural language!

## What You'll See

### Left Panel: Original Room
- Your uploaded photo
- Upload status

### Right Panel: Transformed Design
- AI-generated transformed image (1024x1024)
- Download button for the image

### Analysis Section
- Room type, size, style
- Current features
- Challenges and opportunities
- Professional assessment

### Transformation Section
- Transformed image display
- Detailed description
- Complete project plan
- Budget breakdown
- Timeline estimate
- Shopping list with retailers

## Example Usage

### 1. Upload Image
Click "Browse files" or drag and drop your room photo

### 2. Customize (Sidebar)
```
Design Style: Modern Minimalist
Budget Range: Moderate
Custom Vision: "Cozy reading nook with warm lighting,
comfortable seating, and built-in bookshelves"
```

### 3. Click "Transform My Space"
The AI will:
- Analyze your room
- Generate transformed image
- Create project plan
- Provide budget & timeline

### 4. View Results
- See transformed image side-by-side
- Read detailed descriptions
- Review budget and timeline
- Download transformed image

## Tips for Best Results

### 📸 Image Quality
- Use well-lit photos
- Capture entire room if possible
- Avoid filters or heavy editing
- Higher resolution = better results

### ✍️ Custom Prompts
- Be specific about colors, materials
- Mention must-keep features
- Describe the atmosphere you want
- Reference specific styles

### 💰 Budget Settings
- Choose realistic budget range
- Consider existing furniture
- Factor in labor costs
- Include contingency (15%)

## Keyboard Shortcuts

- `R` - Rerun the app
- `C` - Clear cache
- `?` - Show keyboard shortcuts

## Troubleshooting

### App won't start
```bash
# Check if Streamlit is installed
pip list | grep streamlit

# Reinstall if needed
pip install streamlit
```

### Image upload fails
- Check file format (JPG, PNG only)
- Ensure file size < 200MB
- Try different browser

### Generation fails
- Check internet connection
- Verify GOOGLE_API_KEY in .env
- Check API quota

### Image not displaying
- Wait for generation to complete
- Check output/rendered_images/ folder
- Refresh the page

## Advanced Features

### Download Results
- Click "Download Transformed Image"
- Saves as PNG with timestamp
- High resolution (1024x1024)

### Multiple Transformations
- Upload new image anytime
- Try different styles
- Experiment with prompts

### Session State
- Results persist during session
- Scroll to see all details
- Expand/collapse sections

## Output Files

Generated images saved to:
```
output/rendered_images/nano_banana_TIMESTAMP.png
```

Temporary uploads saved to:
```
temp/uploads/upload_TIMESTAMP_filename.jpg
```

## Performance

**Typical Processing Time:**
- Image upload: Instant
- Room analysis: 10-30 seconds
- Image generation: 20-60 seconds
- Total: ~1-2 minutes

**Resource Usage:**
- RAM: ~500MB
- CPU: Light
- Network: API calls to Google

## Privacy & Security

- Images stored locally only
- Temporary files auto-cleaned
- API calls encrypted
- No data shared with third parties

## Features Overview

| Feature | Status |
|---------|--------|
| Image Upload | ✅ |
| Room Analysis | ✅ |
| Custom Prompts | ✅ |
| Style Selection | ✅ |
| Budget Planning | ✅ |
| Image Generation | ✅ |
| Project Timeline | ✅ |
| Shopping List | ✅ |
| Download Image | ✅ |
| Responsive UI | ✅ |

## Example Prompts

### Bedroom
```
Serene minimalist bedroom with white walls, natural wood
furniture, soft lighting, and plenty of plants
```

### Living Room
```
Cozy living room with warm neutrals, comfortable sectional,
gallery wall, and ambient lighting
```

### Home Office
```
Productive workspace with ergonomic desk, organized storage,
natural light, and inspiring decor
```

### Kitchen
```
Modern farmhouse kitchen with white cabinets, butcher block
counters, and vintage accents
```

## Mobile Support

The app is responsive and works on:
- Desktop ✅
- Tablet ✅
- Mobile ⚠️ (limited, desktop recommended)

## Browser Support

Tested on:
- Chrome ✅
- Firefox ✅
- Edge ✅
- Safari ✅

## API Credits

Uses Google AI APIs:
- Gemini Vision (analysis)
- Gemini 2.5 Flash (text)
- Nano Banana (image generation)

All included in standard API quota.

## Getting Help

Issues? Check:
1. Console for error messages
2. API quota status
3. .env configuration
4. Internet connection

## Updates

To update the app:
```bash
git pull
pip install -r requirements.txt
```

---

**Enjoy transforming your space with AI! 🏠✨**
