import os
import re
import json
import random
import hashlib
import shutil
import subprocess
import sys
import time
import threading
from pathlib import Path
import tempfile

class ProgressIndicator:
    def __init__(self, message):
        self.message = message
        self.is_running = False
        self.thread = None
        
    def animate(self):
        chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        i = 0
        while self.is_running:
            sys.stdout.write('\r' + chars[i % len(chars)] + ' ' + self.message)
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
            
    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.animate)
        self.thread.start()
        
    def stop(self, success=True):
        self.is_running = False
        if self.thread:
            self.thread.join()
        if success:
            sys.stdout.write('\r✓ ' + self.message + '\n')
        else:
            sys.stdout.write('\r✗ ' + self.message + '\n')
        sys.stdout.flush()

    def update(self, new_message):
        self.message = new_message

class QuestionPaperGenerator:
    def __init__(self, preamble_file, topics_dir):
        self.preamble_file = preamble_file
        self.topics_dir = topics_dir
        self.questions = {}
        self.temp_dir = None
        self.original_dir = None
        
    def setup_temp_dir(self):
        """Create a temporary directory for intermediate files."""
        # Create temp directory in system's temp directory
        self.temp_dir = tempfile.mkdtemp(prefix='quiz_generator_')
        # Copy preamble to temp directory once
        shutil.copy2(self.preamble_file, os.path.join(self.temp_dir, "preamble.tex"))
        # Store original directory and change to temp directory
        self.original_dir = os.getcwd()
        os.chdir(self.temp_dir)
            
    def load_questions(self):
        self.setup_temp_dir()
        topics_path = os.path.join(self.original_dir, self.topics_dir)
        for topic_file in os.listdir(topics_path):
            if topic_file.endswith('.tex'):
                topic = topic_file[:-4]  # Remove .tex extension
                with open(os.path.join(topics_path, topic_file), 'r') as f:
                    content = f.read()
                    # Split content into individual questions
                    questions = re.split(r'\\begin{question}', content)[1:]
                    self.questions[topic] = []
                    for q in questions:
                        if q.strip():
                            # Remove marks from question
                            q = re.sub(r'\[\d+\]', '', q)
                            self.questions[topic].append('\\begin{question}' + q)
    
    def get_seed(self, roll_number):
        # Convert roll number to a consistent integer seed
        return int(hashlib.md5(roll_number.encode()).hexdigest()[:8], 16)
    
    def randomize_options(self, question, seed, is_answer_key=False):
        # Set the random seed for this question
        random.seed(seed)
        
        # Find the oneparcheckboxes environment
        pattern = r'\\begin{oneparcheckboxes}(.*?)\\end{oneparcheckboxes}'
        match = re.search(pattern, question, re.DOTALL)
        if match:
            options_text = match.group(1)
            # Split options, preserving both \choice and \correctchoice
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
            
            # Randomize options
            random.shuffle(options)
            
            # Rebuild the options text
            if is_answer_key:
                # In answer key, preserve \correctchoice
                new_options = '\n'.join(options)
            else:
                # In question paper, convert all to \choice
                new_options = '\n'.join([opt.replace('\\correctchoice', '\\choice') for opt in options])
            
            # Replace the original options with randomized ones
            start = match.start()
            end = match.end()
            return question[:start] + '\\begin{oneparcheckboxes}' + new_options + '\\end{oneparcheckboxes}' + question[end:]
        return question
    
    def generate_paper(self, roll_number, questions_per_topic):
        progress = ProgressIndicator(f"Processing {roll_number}")
        progress.start()
        
        # Set the main seed for this roll number
        main_seed = self.get_seed(roll_number)
        random.seed(main_seed)
        
        # Create question paper content
        paper_content = r"\input{preamble}" + "\n\n"
        # Create title with roll number split into individual boxes
        title_boxes = ''.join([f"\\fsquare{{{c}}}" for c in roll_number])
        paper_content += f"\\title{{  \\large   Enrollment No. {title_boxes} \\\\ \\vspace{{1cm}} \\normalsize ABC Institute of Technology \\\\ Department of Physics \\\\ PHY101, X Section \\\\ {{\\vspace{{0.5 cm}} \\large \\bf{{QUIZ}}}}}}\n"
        paper_content += r"\begin{document}" + "\n"
        paper_content += r"\maketitle" + "\n"
        paper_content += r"\examheader" + "\n"
        paper_content += r"\begin{questions}" + "\n"
        
        # Select and randomize questions
        selected_questions = []
        for topic, count in questions_per_topic.items():
            if topic in self.questions:
                topic_questions = random.sample(self.questions[topic], min(count, len(self.questions[topic])))
                selected_questions.extend(topic_questions)
        
        # Randomize order of all questions
        random.shuffle(selected_questions)
        
        # Add questions to paper
        for i, question in enumerate(selected_questions):
            # Create a unique seed for each question by combining the main seed with the question index
            question_seed = main_seed + i
            paper_content += self.randomize_options(question, question_seed, is_answer_key=False)
        
        paper_content += r"\end{questions}" + "\n"
        paper_content += r"\end{document}"
        
        # Generate files with and without answers
        base_filename = f"quiz_{roll_number}"
        
        # Without answers
        with open(f"{base_filename}.tex", 'w') as f:
            f.write(paper_content)
            
        # With answers
        answer_content = paper_content.replace("\\begin{document}", "\\printanswers\n\\begin{document}")
        # Rebuild the answer content with correct choices preserved
        answer_content = answer_content.split(r"\begin{questions}")[0] + r"\begin{questions}" + "\n"
        for i, question in enumerate(selected_questions):
            question_seed = main_seed + i
            answer_content += self.randomize_options(question, question_seed, is_answer_key=True)
        answer_content += r"\end{questions}" + "\n" + r"\end{document}"
        
        with open(f"{base_filename}_answers.tex", 'w') as f:
            f.write(answer_content)
            
        # Compile LaTeX files in parallel
        def compile_tex(tex_file):
            try:
                subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file], 
                             check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file], 
                             check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError as e:
                print(f"Error compiling {tex_file}: {e}")
        
        # Create threads for parallel compilation
        threads = []
        for tex_file in [f"{base_filename}.tex", f"{base_filename}_answers.tex"]:
            thread = threading.Thread(target=compile_tex, args=(tex_file,))
            threads.append(thread)
            thread.start()
        
        # Wait for all compilations to complete
        for thread in threads:
            thread.join()
        
        progress.stop()

    def merge_pdfs(self, output_filename, prefix=''):
        """Merge all PDFs with given prefix into a single PDF."""
        progress = ProgressIndicator(f"Creating {output_filename}")
        progress.start()
        
        # Get all PDF files with the given prefix from temp directory
        pdf_files = [f for f in os.listdir(self.temp_dir) if f.startswith(prefix) and f.endswith('.pdf')]
        
        # Filter files based on whether we're creating papers or answers
        if output_filename == 'papers.pdf':
            pdf_files = [f for f in pdf_files if not f.endswith('_answers.pdf')]
        else:  # answers.pdf
            pdf_files = [f for f in pdf_files if f.endswith('_answers.pdf')]
            
        if not pdf_files:
            progress.stop(success=False)
            return

        # Sort files to ensure consistent order
        pdf_files.sort()
        
        # Create LaTeX content to merge PDFs
        latex_content = self._create_merger(pdf_files)
        
        # Write LaTeX content to file in temp directory
        merger_tex = os.path.join(self.temp_dir, 'merger.tex')
        with open(merger_tex, 'w') as f:
            f.write(latex_content)
            
        # Compile LaTeX file
        self.compile_latex('merger.tex', silent=True)
        
        # Move the merged PDF to original directory
        shutil.move(os.path.join(self.temp_dir, 'merger.pdf'), 
                   os.path.join(self.original_dir, output_filename))
        
        progress.stop()

    def _create_merger(self, pdf_files):
        """Create LaTeX content to merge PDFs."""
        latex_content = [
            r'\documentclass{article}',
            r'\usepackage{pdfpages}',
            r'\usepackage{graphicx}',
            r'\usepackage{hyperref}',
            r'\usepackage{afterpage}',
            r'\begin{document}',
        ]
        
        for pdf in pdf_files:
            latex_content.append(f'\\includepdf[pages=-,pagecommand={{\\afterpage{{\\clearpage\\mbox{{}}}}}}]{{{pdf}}}')
            
        latex_content.append(r'\end{document}')
        return '\n'.join(latex_content)

    def compile_latex(self, tex_file, silent=False):
        try:
            # Redirect output if silent
            output = subprocess.DEVNULL if silent else None
            
            subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file], 
                         check=True, stdout=output, stderr=output)
            subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file], 
                         check=True, stdout=output, stderr=output)
        except subprocess.CalledProcessError as e:
            print(f"Error compiling {tex_file}: {e}")

    def cleanup(self):
        """Remove temporary directory and all its contents."""
        # Change back to original directory
        os.chdir(self.original_dir)
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except Exception as e:
                print(f"✗ Error cleaning up temporary directory: {e}")

def expand_roll_numbers(roll_patterns):
    """Expand roll number patterns into individual roll numbers."""
    roll_numbers = []
    for pattern in roll_patterns:
        if '...' in pattern:
            # Handle range pattern (e.g., BT24ECE01...04)
            prefix, range_part = pattern.split('...')
            # Extract the last numeric part from prefix (e.g., '01' from 'BT24ECE01')
            prefix_parts = re.match(r'(.*?)(\d+)$', prefix)
            if prefix_parts:
                base_prefix = prefix_parts.group(1)  # 'BT24ECE'
                start_num = int(prefix_parts.group(2))  # 1
                end_num = int(range_part)  # 4
                num_width = len(prefix_parts.group(2))  # 2 (from '01')
                # Generate all numbers in the range
                for num in range(start_num, end_num + 1):
                    roll_number = f"{base_prefix}{num:0{num_width}d}"
                    roll_numbers.append(roll_number)
        else:
            # Handle single roll number
            roll_numbers.append(pattern)
    return roll_numbers

def main():
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Expand roll number patterns
    roll_numbers = expand_roll_numbers(config['roll_numbers'])
    
    # Initialize generator
    generator = QuestionPaperGenerator("preamble.tex", "topics")
    
    try:
        # Generate papers for all roll numbers
        generator.load_questions()
        for roll_number in roll_numbers:
            generator.generate_paper(roll_number, config['questions_per_topic'])
        
        # Merge all question papers and answer keys
        generator.merge_pdfs('papers.pdf', 'quiz_')
        generator.merge_pdfs('answers.pdf', 'quiz_')
        
        # Cleanup temporary files
        progress = ProgressIndicator("Cleaning up")
        progress.start()
        generator.cleanup()
        progress.stop()
        
        print("\n✨ All done! Find your PDFs in the current directory.")
    finally:
        # If we crashed, still try to clean up
        if 'progress' not in locals():
            generator.cleanup()

if __name__ == "__main__":
    main() 