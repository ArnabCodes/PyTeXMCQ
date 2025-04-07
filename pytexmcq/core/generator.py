"""
Core quiz generation functionality.
"""

import os
import random
import subprocess
import re
import hashlib
from pathlib import Path
from typing import Dict, List

from pytexmcq.config import config

class QuizGenerator:
    """Handles the generation of randomized quiz papers and answer keys."""
    
    def __init__(self):
        """Initialize the quiz generator with configuration settings."""
        self.questions = {}
        self._ensure_directories()
        
    def _ensure_directories(self) -> None:
        """Create necessary output directories if they don't exist."""
        config.OUTPUT_DIR.mkdir(exist_ok=True)
        config.ANSWERS_DIR.mkdir(exist_ok=True)
        
    def load_questions(self) -> None:
        """Load questions from topic files in the topics directory."""
        for topic_file in os.listdir(config.TOPICS_DIR):
            if topic_file.endswith('.tex'):
                topic = topic_file[:-4]  # Remove .tex extension
                file_path = config.TOPICS_DIR / topic_file
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Split content into individual questions
                    questions = re.split(r'\\begin{question}', content)[1:]
                    self.questions[topic] = []
                    for q in questions:
                        if q.strip():
                            # Remove marks from question
                            q = re.sub(r'\[\d+\]', '', q)
                            self.questions[topic].append('\\begin{question}' + q)
    
    def _get_seed(self, roll_number: str) -> int:
        """Generate a consistent random seed from a roll number."""
        return int(hashlib.md5(roll_number.encode()).hexdigest()[:8], 16)
    
    def _randomize_options(self, question: str, seed: int, is_answer_key: bool = False) -> str:
        """Randomize multiple choice options while preserving the correct answer."""
        random.seed(seed)
        
        pattern = r'\\begin{oneparcheckboxes}(.*?)\\end{oneparcheckboxes}'
        match = re.search(pattern, question, re.DOTALL)
        if not match:
            return question
            
        options_text = match.group(1)
        options = []
        current_option = ""
        for line in options_text.split('\n'):
            if line.strip().startswith('\\choice') or line.strip().startswith('\\correctchoice'):
                if current_option:
                    options.append(current_option)
                current_option = line
            else:
                current_option += '\n' + line
        if current_option:
            options.append(current_option)
        
        random.shuffle(options)
        
        if is_answer_key:
            new_options = '\n'.join(options)
        else:
            new_options = '\n'.join([opt.replace('\\correctchoice', '\\choice') for opt in options])
        
        return (
            question[:match.start()] +
            '\\begin{oneparcheckboxes}' +
            new_options +
            '\\end{oneparcheckboxes}' +
            question[match.end():]
        )
    
    def generate_paper(self, roll_number: str) -> None:
        """Generate a unique quiz paper and answer key for a given roll number."""
        main_seed = self._get_seed(roll_number)
        random.seed(main_seed)
        
        # Copy preamble to output directories
        for dir_path in [config.OUTPUT_DIR, config.ANSWERS_DIR]:
            preamble_dest = dir_path / "preamble.tex"
            if not preamble_dest.exists():
                with open(config.PREAMBLE_FILE, 'r') as src, open(preamble_dest, 'w') as dest:
                    dest.write(src.read())
        
        # Create title with roll number boxes
        title_boxes = ''.join([f"\\fsquare{{{c}}}" for c in roll_number])
        
        # Generate paper content
        paper_content = self._generate_paper_content(roll_number, title_boxes)
        answer_content = self._generate_answer_content(roll_number, title_boxes, main_seed)
        
        # Write and compile files
        base_filename = f"quiz_{roll_number}"
        self._write_and_compile_tex(config.OUTPUT_DIR / f"{base_filename}.tex", paper_content)
        self._write_and_compile_tex(config.ANSWERS_DIR / f"{base_filename}_answers.tex", answer_content)
    
    def _generate_paper_content(self, roll_number: str, title_boxes: str) -> str:
        """Generate the content for the question paper."""
        content = [
            r"\input{preamble}",
            "",
            self._generate_title(title_boxes),
            r"\begin{document}",
            r"\maketitle",
            r"\examheader",
            r"\begin{questions}"
        ]
        
        # Add randomized questions
        selected_questions = self._select_questions()
        random.shuffle(selected_questions)
        
        for i, question in enumerate(selected_questions):
            question_seed = self._get_seed(roll_number) + i
            content.append(self._randomize_options(question, question_seed, False))
        
        content.extend([
            r"\end{questions}",
            r"\end{document}"
        ])
        
        return '\n'.join(content)
    
    def _generate_answer_content(self, roll_number: str, title_boxes: str, main_seed: int) -> str:
        """Generate the content for the answer key."""
        content = [
            r"\input{preamble}",
            "",
            self._generate_title(title_boxes),
            r"\printanswers",
            r"\begin{document}",
            r"\maketitle",
            r"\examheader",
            r"\begin{questions}"
        ]
        
        # Add questions with preserved correct answers
        selected_questions = self._select_questions()
        random.seed(main_seed)
        random.shuffle(selected_questions)
        
        for i, question in enumerate(selected_questions):
            question_seed = self._get_seed(roll_number) + i
            content.append(self._randomize_options(question, question_seed, True))
        
        content.extend([
            r"\end{questions}",
            r"\end{document}"
        ])
        
        return '\n'.join(content)
    
    def _generate_title(self, title_boxes: str) -> str:
        """Generate the title section of the document."""
        return f"""\\title{{  \\large   Enrollment No. {title_boxes} \\\\ 
        \\vspace{{1cm}} \\normalsize {config.INSTITUTE} \\\\ 
        {config.DEPARTMENT} \\\\ {config.COURSE_CODE} \\\\ 
        {{\\vspace{{0.5 cm}} \\large \\bf{{{config.QUIZ_TITLE}}}}}}}"""
    
    def _select_questions(self) -> List[str]:
        """Select questions from each topic according to configuration."""
        selected = []
        for topic, count in config.QUESTIONS_PER_TOPIC.items():
            if topic in self.questions:
                topic_questions = random.sample(
                    self.questions[topic],
                    min(count, len(self.questions[topic]))
                )
                selected.extend(topic_questions)
        return selected
    
    def _write_and_compile_tex(self, tex_file: Path, content: str) -> None:
        """Write and compile a LaTeX file."""
        with open(tex_file, 'w') as f:
            f.write(content)
        
        try:
            # Change to the directory containing the tex file
            original_dir = os.getcwd()
            os.chdir(tex_file.parent)
            
            # Run pdflatex twice to ensure references are correct
            for _ in range(2):
                subprocess.run(
                    ['pdflatex', *config.LATEX_COMPILE_OPTIONS, tex_file.name],
                    check=True
                )
            
            # Return to original directory
            os.chdir(original_dir)
        except subprocess.CalledProcessError as e:
            print(f"Error compiling {tex_file}: {e}") 