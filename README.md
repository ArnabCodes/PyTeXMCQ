# PyTeXMCQ

A powerful tool for generating randomized multiple-choice quizzes using LaTeX.

## Features

- Generate unique quiz papers for each student
- Randomize question order and multiple-choice options
- Support for mathematical equations and scientific notation
- Automatic answer key generation
- Customizable LaTeX preamble
- High configurability through central configuration file
- Professional project structure following Python best practices

## Prerequisites

- Python 3.8 or higher
- LaTeX distribution (TeX Live recommended)
- Required Python packages (will be installed automatically)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ArnabCodes/PyTeXMCQ.git
cd PyTeXMCQ
```

2. Install the package in development mode:
```bash
pip install -e .
```

## Project Structure

```
PyTeXMCQ/
├── pytexmcq/                  # Main package directory
│   ├── core/                  # Core functionality
│   │   └── generator.py       # Quiz generation logic
│   ├── config/                # Configuration management
│   │   └── config.py          # Central configuration file
│   ├── templates/             # LaTeX templates
│   │   └── preamble.tex       # LaTeX preamble template
│   ├── utils/                 # Utility functions
│   │   └── pdf_utils.py       # PDF operations
│   ├── __init__.py           # Package initialization
│   └── __main__.py           # Main entry point
├── data/                      # Data files
│   └── roll_numbers.txt      # Student roll numbers
├── topics/                    # Question bank directory
│   ├── semiconductor_physics.tex
│   ├── device_physics.tex
│   └── laser_optics.tex
├── output/                    # Generated output
│   ├── papers/               # Individual question papers
│   ├── answers/              # Individual answer keys
│   ├── all_question_papers.pdf
│   └── all_answer_keys.pdf
├── setup.py                  # Package installation
├── requirements.txt          # Development dependencies
├── README.md                # Project documentation
├── CONTRIBUTOR_GUIDE.md     # Detailed contributor guide
└── LICENSE                  # License information
```

## Configuration

All configuration settings are centralized in `pytexmcq/config/config.py`. This includes:
- Project paths
- Quiz settings (title, department, course code, etc.)
- Number of questions per topic
- Physical constants
- LaTeX compilation options

## Usage

1. Create your question bank in the `topics/` directory
2. Configure your quiz settings in `pytexmcq/config/config.py`
3. Set up student roll numbers in `data/roll_numbers.txt`
4. Generate quizzes:
```bash
python -m pytexmcq
```

## Development

For detailed information about the project's inner workings, contribution guidelines, and development practices, please refer to [CONTRIBUTOR_GUIDE.md](CONTRIBUTOR_GUIDE.md).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- LaTeX exam class for the quiz template
- PyPDF2 for PDF operations