import warnings

warnings.filterwarnings(
    "ignore",
    message=r"(?s).*google\.generativeai.*",
    category=FutureWarning,
)

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def test_gemini():
    api_key = os.getenv('GEMINI_API_KEY') or 'AIzaSyBe-IS8DDhhu8qDATObhFF1-x6vl2rV3JU'
    if not api_key:
        print("Error: GEMINI_API_KEY no encontrada.")
        return

    print(f"Usando API Key: {api_key[:5]}...{api_key[-5:]}")
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Di 'Hola, Gemini funciona correctamente'")
        
        print("\nGemini Respondio:")
        print(response.text)
        print("\nLa integracion con Gemini es exitosa (SDK legacy update).")
        
    except Exception as e:
        print(f"\nError probando Gemini: {e}")

if __name__ == "__main__":
    test_gemini()
