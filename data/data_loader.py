"""
Functions for loading and managing data for the Country Guesser game
"""
import json
import os
from typing import Dict, List, Any

# Default data path
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def load_country_data() -> Dict[str, Dict[str, Any]]:
    """Load country data from JSON file"""
    try:
        with open(os.path.join(DATA_DIR, 'country_traits.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("country_traits.json file not found in the data directory")

def load_questions() -> List[Dict[str, Any]]:
    """Load questions from JSON file"""
    try:
        with open(os.path.join(DATA_DIR, 'questions.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # If file doesn't exist, create it with sample data
        sample_questions = _get_sample_questions()
        
        # Ensure the directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Write sample data to file
        with open(os.path.join(DATA_DIR, 'questions.json'), 'w', encoding='utf-8') as f:
            json.dump(sample_questions, f, indent=2)
        
        return sample_questions

def _get_sample_questions() -> List[Dict[str, Any]]:
    """
    Return sample questions data
    This is used to initialize the questions file if it doesn't exist
    """
    return [
        {
            "id": "continent_europe",
            "text": "Is the country located in Europe?",
            "trait": "continent",
            "match_value": "Europe",
            "category": "geography"
        },
        {
            "id": "continent_asia",
            "text": "Is the country located in Asia?",
            "trait": "continent",
            "match_value": "Asia",
            "category": "geography"
        },
        {
            "id": "continent_africa",
            "text": "Is the country located in Africa?",
            "trait": "continent",
            "match_value": "Africa",
            "category": "geography"
        },
        {
            "id": "continent_north_america",
            "text": "Is the country located in North America?",
            "trait": "continent",
            "match_value": "North America",
            "category": "geography"
        },
        {
            "id": "continent_south_america",
            "text": "Is the country located in South America?",
            "trait": "continent",
            "match_value": "South America",
            "category": "geography"
        },
        {
            "id": "continent_oceania",
            "text": "Is the country located in Oceania?",
            "trait": "continent",
            "match_value": "Oceania",
            "category": "geography"
        },
        {
            "id": "northern_hemisphere",
            "text": "Is the country in the Northern Hemisphere?",
            "trait": "hemisphere",
            "match_value": "Northern",
            "category": "geography"
        },
        {
            "id": "coastline",
            "text": "Does the country have a coastline?",
            "trait": "coastline",
            "match_value": True,
            "category": "geography"
        },
        {
            "id": "landlocked",
            "text": "Is the country landlocked (no access to the sea)?",
            "trait": "landlocked",
            "match_value": True,
            "category": "geography"
        },
        {
            "id": "monarchy",
            "text": "Is the country a monarchy (has a king or queen)?",
            "trait": "monarchy",
            "match_value": True,
            "category": "political"
        },
        {
            "id": "eu_member",
            "text": "Is the country a member of the European Union?",
            "trait": "eu_member",
            "match_value": True,
            "category": "political"
        },
        {
            "id": "climate_tropical",
            "text": "Does the country have tropical regions?",
            "trait": "tropical",
            "match_value": True,
            "category": "climate"
        },
        {
            "id": "climate_desert",
            "text": "Does the country have desert regions?",
            "trait": "desert",
            "match_value": True,
            "category": "climate"
        },
        {
            "id": "mountains",
            "text": "Does the country have significant mountain ranges?",
            "trait": "mountains",
            "match_value": True,
            "category": "geography"
        },
        {
            "id": "romance_language",
            "text": "Is the official language a Romance language (like Spanish, French, Italian)?",
            "trait": "language_group",
            "match_value": "Romance",
            "category": "cultural"
        },
        {
            "id": "germanic_language",
            "text": "Is the official language a Germanic language (like English, German, Dutch)?",
            "trait": "language_group",
            "match_value": "Germanic",
            "category": "cultural"
        },
        {
            "id": "slavic_language",
            "text": "Is the official language a Slavic language (like Russian, Polish, Czech)?",
            "trait": "language_group",
            "match_value": "Slavic",
            "category": "cultural"
        },
        {
            "id": "religion_christianity",
            "text": "Is Christianity the predominant religion?",
            "trait": "main_religion",
            "match_value": "Christianity",
            "category": "cultural"
        },
        {
            "id": "religion_islam",
            "text": "Is Islam the predominant religion?",
            "trait": "main_religion",
            "match_value": "Islam",
            "category": "cultural"
        },
        {
            "id": "tourism",
            "text": "Is the country a popular tourist destination?",
            "trait": "tourism",
            "match_value": True,
            "category": "economic"
        },
        {
            "id": "export_oil",
            "text": "Is oil or natural gas a major export?",
            "trait": "major_exports",
            "match_value": ["oil", "natural gas"],
            "category": "economic"
        },
        {
            "id": "export_technology",
            "text": "Is technology or electronics a major export?",
            "trait": "major_exports",
            "match_value": ["technology", "electronics"],
            "category": "economic"
        },
        {
            "id": "export_agriculture",
            "text": "Are agricultural products major exports?",
            "trait": "major_exports",
            "match_value": ["agricultural products", "coffee", "soybeans"],
            "category": "economic"
        }
    ]