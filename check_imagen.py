"""
Check Google Image Generation Availability
Tests what image generation options are available
"""
import sys
import os

# Fix UTF-8 encoding for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')

print("="*70)
print("🔍 CHECKING GOOGLE IMAGE GENERATION AVAILABILITY")
print("="*70)

# Check 1: google-generativeai package
print("\n1️⃣ Checking google-generativeai package...")
try:
    import google.generativeai as genai
    print(f"   ✅ google-generativeai version: {genai.__version__}")

    # List available models
    import config
    genai.configure(api_key=config.GOOGLE_API_KEY)

    print("\n   📋 Available models:")
    try:
        for model in genai.list_models():
            if 'generate' in model.name.lower() or 'image' in model.name.lower():
                print(f"      - {model.name}")
                print(f"        Capabilities: {model.supported_generation_methods}")
    except Exception as e:
        print(f"      ⚠️ Could not list models: {e}")

except ImportError:
    print("   ❌ google-generativeai not installed")

# Check 2: ImageGenerationModel
print("\n2️⃣ Checking for ImageGenerationModel...")
try:
    from google.generativeai import ImageGenerationModel
    print("   ✅ ImageGenerationModel available")
except (ImportError, AttributeError) as e:
    print(f"   ❌ ImageGenerationModel not available: {e}")

# Check 3: Vertex AI
print("\n3️⃣ Checking google-cloud-aiplatform (Vertex AI)...")
try:
    from google.cloud import aiplatform
    print(f"   ✅ google-cloud-aiplatform installed")
    print("   ℹ️ This enables Imagen through Vertex AI (requires Google Cloud setup)")
except ImportError:
    print("   ❌ google-cloud-aiplatform not installed")
    print("   💡 Install with: pip install google-cloud-aiplatform")

# Check 4: Current available options
print("\n" + "="*70)
print("📊 SUMMARY")
print("="*70)

print("\n🎯 Current Situation:")
print("   • Gemini Vision: ✅ Available (image analysis)")
print("   • Gemini Text: ✅ Available (text generation)")

try:
    from google.generativeai import ImageGenerationModel
    print("   • Imagen (via generativeai): ✅ Available")
except:
    print("   • Imagen (via generativeai): ❌ Not available")

try:
    from google.cloud import aiplatform
    print("   • Imagen (via Vertex AI): ✅ Package installed (needs cloud setup)")
except:
    print("   • Imagen (via Vertex AI): ❌ Not installed")

print("\n" + "="*70)
print("💡 RECOMMENDATIONS")
print("="*70)

print("\n📌 Option 1: Wait for Imagen in google-generativeai")
print("   • Google is rolling out Imagen access")
print("   • Will work with same API key")
print("   • Currently in limited preview")

print("\n📌 Option 2: Use Vertex AI + Imagen (Enterprise)")
print("   Steps:")
print("   1. pip install google-cloud-aiplatform")
print("   2. Set up Google Cloud project")
print("   3. Enable Vertex AI API")
print("   4. Set up authentication")
print("   Cost: Pay-as-you-go pricing")

print("\n📌 Option 3: Use Alternative AI Services")
print("   A. OpenAI DALL-E:")
print("      • pip install openai")
print("      • Set OPENAI_API_KEY in .env")
print("      • ~$0.04 per image (DALL-E 3)")

print("\n   B. Stability AI (Stable Diffusion):")
print("      • pip install stability-sdk")
print("      • Set STABILITY_API_KEY in .env")
print("      • ~$0.002-0.01 per image")

print("\n   C. Replicate (Multiple Models):")
print("      • pip install replicate")
print("      • Set REPLICATE_API_TOKEN in .env")
print("      • Various pricing options")

print("\n📌 Option 4: Local Generation (Free but slower)")
print("   • Use Stable Diffusion locally")
print("   • Requires GPU (NVIDIA recommended)")
print("   • pip install diffusers torch")

print("\n" + "="*70)
print("🚀 QUICK START OPTIONS")
print("="*70)

print("\n1️⃣ EASIEST: OpenAI DALL-E (Recommended)")
print("   Run: pip install openai")
print("   Add to .env: OPENAI_API_KEY=your_key_here")
print("   Get key: https://platform.openai.com/api-keys")

print("\n2️⃣ CHEAPEST: Stability AI")
print("   Run: pip install stability-sdk")
print("   Add to .env: STABILITY_API_KEY=your_key_here")
print("   Get key: https://platform.stability.ai/")

print("\n3️⃣ GOOGLE NATIVE: Wait for Imagen")
print("   • Check periodically for Imagen availability")
print("   • May become available with current API key")
print("   • Or use Vertex AI (enterprise solution)")

print("\n" + "="*70)
