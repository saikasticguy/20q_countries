from typing import Dict, List, Tuple, Any, Optional, Set
import random

class DecisionTree:
    
    def __init__(self, countries_data: Dict[str, Dict[str, Any]]):
        self.countries_data = countries_data
        
        # Score weights for different answers
        self.score_weights = {
            "Yes": 1.0,
            "No": -0.5,
            "Maybe": 0.2,
            "I don't know": 0.0
        }
        
        # Continent priority mapping (to help with geographic narrowing)
        self.continent_questions = {
            "continent_europe",
            "continent_asia", 
            "continent_africa",
            "continent_north_america", 
            "continent_south_america",
            "continent_oceania"
        }
        
    def get_next_question(
        self, 
        asked_questions: List[Tuple[str, str]], 
        country_scores: Dict[str, float]
    ) -> Optional[str]:
        from data.data_loader import load_questions
        
        # Get all questions
        all_questions = load_questions()
        
        # Filter out already asked questions
        asked_question_ids = {q for q, _ in asked_questions}
        available_questions = [q for q in all_questions if q["id"] not in asked_question_ids]
        
        if not available_questions:
            return None
            
        # Special case: If no questions asked yet, start with continent questions
        if not asked_questions:
            continent_questions = [q for q in available_questions 
                                  if q["id"] in self.continent_questions]
            if continent_questions:
                return random.choice(continent_questions)["text"]
        
        # Get top countries based on current scores
        top_countries = sorted(
            [(country, score) for country, score in country_scores.items() if score >= 0],
            key=lambda x: x[1],
            reverse=True
        )[:5]  # Focus on top 5 countries
        
        # If we have narrowed down continents, avoid asking continent questions
        continent_narrowed = False
        for question, answer in asked_questions:
            for q in all_questions:
                if q["text"] == question and q["id"] in self.continent_questions and answer == "Yes":
                    continent_narrowed = True
        
        # If we've narrowed down to a continent, don't ask more continent questions
        if continent_narrowed:
            available_questions = [q for q in available_questions 
                                  if q["id"] not in self.continent_questions]
        
        # Skip questions that would no longer be useful
        useful_questions = []
        
        for question in available_questions:
            # Calculate potential information gain
            trait = question["trait"]
            match_value = question["match_value"]
            
            # Skip if trait not relevant to top countries
            if all(trait not in self.countries_data[country] for country, _ in top_countries):
                continue
                
            # Check if question would be informative
            potential_yes = 0
            potential_no = 0
            
            for country, _ in top_countries:
                country_data = self.countries_data[country]
                if self._check_trait_match(country_data, trait, match_value):
                    potential_yes += 1
                else:
                    potential_no += 1
            
            # Only ask if question could split the top countries
            if potential_yes > 0 and potential_no > 0:
                useful_questions.append((question, abs(potential_yes - potential_no)))
        
        if not useful_questions:
            # If no useful questions among top countries, pick a random one
            if available_questions:
                return random.choice(available_questions)["text"]
            return None
            
        # Sort by how evenly the question splits the top countries
        useful_questions.sort(key=lambda x: x[1])
        
        # Return the question that will provide the most information
        return useful_questions[0][0]["text"]
        
    def update_scores(
        self,
        question: str,
        answer: str,
        country_scores: Dict[str, float]
    ) -> None:
        from data.data_loader import load_questions
        
        # Find the question details
        all_questions = load_questions()
        question_data = None
        
        for q in all_questions:
            if q["text"] == question:
                question_data = q
                break
                
        if not question_data:
            return
            
        # Get the trait and match value
        trait = question_data["trait"]
        match_value = question_data["match_value"]
        
        # Get score adjustment based on answer
        weight = self.score_weights.get(answer, 0)
        
        # Update scores for all countries
        for country, country_data in self.countries_data.items():
            # Check if the trait matches
            trait_matches = self._check_trait_match(country_data, trait, match_value)
            
            # Apply score adjustment based on match and weight
            if trait_matches:
                # If trait matches and answer is Yes, increase score
                if answer == "Yes":
                    country_scores[country] += weight
                # If trait matches but answer is No, decrease score
                elif answer == "No":
                    country_scores[country] -= 1.0
                # If Maybe, smaller adjustment
                elif answer == "Maybe":
                    country_scores[country] += weight
            else:
                # If trait doesn't match and answer is No, increase score
                if answer == "No":
                    country_scores[country] += abs(weight)
                # If trait doesn't match but answer is Yes, decrease score
                elif answer == "Yes":
                    country_scores[country] -= 1.0
                # If Maybe, smaller adjustment
                elif answer == "Maybe":
                    country_scores[country] -= weight * 0.5
    
    def _check_trait_match(
        self, 
        country_data: Dict[str, Any], 
        trait: str, 
        match_value: Any
    ) -> bool:
        # If trait doesn't exist for country, assume no match
        if trait not in country_data:
            return False
            
        country_value = country_data[trait]
        
        # Handle different types of matching
        if isinstance(country_value, list):
            # If country value is a list, check if match_value is in the list
            if isinstance(match_value, list):
                return any(val in country_value for val in match_value)
            return match_value in country_value
        elif isinstance(match_value, list):
            # If match_value is a list but country_value is not,
            # check if country_value is in match_value
            return country_value in match_value
        else:
            # Simple equality check
            return country_value == match_value