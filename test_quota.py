"""Quick test to check if Gemini API key has quota remaining."""
from google import genai
from src.config import Config

def test_quota():
    try:
        client = genai.Client(api_key=Config.GEMINI_API_KEY)
        
        # Minimal text request (uses very few tokens)
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents="Say 'OK' in one word."
        )
        
        print(f"✅ API Key works! Response: {response.text}")
        print("You have quota remaining.")
        return True
        
    except Exception as e:
        error_str = str(e)
        print(f"❌ Error: {error_str}")
        
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            print("\n⚠️  Your quota is EXHAUSTED for today.")
            print("Options:")
            print("  1. Wait until tomorrow (quota resets daily)")
            print("  2. Use a different Google account's API key")
            print("  3. Enable billing for unlimited usage")
        
        return False

if __name__ == "__main__":
    test_quota()
