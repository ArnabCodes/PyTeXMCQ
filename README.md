# Quiz Paper Generator

A Python-based tool for generating randomized quiz papers and answer keys in LaTeX format. This tool is designed to create unique question papers for each student while maintaining the same set of questions, just with randomized options and order.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Contributing](#contributing)

## Installation

### Prerequisites
- Python 3.8 or higher
- LaTeX distribution (TeX Live or MiKTeX)
- `pdflatex` command-line tool

### Step-by-Step Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd quiz-paper-generator
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify LaTeX installation**:
   ```bash
   pdflatex --version
   ```

## Quick Start

1. **Prepare your questions**:
   - Create `.tex` files in the `topics/` directory
   - Each file should contain questions in the format:
     ```latex
     \begin{question}[2]
     Your question here
     \begin{oneparcheckboxes}
     \choice Option A
     \correctchoice Option B
     \choice Option C
     \choice Option D
     \end{oneparcheckboxes}
     \end{question}
     ```

2. **Configure the generator**:
   - Edit `config.json` to specify:
     - Number of questions per topic
     - Roll number patterns

3. **Run the generator**:
   ```bash
   python generate_papers.py
   ```

4. **Find your output**:
   - `papers.pdf`: All question papers merged
   - `answers.pdf`: All answer keys merged

## Configuration

### config.json
The configuration file controls how papers are generated:

```json
{
    "questions_per_topic": {
        "quantum_mechanics": 0,
        "quantum_applications": 0,
        "crystal_structure": 0,
        "semiconductor_physics": 10,
        "device_physics": 10,
        "laser_optics": 1
    },
    "roll_numbers": [
        "BT24ECE01...04",
        "BT24ECE10",
        "BT24ECE15...18"
    ]
}
```

- `questions_per_topic`: Number of questions to select from each topic
- `roll_numbers`: List of roll number patterns
  - Use `...` for ranges (e.g., `BT24ECE01...04`)
  - Individual roll numbers can be specified directly

### preamble.tex
This file contains the LaTeX preamble and document settings. Modify it to change:
- Page layout
- Font settings
- Header/footer content
- Question formatting

## Usage

### Generating Papers
1. Place your question files in the `topics/` directory
2. Update `config.json` with your requirements
3. Run `python generate_papers.py`

### Output Files
- Individual papers: `quiz_<roll_number>.pdf`
- Individual answer keys: `quiz_<roll_number>_answers.pdf`
- Merged papers: `papers.pdf`
- Merged answer keys: `answers.pdf`

### Customizing Output
- Modify `preamble.tex` to change paper formatting
- Adjust `config.json` to change question distribution
- Edit question files in `topics/` to update content

## How It Works

### Core Components

1. **QuestionPaperGenerator Class**
   - Manages the entire paper generation process
   - Handles temporary file management
   - Coordinates LaTeX compilation

2. **ProgressIndicator Class**
   - Provides visual feedback during generation
   - Uses spinning animation for long operations
   - Shows success/failure status

### Key Processes

1. **Question Loading**
   - Reads `.tex` files from `topics/` directory
   - Parses questions and options
   - Stores questions by topic

2. **Randomization**
   - Uses roll number to generate consistent seeds
   - Randomizes question order
   - Shuffles options while preserving correct answers
   - Ensures each student gets a unique paper

3. **Paper Generation**
   - Creates LaTeX content for each paper
   - Compiles to PDF using `pdflatex`
   - Handles both question papers and answer keys

4. **PDF Merging**
   - Combines individual papers into single PDFs
   - Adds blank pages for odd-numbered papers
   - Maintains consistent formatting

### Technical Details

1. **Seed Generation**
   ```python
   def get_seed(self, roll_number):
       return int(hashlib.md5(roll_number.encode()).hexdigest()[:8], 16)
   ```
   - Converts roll number to consistent integer seed
   - Ensures same randomization for same roll number

2. **Option Randomization**
   ```python
   def randomize_options(self, question, seed, is_answer_key=False):
       random.seed(seed)
       # Preserves correct answers in answer key
       # Randomizes options in question paper
   ```

3. **PDF Merging**
   ```python
   def _create_merger(self, pdf_files):
       # Uses pdfpages package
       # Adds blank pages after each paper
       # Maintains consistent formatting
   ```

## Contributing

### Adding New Features

1. **Question Types**
   - Add support for different question formats
   - Implement new randomization methods
   - Create custom LaTeX environments

2. **Output Formats**
   - Support different paper sizes
   - Add custom headers/footers
   - Implement different answer key formats

3. **Configuration Options**
   - Add more customization options
   - Implement validation for config values
   - Create configuration templates

### Code Structure

1. **Main Components**
   - `QuestionPaperGenerator`: Core functionality
   - `ProgressIndicator`: User interface
   - Utility functions: Helper methods

2. **File Organization**
   - `topics/`: Question source files
   - `config.json`: Configuration
   - `preamble.tex`: LaTeX settings

3. **Temporary Files**
   - Created in system temp directory
   - Automatically cleaned up
   - Never stored in project directory

### Best Practices

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints
   - Document all functions

2. **Testing**
   - Add unit tests for core functions
   - Test different configurations
   - Verify output formats

3. **Documentation**
   - Keep README up to date
   - Document new features
   - Include usage examples

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using the LaTeX `exam` document class
- Inspired by the need for efficient quiz generation in academic settings 