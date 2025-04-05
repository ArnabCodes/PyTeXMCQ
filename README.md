# LaTeX Quiz Generator

A powerful and flexible tool for generating randomized multiple-choice quizzes using LaTeX. Perfect for educators who need to create different versions of the same quiz for multiple students while maintaining consistency and professional formatting.

## Features

- 🎲 Generates unique quiz versions for each student
- 📝 Automatically creates answer keys
- 📊 Maintains consistent formatting across all versions
- 🔄 Combines all quizzes and answer keys into consolidated PDFs
- 📋 Supports custom LaTeX preamble for advanced formatting
- 🎯 Perfect for classroom settings with multiple students

## Prerequisites

- Python 3.8 or higher
- LaTeX distribution (TeX Live or MiKTeX)
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/latex-quiz-generator.git
cd latex-quiz-generator
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Project Structure

```
latex-quiz-generator/
├── generate_papers.py     # Main script for generating quizzes
├── merge_pdfs.py         # Script for combining PDFs
├── preamble.tex          # LaTeX preamble with formatting
├── roll_numbers.txt      # List of student roll numbers
├── papers/              # Directory for question papers
├── answers/             # Directory for answer keys
└── topics/             # Directory for question banks
```

## Usage

1. Create your question bank:
   - Place your questions in `.tex` files in the `topics/` directory
   - Follow the template format (see example in `USER_GUIDE.md`)

2. Set up student roll numbers:
   - Add roll numbers to `roll_numbers.txt` (one per line)

3. Generate quizzes:
```bash
python generate_papers.py
```

4. Merge all papers into consolidated PDFs:
```bash
python merge_pdfs.py
```

## Question Format

Questions should be written in LaTeX using the `exam` document class. Example:

```latex
\question[0.5] What is the correct answer?
\begin{oneparcheckboxes}
    \choice Incorrect option
    \CorrectChoice Correct option
    \choice Another incorrect option
    \choice Yet another incorrect option
\end{oneparcheckboxes}
```

For more detailed formatting instructions, see `USER_GUIDE.md`.

## Customization

- Modify `preamble.tex` to customize the quiz appearance
- Adjust spacing and formatting in the LaTeX preamble
- Customize headers, footers, and page layout

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using the LaTeX `exam` document class
- Inspired by the need for efficient quiz generation in academic settings 