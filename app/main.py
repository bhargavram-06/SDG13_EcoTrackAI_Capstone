import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Load workspace environment variables from .env profile for local development
load_dotenv()

class CarbonAIEngine:
    def __init__(self):
        """Initializes the Gemini Core engine safely checking Streamlit Secrets and local env."""
        # 1. First, check if running on Streamlit Cloud using their native secrets vault
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
        # 2. Fallback to local machine environment configuration
        else:
            api_key = os.getenv("GEMINI_API_KEY")

        if api_key:
            genai.configure(api_key=api_key)
            # Utilizing stable high-performance model profile
            self.model = genai.GenerativeModel("gemini-2.5-flash")
        else:
            self.model = None
            print("CRITICAL WARNING: GEMINI_API_KEY not detected inside active environment system configurations.")

    def clean_text_for_compatibility(self, raw_text):
        """Sanitizes text output to make it presentation-grade on mobile layout vectors."""
        if not raw_text:
            return ""
        # Strip out emojis to prevent text rendering artifacts on basic viewports
        clean_text = raw_text.encode('ascii', 'ignore').decode('ascii')
        # Filter down double asterisks or layout markups for flat clean lines
        clean_text = clean_text.replace("**", "").replace("* ", " - ").strip()
        return clean_text

    def extract_action_items(self, response_text):
        """
        Extracts exactly 3 clear, actionable goals from the AI text 
        to map safely into the Excel spreadsheet and PDF report rows.
        """
        # Fallback target lines if engine parsing has unexpected variance
        default_actions = [
            "Opt for public transit or carpooling twice this week.",
            "Unplug major household appliances when left on standby mode.",
            "Substitute one heavy meat meal with a green plant-based alternative."
        ]
        
        if not response_text:
            return default_actions
            
        # Parse output looking for list markers or sequential dash layouts
        lines = [line.strip() for line in response_text.split('\n') if line.strip()]
        bullets = []
        
        for line in lines:
            if line.startswith('-') or line.startswith('*') or (line[:1].isdigit() and line[1:2] in ['.', ')']):
                cleaned_bullet = line.lstrip('-*0123456789.) ').strip()
                if cleaned_bullet and len(cleaned_bullet) > 10:
                    bullets.append(cleaned_bullet)
                    
        if len(bullets) >= 3:
            return bullets[:3]
        return default_actions

    def generate_sustainability_plan(self, transport_co2, energy_co2, diet_co2, total_co2, context_dict):
        """
        Queries Gemini Core to compile a high-performance sustainability mitigation 
        matrix in pure compliance with UN SDG 13 framework boundaries.
        """
        if not self.model:
            return (
                "AI engine connection offline. Please check your system logs "
                "to confirm your GEMINI_API_KEY secret string is linked correctly."
            )

        # Formulate highly structured prompt context to govern generation limits
        prompt = f"""
        You are an expert UN SDG 13 Environmental Compliance Auditor. Provide a strict, premium quality carbon mitigation analysis report based on these individual parameters:
        
        USER CARBON PROFILE METRICS:
        - Daily Transportation Commute: {context_dict.get('vehicle', 'Unknown Mode')} pulling {transport_co2:.2f} kg CO2e/day (Total distance: {context_dict.get('distance', 0)} km)
        - Household Power Grid Consumption: {context_dict.get('electricity', 0)} kWh/Month pulling {energy_co2:.2f} kg CO2e/day
        - Dietary Habits Profile: {context_dict.get('diet', 'Unknown')} profile pulling {diet_co2:.2f} kg CO2e/day
        - Combined Daily Footprint Accumulated: {total_co2:.2f} kg CO2e
        - Calculated Platform Sustainability Rank: {context_dict.get('badge', 'Auditor Tier')} (Score: {context_dict.get('green_score', 50)}/100)

        REPORT COMPLIANCE REQUIREMENT STRUCTURE:
        1. Write a brief overview summary explaining what these numbers signify for climate action (under 3 lines).
        2. Provide exactly 3 short, concrete weekly actionable items to lower this specific footprint. Start each action item with a dash (-) character.
        
        CRITICAL STYLING LIMITS:
        - Talk naturally and professionally.
        - Do NOT include any technical code, programming terms, database details, or code logic variables.
        - Do NOT use any emojis or markdown symbols like asterisks (**).
        """

        try:
            response = self.model.generate_content(prompt)
            return self.clean_text_for_compatibility(response.text)
        except Exception as e:
            # Smart fallback handling if rate limits or minute caps are encountered during testing
            if "429" in str(e) or "quota" in str(e).lower():
                return (
                    "The AI system is taking a quick breath due to rapid usage caps. "
                    "Your metrics calculated perfectly above! Review your graphical metrics "
                    "or retry exporting your report centers in a moment."
                )
            return f"Environmental Analysis Engine Connection Fault: {str(e)}"