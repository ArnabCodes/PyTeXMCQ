# Physics Quiz Paper Generator - User Guide

## Overview
This system generates unique quiz papers for physics students, with randomized questions and options. Each student gets a unique paper based on their roll number, and corresponding answer keys are generated automatically.

## Installation

1. **System Requirements**:
   - Python 3.x
   - LaTeX distribution (with pdflatex)
   - Required Python packages: None (uses only standard library)

2. **Directory Setup**:
   ```
   Quiz 2/
   ├── generate_papers.py    # Main program
   ├── merge_pdfs.py        # PDF merging utility
   ├── preamble.tex         # LaTeX formatting template
   ├── roll_numbers.txt     # List of student roll numbers
   ├── topics/              # Question files by topic
   ├── papers/              # Generated question papers
   └── answers/             # Generated answer keys
   ```

## Usage Instructions

### 1. Setting Up Questions

1. Create question files in the `topics/` directory:
   - Each file should contain questions in LaTeX format
   - Example format:
     ```latex
     \begin{question}
     Question text
     \begin{oneparcheckboxes}
     \choice Option 1
     \choice Option 2
     \correctchoice Correct Option
     \choice Option 3
     \end{oneparcheckboxes}
     \end{question}
     ```

2. Add roll numbers to `roll_numbers.txt`:
   - One roll number per line
   - Example:
     ```
     BT24ECE001
     BT24ECE002
     BT24ECE003
     ```

### 2. Generating Papers

1. Run the generator:
   ```bash
   python generate_papers.py
   ```

2. The system will:
   - Generate unique papers for each roll number
   - Create corresponding answer keys
   - Compile all documents to PDF
   - Store files in `papers/` and `answers/` directories

3. Merge all PDFs:
   ```bash
   python merge_pdfs.py
   ```
   This creates:
   - `all_question_papers.pdf`
   - `all_answer_keys.pdf`

### 3. Customizing the Format

1. Edit `preamble.tex` to modify:
   - Paper title and header
   - Constants table
   - Formatting options
   - Question point values

2. Modify `generate_papers.py` to change:
   - Number of questions per topic
   - Question selection criteria
   - Output formatting

## Features

- **Unique Papers**: Each student gets a different paper based on their roll number
- **Randomization**: Questions and options are randomly ordered
- **Constants Table**: Each paper includes a table of physical constants
- **Answer Keys**: Automatic generation of answer keys
- **PDF Output**: Professional-looking PDFs with proper formatting

## Troubleshooting

1. **LaTeX Errors**:
   - Check if all required LaTeX packages are installed
   - Verify question formatting in topic files
   - Ensure preamble.tex is properly configured

2. **Python Errors**:
   - Verify Python version (3.x required)
   - Check file permissions
   - Ensure all required directories exist

3. **Missing Files**:
   - Verify roll_numbers.txt exists
   - Check topic files in topics/ directory
   - Ensure output directories (papers/, answers/) exist

## Maintenance

1. **Adding Questions**:
   - Add new questions to appropriate topic files
   - Follow the question format exactly
   - Mark correct answers with \correctchoice

2. **Updating Roll Numbers**:
   - Edit roll_numbers.txt
   - One roll number per line
   - No special characters or spaces

3. **Modifying Format**:
   - Edit preamble.tex for layout changes
   - Update generate_papers.py for logic changes
   - Test changes with a small set of roll numbers first 