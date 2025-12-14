"""
API Connection Test Script
Verifies Google Gemini API connectivity before running POC
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

def test_api_connection():
    """Test Google Gemini API connection"""
    print("\n" + "="*70)
    print("🔧 TESTING GOOGLE GEMINI API CONNECTION")
    print("="*70)

    # Load environment variables
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')

    if not api_key:
        print("\n❌ ERROR: GOOGLE_API_KEY not found in .env file")
        print("\nPlease:")
        print("1. Copy .env.example to .env")
        print("2. Get your API key from https://aistudio.google.com/app/apikey")
        print("3. Add it to .env file: GOOGLE_API_KEY=your_key_here")
        return False

    if api_key == "your_google_api_key_here":
        print("\n❌ ERROR: Please replace 'your_google_api_key_here' with your actual API key")
        print("\nGet your key from: https://aistudio.google.com/app/apikey")
        return False

    print(f"\n✓ API key found (length: {len(api_key)} characters)")

    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        print("✓ Gemini configured")

        # Test basic text generation
        print("\n📝 Testing text generation...")
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say 'API connection successful!' if you can read this.")
        print(f"✓ Response: {response.text[:100]}...")

        # List available models
        print("\n📋 Listing available models...")
        available_models = []
        for m in genai.list_models():
            model_name = m.name
            available_models.append(model_name)
            if 'vision' in model_name.lower() or 'image' in model_name.lower() or 'flash' in model_name.lower():
                print(f"  ✓ {model_name}")

        print(f"\n✓ Found {len(available_models)} total models")

        # Success
        print("\n" + "="*70)
        print("✅ API CONNECTION TEST SUCCESSFUL!")
        print("="*70)
        print("\nYou're ready to run the POC!")
        print("Next step: python main.py")
        return True

    except Exception as e:
        print(f"\n❌ API CONNECTION FAILED: {str(e)}")
        print("\nPossible issues:")
        print("1. Invalid API key")
        print("2. Network connectivity problems")
        print("3. API quota exceeded")
        print("\nPlease check your API key and try again.")
        return False

if __name__ == "__main__":
    test_api_connection()
