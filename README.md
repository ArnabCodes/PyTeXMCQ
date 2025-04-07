# PyTeXMCQ

A Python-based tool for generating randomized multiple-choice quiz papers and answer keys in LaTeX format. Perfect for educators who need to create different versions of the same quiz for multiple students while maintaining consistency and professional formatting.

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
- `pdflatex` command-line tool

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/ArnabCodes/PyTeXMCQ.git
   cd PyTeXMCQ
   ```

2. Create and activate a virtual environment (optional):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Verify LaTeX installation:
   ```bash
   pdflatex --version
   ```

## Project Structure

```
PyTeXMCQ/
├── generate_papers.py     # Main script for generating quizzes
├── preamble.tex          # LaTeX preamble with formatting
├── config.json           # Configuration file
├── papers/              # Directory for question papers
├── answers/             # Directory for answer keys
└── topics/             # Directory for question banks
```

## Usage

1. Create your question bank:
   - Place your questions in `.tex` files in the `topics/` directory
   - Follow the template format:
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

2. Configure the generator:
   - Edit `config.json` to specify:
     - Number of questions per topic
     - Roll number patterns (e.g., "BT24ECE01...04")

3. Generate quizzes:
   ```bash
   python generate_papers.py
   ```

4. Find your output:
   - `papers.pdf`: All question papers merged
   - `answers.pdf`: All answer keys merged

## Configuration

### config.json
```json
{
    "questions_per_topic": {
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

### preamble.tex
Customize your quiz appearance by modifying:
- Page layout
- Font settings
- Header/footer content
- Question formatting

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Areas for Contribution
- Add support for different question types
- Implement question difficulty levels
- Add support for images and diagrams
- Create a GUI interface
- Improve error handling
- Add unit tests

## License

This project is licensed under the MIT License - see the LICENSE file for details. 