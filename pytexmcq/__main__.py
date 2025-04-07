"""
Main entry point for PyTeXMCQ.
"""

import sys
from pathlib import Path
from typing import List

from pytexmcq.config import config
from pytexmcq.core.generator import QuizGenerator
from pytexmcq.utils.pdf_utils import merge_pdfs

def load_roll_numbers() -> List[str]:
    """Load roll numbers from the configuration file."""
    try:
        with open(config.ROLL_NUMBERS_FILE, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Roll numbers file not found at {config.ROLL_NUMBERS_FILE}")
        sys.exit(1)

def main() -> None:
    """Main function to generate quiz papers and answer keys."""
    print("PyTeXMCQ - LaTeX Quiz Generator")
    print("-" * 30)
    
    # Initialize the quiz generator
    generator = QuizGenerator()
    
    # Load questions from topic files
    print("Loading questions from topics...")
    generator.load_questions()
    
    # Load roll numbers
    roll_numbers = load_roll_numbers()
    
    # Generate papers for all roll numbers
    for roll_number in roll_numbers:
        print(f"Generating paper for roll number: {roll_number}")
        generator.generate_paper(roll_number)
    
    print("\nAll papers generated successfully!")
    
    # Merge PDFs
    print("\nMerging PDFs...")
    merge_pdfs(config.OUTPUT_DIR, 'all_question_papers.pdf', 'quiz_')
    merge_pdfs(config.ANSWERS_DIR, 'all_answer_keys.pdf', 'quiz_')
    print("PDF merging completed successfully!")

if __name__ == "__main__":
    main() 