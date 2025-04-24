import time
import json
import os
from typing import Dict, List, Tuple, Any

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

from logic.decision_tree import DecisionTree

class CountryGuesser:
    
    def __init__(self, max_questions: int = 20):
        self.console = Console()
        self.max_questions = max_questions
        self.countries_data = self._load_country_data()
        self.questions = self._load_questions()
        self.decision_tree = DecisionTree(self.countries_data)
        
        # Track game state
        self.asked_questions = []
        self.current_question_num = 0
        self.country_scores = {country: 0 for country in self.countries_data}
        
    def _load_country_data(self) -> Dict[str, Dict[str, Any]]:
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        try:
            with open(os.path.join(data_dir, 'country_traits.json'), 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("country_traits.json file not found in the data directory")

    def _load_questions(self) -> List[Dict[str, Any]]:
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        try:
            with open(os.path.join(data_dir, 'questions.json'), 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # If file doesn't exist, create it with sample data
            sample_questions = self._get_sample_questions()
            
            # Ensure the directory exists
            os.makedirs(data_dir, exist_ok=True)
            
            # Write sample data to file
            with open(os.path.join(data_dir, 'questions.json'), 'w', encoding='utf-8') as f:
                json.dump(sample_questions, f, indent=2)
            
            return sample_questions


    def play(self):
        """Main game loop"""
        self.reset_game()
        
        # Ask if user is thinking of a country
        if not self._confirm_ready():
            self.console.print("[yellow]Maybe next time then! Goodbye![/yellow]")
            return
            
        # Start asking questions
        while self.current_question_num < self.max_questions:
            # Get next best question
            question = self.decision_tree.get_next_question(
                self.asked_questions, 
                self.country_scores
            )
            
            if not question:
                self.console.print("[yellow]I've run out of questions![/yellow]")
                break
                
            # Ask the question and process answer
            self.current_question_num += 1
            answer = self._ask_question(question)
            self.asked_questions.append((question, answer))
            
            # Update country scores based on the answer
            self.decision_tree.update_scores(
                question, 
                answer, 
                self.country_scores
            )
            
            # Check if we can make a confident guess
            top_countries = self._get_top_countries(3)
            confidence = self._calculate_confidence(top_countries)
            
            if confidence > 0.7:
                break
        
        # Make the final guess
        self._make_guess()
    
    def reset_game(self):
        self.asked_questions = []
        self.current_question_num = 0
        self.country_scores = {country: 0 for country in self.countries_data}
    
    def _confirm_ready(self) -> bool:
        return questionary.confirm(
            "🤔 Are you thinking of a country?",
            default=True
        ).ask()
    
    def _ask_question(self, question: str) -> str:
        progress_text = f"Question {self.current_question_num}/{self.max_questions}"
        self.console.print(f"\n[cyan]{progress_text}[/cyan]")
        
        # Display the question with a slight delay
        time.sleep(0.5)
        self.console.print(f"[bold white]{question}[/bold white]")
        
        # Get the user's answer
        answer = questionary.select(
            "Your answer:",
            choices=["Yes", "No", "Maybe", "I don't know"],
            style=questionary.Style([
                ('selected', 'bg:cyan fg:black'),
                ('pointer', 'fg:cyan bold'),
            ])
        ).ask()
        
        return answer
    
    def _get_top_countries(self, n: int = 3) -> List[Tuple[str, float]]:
        # Convert scores to a list of (country, score) tuples and sort
        sorted_countries = sorted(
            self.country_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return sorted_countries[:n]
    
    def _calculate_confidence(self, top_countries: List[Tuple[str, float]]) -> float:
        if not top_countries:
            return 0.0
            
        # If the top country has a much higher score than the second
        if len(top_countries) > 1:
            top_score = top_countries[0][1]
            second_score = top_countries[1][1]
            
            if top_score > 0:
                return min(1.0, (top_score - second_score) / top_score)
        
        return 0.0
    
    def _make_guess(self):
        top_countries = self._get_top_countries(3)
        
        if not top_countries:
            self.console.print("[red]I'm sorry, I couldn't guess your country.[/red]")
            return
            
        # Create a spinner animation for "thinking"
        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]Analyzing your answers...[/cyan]"),
            console=self.console,
        ) as progress:
            progress.add_task("", total=None)
            time.sleep(2)
        
        self.console.print()
        
        # Calculate confidence
        confidence = self._calculate_confidence(top_countries)
        top_country, top_score = top_countries[0]
        
        # Make a confident guess if possible
        if confidence > 0.7:
            guess_message = Text(f"I'm confident you're thinking of... {top_country}!")
            self.console.print(Panel(
                guess_message,
                title="🎯 My Guess",
                border_style="green",
                expand=False
            ))
        else:
            # Show multiple possibilities
            guess_panel = Text()
            guess_panel.append("Based on your answers, you might be thinking of:\n\n")
            
            for i, (country, score) in enumerate(top_countries):
                percentage = min(100, int(score * 100 / max(1, top_score)))
                guess_panel.append(f"{i+1}. {country} ", style="bold")
                guess_panel.append(f"({percentage}% confidence)\n")
                
            self.console.print(Panel(
                guess_panel,
                title="🤔 My Top Guesses",
                border_style="yellow",
                expand=False
            ))
        
        # Ask if the guess was correct
        correct = questionary.confirm(
            "Was my guess correct?",
            default=True
        ).ask()
        
        if correct:
            self.console.print("\n[green]Awesome! I guessed it correctly![/green] 🎉")
        else:
            actual_country = questionary.text("What country were you thinking of?").ask()
            self.console.print(f"\n[yellow]Thanks! I'll learn from this to make better guesses in the future.[/yellow]")