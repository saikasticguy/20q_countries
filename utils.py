import random
import time
from typing import List, Dict, Any

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

def animate_text(console: Console, text: str, delay: float = 0.03) -> None:
    for char in text:
        console.print(char, end="", highlight=False)
        time.sleep(delay)
    console.print()

def get_random_encouragement() -> str:
    messages = [
        "Good choice!",
        "Interesting...",
        "I'm getting closer!",
        "That helps a lot!",
        "Now we're making progress!",
        "Hmm, let me think about that...",
        "I'm starting to narrow it down!",
        "That's useful information!",
    ]
    return random.choice(messages)

def format_country_info(country: str, country_data: Dict[str, Any]) -> Text:
    text = Text()
    text.append(f"{country}\n\n", style="bold cyan")
    
    # Add basic info
    text.append("Location: ", style="bold")
    if isinstance(country_data.get("continent"), list):
        text.append(", ".join(country_data["continent"]))
    else:
        text.append(str(country_data.get("continent", "Unknown")))
    text.append(" (")
    text.append(str(country_data.get("hemisphere", "Unknown")))
    text.append(" Hemisphere)\n")
    
    # Climate
    text.append("Climate: ", style="bold")
    if isinstance(country_data.get("climate"), list):
        text.append(", ".join(country_data["climate"]))
    else:
        text.append(str(country_data.get("climate", "Unknown")))
    text.append("\n")
    
    # Geography
    geo_traits = []
    if country_data.get("coastline"):
        geo_traits.append("has coastline")
    if country_data.get("landlocked"):
        geo_traits.append("landlocked")
    if country_data.get("mountains"):
        geo_traits.append("mountainous")
    if country_data.get("desert"):
        geo_traits.append("has deserts")
    if country_data.get("tropical"):
        geo_traits.append("has tropical regions")
    
    if geo_traits:
        text.append("Geography: ", style="bold")
        text.append(", ".join(geo_traits))
        text.append("\n")
    
    # Language and culture
    text.append("Language group: ", style="bold")
    text.append(str(country_data.get("language_group", "Unknown")))
    text.append("\n")
    
    text.append("Main religion: ", style="bold")
    text.append(str(country_data.get("main_religion", "Unknown")))
    text.append("\n")
    
    # Political
    political_traits = []
    if country_data.get("monarchy"):
        political_traits.append("monarchy")
    if country_data.get("eu_member"):
        political_traits.append("EU member")
    
    if political_traits:
        text.append("Political: ", style="bold")
        text.append(", ".join(political_traits))
        text.append("\n")
    
    # Famous for
    if country_data.get("famous_for"):
        text.append("Famous for: ", style="bold")
        if isinstance(country_data["famous_for"], list):
            text.append(", ".join(country_data["famous_for"]))
        else:
            text.append(str(country_data["famous_for"]))
        text.append("\n")
    
    # Exports
    if country_data.get("major_exports"):
        text.append("Major exports: ", style="bold")
        if isinstance(country_data["major_exports"], list):
            text.append(", ".join(country_data["major_exports"]))
        else:
            text.append(str(country_data["major_exports"]))
    
    return text