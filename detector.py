# detector.py (V3 - Cognitive Forensic Analyst)
import os
import json
import google.generativeai as genai

# --- Initialize the Google Gemini Client ---
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
except ImportError:
    print("Google Generative AI library not found. Please run 'pip install google-generativeai'")
    exit()
except Exception as e:
    print(f"Configuration Error: {e}")
    exit()

def get_analysis_prompt(article_text: str) -> str:
    """
    Formats the article text into the V3 Cognitive Forensic Analysis prompt.
    This prompt uses a multi-layered, chain-of-thought approach to maximize analytical depth.
    """
    return f"""
    **ROLE:** You are a Senior Analyst in a Digital Forensics and Media Integrity Unit. Your mission is to perform a rigorous, multi-faceted forensic analysis of the provided text to determine its authenticity and intent.

    **METHODOLOGY:** Execute the following four-step cognitive analysis. Perform these steps as an internal monologue (chain-of-thought) before rendering your final JSON output.

    * **Step 1: Psychological Tone & Intent Analysis.**
        * Analyze the language. Does it use emotionally charged, loaded, or sensationalized words? (e.g., "thugs," "slaughter," "unhinged").
        * What is the likely psychological effect on the reader? Is it designed to evoke outrage, fear, or confirmation bias?
        * What is the probable intent of the author? Is it to inform, persuade, entertain, or manipulate?

    * **Step 2: Logical Structure & Fallacy Detection.**
        * Examine the core arguments. Are they logically sound?
        * Identify any logical fallacies present (e.g., ad hominem attacks, strawman arguments, false dilemmas, oversimplification).
        * Does the conclusion logically follow from the premises?

    * **Step 3: Assertion & Evidence Scrutiny (Legal Cross-Examination Approach).**
        * Isolate every major factual claim made in the article. Treat each claim as "unverified until proven."
        * Does the article provide credible, verifiable sources for its claims? (e.g., links to official reports, direct quotes from named, reputable individuals, references to established news organizations).
        * How strong is the evidence? Is it primary (direct evidence) or secondary (hearsay, anonymous "sources")? An absence of verifiable evidence for an extraordinary claim is a strong indicator of fabrication.

    * **Step 4: Provenance & Source Context Clues.**
        * Based *only on the text provided*, are there clues to the source's nature? Does it cite a reputable agency like "Reuters" or "Associated Press"? Or does it feel more like a blog post, opinion piece, or propaganda?
        * Synthesize the findings from Steps 1-3 to form a final hypothesis about the text's authenticity.

    **FINAL TASK:** After completing your internal cognitive analysis, provide your findings ONLY in the specified JSON format. Your reasoning should be a concise summary of your most critical findings from the four-step analysis.

    **ARTICLE FOR ANALYSIS:**
    ---
    {article_text}
    ---

    **CRITICAL OUTPUT DIRECTIVES:**
    1.  Your final verdict MUST be "Real" or "Fake". Avoid "Uncertain" unless the text is pure opinion with zero factual claims.
    2.  Your entire response must be ONLY the raw JSON object, without any markdown formatting.

    **JSON OUTPUT FORMAT:**
    {{
      "verdict": "[Real/Fake]",
      "confidence_score": <A number between 0 and 100, representing your certainty in the verdict>,
      "reason": "<A concise summary of your forensic analysis, referencing the key factors (psychological, logical, evidentiary) that led to your conclusion>",
      "analysis_summary": {{
        "psychological_intent": "<Briefly describe the likely intent and emotional manipulation tactics>",
        "logical_fallacies": ["<List any identified logical fallacies, e.g., 'Ad Hominem', 'Oversimplification'>"],
        "evidence_quality": "<Assess the evidence as 'Strong', 'Weak', 'Circumstantial', or 'Non-existent'>"
      }}
    }}
    """

def analyze_article(article_text: str) -> dict:
    """
    Analyzes a single news article for fakeness using the Google Gemini API.
    Returns a dictionary with the analysis.
    """
    if not article_text or not article_text.strip():
        # Handle empty or whitespace-only strings
        return {"error": "Article text is empty."}
        
    prompt = get_analysis_prompt(article_text)
    
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        # Increased timeout for potentially more complex analysis
        request_options = {"timeout": 120}
        
        response = model.generate_content(prompt, request_options=request_options)
        
        # Robust cleaning of the response to ensure it's valid JSON
        cleaned_response_text = response.text.strip().lstrip('```json').rstrip('```').strip()

        analysis_json = json.loads(cleaned_response_text)
        return analysis_json
    except json.JSONDecodeError as e:
        print(f"JSON Parsing Error: {e}\nRaw Response was: '{cleaned_response_text}'")
        return {"error": f"JSON Parsing Error: {e}"}
    except Exception as e:
        print(f"An API or other error occurred: {e}")
        return {"error": str(e)}

# --- This section allows us to test the script directly ---
if __name__ == "__main__":
    test_article = """
    Sources within the 'Global Weather Consortium' have leaked a preliminary report suggesting
    that unusual solar flare activity is set to cause a two-day global internet outage next month.
    The report warns of unprecedented disruption. Major tech companies are reportedly holding
    emergency meetings, though no official statements have been released.
    """

    print("--- Testing the V3 Cognitive Forensic Analysis ---")
    result = analyze_article(test_article)

    print(json.dumps(result, indent=2))