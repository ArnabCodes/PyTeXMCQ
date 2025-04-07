# PyTeXMCQ

A powerful and flexible tool for generating randomized multiple-choice quizzes using LaTeX. Perfect for educators who need to create different versions of the same quiz for multiple students while maintaining consistency and professional formatting.

## Features

- 🎲 Generates unique quiz versions for each student
- 📝 Automatically creates answer keys
- 📊 Maintains consistent formatting across all versions
- 🔄 Combines all quizzes and answer keys into consolidated PDFs
- 📋 Supports custom LaTeX preamble for advanced formatting
- 🎯 Perfect for classroom settings with multiple students
- ⚙️ Highly configurable through a central configuration file

## Prerequisites

- Python 3.8 or higher
- LaTeX distribution (TeX Live or MiKTeX)
- Required Python packages (installed automatically)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ArnabCodes/PyTeXMCQ.git
cd PyTeXMCQ
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install the package in development mode:
```bash
pip install -e .
```

## Project Structure

```
PyTeXMCQ/
├── pytexmcq/                # Main package directory
│   ├── __init__.py         # Package initialization
│   ├── __main__.py         # Entry point
│   ├── config/             # Configuration
│   │   └── config.py       # Central configuration file
│   ├── core/               # Core functionality
│   │   └── generator.py    # Quiz generation logic
│   ├── templates/          # LaTeX templates
│   │   └── preamble.tex    # Document preamble
│   └── utils/              # Utility functions
│       └── pdf_utils.py    # PDF manipulation
├── topics/                 # Question bank directory
├── papers/                 # Generated question papers
├── answers/               # Generated answer keys
├── setup.py               # Package setup
├── requirements.txt       # Development dependencies
└── README.md             # This file
```

## Configuration

All configuration settings are centralized in `pytexmcq/config/config.py`:

- Quiz settings (title, department, course code)
- Number of questions per topic
- Physical constants for the quiz header
- File paths and directories
- LaTeX compilation options

## Usage

1. Create your question bank:
   - Place your questions in `.tex` files in the `topics/` directory
   - Follow the template format (see `USER_GUIDE.md`)

2. Configure the quiz:
   - Adjust settings in `pytexmcq/config/config.py`
   - Set the number of questions per topic
   - Customize quiz appearance

3. Set up student roll numbers:
   - Add roll numbers to `roll_numbers.txt` (one per line)

4. Generate quizzes:
```bash
python -m pytexmcq
```

This will:
- Generate unique papers for each roll number
- Create corresponding answer keys
- Merge papers into consolidated PDFs

## Development

To contribute to the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests (when available)
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using the LaTeX `exam` document class
- Inspired by the need for efficient quiz generation in academic settings 