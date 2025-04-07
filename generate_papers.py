import os
import random
import subprocess
from pathlib import Path
import re
import hashlib
import shutil
from merge_pdfs import merge_pdfs

class QuestionPaperGenerator:
    def __init__(self, preamble_file, topics_dir, output_dir, answers_dir):
        self.preamble_file = preamble_file
        self.topics_dir = topics_dir
        self.output_dir = output_dir
        self.answers_dir = answers_dir
        self.questions = {}
        
        # Create output directories if they don't exist
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(answers_dir, exist_ok=True)
        
    def load_preamble(self):
        with open(self.preamble_file, 'r') as f:
            return f.read()
            
    def load_questions(self):
        for topic_file in os.listdir(self.topics_dir):
            if topic_file.endswith('.tex'):
                topic = topic_file[:-4]  # Remove .tex extension
                with open(os.path.join(self.topics_dir, topic_file), 'r') as f:
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
        # Set the main seed for this roll number
        main_seed = self.get_seed(roll_number)
        random.seed(main_seed)
        
        # Create output directories if they don't exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.answers_dir, exist_ok=True)
        
        # Copy preamble file to output directories
        shutil.copy2(self.preamble_file, os.path.join(self.output_dir, "preamble.tex"))
        shutil.copy2(self.preamble_file, os.path.join(self.answers_dir, "preamble.tex"))
        
        # Create question paper content
        paper_content = r"\input{preamble}" + "\n\n"
        # Create title with roll number split into individual boxes
        title_boxes = ''.join([f"\\fsquare{{{c}}}" for c in roll_number])
        paper_content += f"\\title{{  \\large   Enrollment No. {title_boxes} \\\\ \\vspace{{1cm}} \\normalsize Visvesvaraya National Institute of Technology, Nagpur \\\\ Department of Physics \\\\ PHL102, S Section \\\\ {{\\vspace{{0.5 cm}} \\large \\bf{{QUIZ 2}}}}}}\n"
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
        with open(os.path.join(self.output_dir, f"{base_filename}.tex"), 'w') as f:
            f.write(paper_content)
            
        # With answers
        answer_content = paper_content.replace("\\begin{document}", "\\printanswers\n\\begin{document}")
        # Rebuild the answer content with correct choices preserved
        answer_content = answer_content.split(r"\begin{questions}")[0] + r"\begin{questions}" + "\n"
        for i, question in enumerate(selected_questions):
            question_seed = main_seed + i
            answer_content += self.randomize_options(question, question_seed, is_answer_key=True)
        answer_content += r"\end{questions}" + "\n" + r"\end{document}"
        
        with open(os.path.join(self.answers_dir, f"{base_filename}_answers.tex"), 'w') as f:
            f.write(answer_content)
            
        # Compile LaTeX files
        self.compile_latex(os.path.join(self.output_dir, f"{base_filename}.tex"))
        self.compile_latex(os.path.join(self.answers_dir, f"{base_filename}_answers.tex"))
    
    def compile_latex(self, tex_file):
        try:
            # Get the directory and filename
            tex_dir = os.path.dirname(tex_file)
            tex_filename = os.path.basename(tex_file)
            
            # Change to the directory containing the tex file
            current_dir = os.getcwd()
            os.chdir(tex_dir)
            
            # Run pdflatex
            subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename], check=True)
            # Run twice to ensure references are correct
            subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename], check=True)
            
            # Change back to the original directory
            os.chdir(current_dir)
        except subprocess.CalledProcessError as e:
            print(f"Error compiling {tex_file}: {e}")

def load_roll_numbers(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    # Configuration
    preamble_file = "preamble.tex"
    topics_dir = "topics"
    output_dir = "papers"
    answers_dir = "answers"
    roll_numbers_file = "roll_numbers.txt"
    
    # Load roll numbers from file
    roll_numbers = load_roll_numbers(roll_numbers_file)
    
    # Example questions per topic configuration
    questions_per_topic = {
        "quantum_mechanics": 0,
        "quantum_applications": 0,
        "crystal_structure": 0,
        "semiconductor_physics": 11,
        "device_physics": 10,
        "laser_optics": 1
    }
    
    generator = QuestionPaperGenerator(preamble_file, topics_dir, output_dir, answers_dir)
    generator.load_questions()
    
    # Generate papers for all roll numbers
    for roll_number in roll_numbers:
        print(f"Generating paper for roll number: {roll_number}")
        generator.generate_paper(roll_number, questions_per_topic)
    
    print("All papers generated successfully!")
    
    # Merge all question papers and answer keys
    print("Merging question papers and answer keys...")
    merge_pdfs(output_dir, 'all_question_papers.pdf', 'quiz_')
    merge_pdfs(answers_dir, 'all_answer_keys.pdf', 'quiz_')
    print("Merging completed successfully!")

if __name__ == "__main__":
    main() 