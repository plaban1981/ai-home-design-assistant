# Home Design Assistant - POC

AI-powered interior design planning system using multi-agent architecture (CrewAI) and photorealistic rendering (Gemini/Nano Banana).

## 🎯 POC Goals

This Proof of Concept validates:
1. **Multi-agent orchestration** - Can CrewAI effectively coordinate VisualAssessor → ProjectCoordinator workflow?
2. **Vision API quality** - Does Gemini Vision extract useful room data?
3. **Rendering feasibility** - Can we generate trustworthy design renderings?
4. **Cost economics** - What are the actual API costs per user request?
5. **User value** - Do people trust the output enough to make buying decisions?

## 📦 What's Included

### Agents
- **VisualAssessor** - Analyzes room photos using Gemini Vision to extract room type, features, style, challenges, and opportunities
- **ProjectCoordinator** - Generates design renderings, budget breakdowns, timelines, and shopping lists

### Tools
- **ImageAnalyzer** - Gemini Vision wrapper for structured room analysis
- **ImageGenerator** - Gemini Image Generation wrapper for photorealistic renderings

### Workflow
```
User uploads photo
    ↓
VisualAssessor analyzes room
    ↓
ProjectCoordinator creates plan + rendering
    ↓
Results saved to output/
```

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.11 or higher
- Google API key (free tier available)

### 2. Installation

```bash
# Navigate to project directory
cd "C:\Users\nayak\Documents\Home_design assistant"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. API Key Setup

1. Get your Google API key:
   - Go to https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key

2. Create `.env` file:
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

### 4. Test API Connection

```bash
python test_api.py
```

You should see: ✅ API CONNECTION TEST SUCCESSFUL!

### 5. Add Test Photos

Place 1-5 room photos in the `test_photos/` directory:
- Supported formats: JPG, JPEG, PNG
- Clear, well-lit photos work best
- Include variety: living rooms, bedrooms, kitchens

Example:
```
test_photos/
  ├── living_room_01.jpg
  ├── bedroom_01.jpg
  └── kitchen_01.jpg
```

### 6. Run the POC

```bash
python main.py
```

The POC will:
1. Analyze the first photo in `test_photos/`
2. Generate a design plan with modern minimalist style
3. Save results to `output/poc_results_TIMESTAMP.json`

## 📊 Expected Output

```
🏠 HOME DESIGN POC - Multi-Agent Interior Design Planner
======================================================================

📍 STEP 1: Visual Assessment
----------------------------------------------------------------------
🔍 Visual Assessor analyzing: test_photos/living_room_01.jpg

📊 ROOM ANALYSIS SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━
Room Type: living_room
Current Style: traditional
Size: medium
Condition: needs_refresh
...

📍 STEP 2: Project Coordination & Rendering Generation
----------------------------------------------------------------------
🎨 Project Coordinator creating plan for modern minimalist design...

✅ Project Plan Generated!
Design Style: modern minimalist
Budget Range: moderate

🎨 RENDERING DESCRIPTION:
----------------------------------------------------------------------
[Detailed design description with materials, colors, layout...]

======================================================================
✅ POC WORKFLOW COMPLETE!
======================================================================
```

## 📁 Project Structure

```
Home_design assistant/
├── agents/                 # CrewAI agents
│   ├── __init__.py
│   ├── visual_assessor.py      # Room analysis agent
│   └── project_coordinator.py  # Design & rendering agent
├── tools/                  # Utility tools
│   ├── __init__.py
│   ├── image_analyzer.py       # Gemini Vision wrapper
│   └── image_generator.py      # Image generation wrapper
├── test_photos/            # Input photos (YOU ADD THESE)
├── output/                 # Generated results
├── tests/                  # Test metrics (future)
├── .env                    # API keys (YOU CREATE THIS)
├── .env.example            # Template for .env
├── config.py               # Configuration
├── main.py                 # Main POC entry point
├── test_api.py             # API connection test
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🧪 Success Metrics

### Technical Validation
- ✅ Room type classification: 80%+ accuracy
- ✅ End-to-end latency: <60 seconds (P95)
- ✅ API cost per run: <$2.00
- ✅ Error rate: <10%

### Quality Validation
- ✅ Visual similarity: Can users recognize their room?
- ✅ Trust factor: Would users make buying decisions based on this?
- ✅ Rendering quality: Professional enough to compete with existing tools?

## 🔧 Customization

### Change Design Style

Edit `main.py`:
```python
results = run_poc(
    image_path=test_image,
    design_style="industrial modern",  # Change this
    budget_range="high"
)
```

Available styles: modern minimalist, industrial, farmhouse, scandinavian, traditional, eclectic

### Test Refinement

Add after the main POC run in `main.py`:
```python
coordinator = ProjectCoordinator()
refined = coordinator.refine_design(
    previous_plan=project_plan,
    refinement_request="make colors warmer and add more plants"
)
```

## 📝 Notes

### Image Generation Status
- **Current**: Gemini generates detailed TEXT descriptions of renderings
- **Future**: When Imagen-3 API is available, will generate actual photorealistic images
- The POC validates the workflow and quality of descriptions

### API Costs (Approximate)
- Gemini Vision API: ~$0.01-0.05 per image analysis
- Gemini Text Generation: ~$0.001 per request
- **Total per POC run**: ~$0.02-0.10

### Rate Limits
- Free tier: 15 requests per minute
- Paid tier: Higher limits available

## 🐛 Troubleshooting

### "GOOGLE_API_KEY not found"
- Make sure you created `.env` file from `.env.example`
- Make sure API key is correct in `.env`

### "No test photos found"
- Add at least one image file to `test_photos/` directory
- Supported: .jpg, .jpeg, .png

### JSON parsing errors
- Gemini sometimes returns malformed JSON
- The code includes error handling for this
- If persistent, try a different photo or check API status

### Import errors
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

## 📈 Next Steps After POC

1. **Analyze results** - Review `output/poc_results_*.json`
2. **Test with real users** - Show renderings to 10 potential users
3. **Measure metrics** - Calculate actual accuracy, latency, costs
4. **Make go/no-go decision** based on success criteria
5. **If GO**: Implement additional agents (DesignPlanner, RenderingEditor)
6. **If NO-GO**: Pivot approach or adjust scope

## 🤝 Support

POC created by the BMAD team:
- 🚀 Barry (Quick Flow Solo Dev) - Implementation
- 💻 Amelia (Developer) - Technical validation
- 🏗️ Winston (Architect) - Architecture design
- 📊 Mary (Business Analyst) - Requirements & testing
- 📋 John (Product Manager) - Success criteria

## 📄 License

POC - Internal use only
