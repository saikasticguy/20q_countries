""" 20Q Countries - A CLI game that tries to guess the country you're thinking of """
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from country_guesser import CountryGuesser

def display_welcome():
    console = Console()
    
    title = Text("🌍 COUNTRY GUESSER 🌎", style="bold cyan")
    instructions = Text.from_markup(
        "Think of a country and I'll try to guess it by asking you questions.\n"
        "For each question, you can answer:\n"
        "• [green]Yes[/green] - if the statement is true\n"
        "• [red]No[/red] - if the statement is false\n"
        "• [yellow]Maybe[/yellow] - if it's partially true or you're unsure\n"
        "• [blue]I don't know[/blue] - if you have no idea\n\n"
        "Ready to begin? Let's go!"
    )
    
    console.print("\n")
    console.print(Panel(title, expand=False, border_style="cyan"))
    console.print("\n")
    console.print(Panel(instructions, expand=False, border_style="white"))
    console.print("\n")

def main():
    display_welcome()
    
    # Default max questions is 20, but can be configured via command-line arg
    max_questions = 20
    if len(sys.argv) > 1:
        try:
            max_questions = int(sys.argv[1])
        except ValueError:
            print(f"Invalid number of questions: {sys.argv[1]}. Using default: 20")
    
    # Initialize and start the game
    guesser = CountryGuesser(max_questions=max_questions)
    guesser.play()

if __name__ == "__main__":
    main()