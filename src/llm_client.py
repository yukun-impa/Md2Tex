import os
import google.generativeai as genai
from google.api_core import exceptions

class LLMClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro-latest')
        else:
            print("Warning: GEMINI_API_KEY not found. Using mock mode.")
            self.model = None

    def generate_latex(self, prompt, content):
        """
        Sends the prompt and content to the Gemini API.
        """
        if not self.model:
            return self._mock_response(content)

        full_prompt = f"{prompt}\n\n{content}"
        
        try:
            print("--- Sending to Gemini API ---")
            response = self.model.generate_content(full_prompt)
            print("--- Response received ---")
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return self._mock_response(content)

    def _mock_response(self, content):
        """
        Fallback mock response if no API key is present.
        """
        print("Using Mock Response...")
        latex_content = content.replace("# ", "\\section{").replace("## ", "\\subsection{")
        lines = latex_content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("\\section{") or line.startswith("\\subsection{"):
                lines[i] = line + "}"
        return "\n".join(lines)

