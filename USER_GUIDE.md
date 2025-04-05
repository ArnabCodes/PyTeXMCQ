# LaTeX Quiz Generator User Guide

This guide provides detailed instructions on how to use the LaTeX Quiz Generator effectively.

## Table of Contents
1. [Setting Up Questions](#setting-up-questions)
2. [Question Format](#question-format)
3. [LaTeX Formatting](#latex-formatting)
4. [Configuration](#configuration)
5. [Generating Quizzes](#generating-quizzes)
6. [Troubleshooting](#troubleshooting)

## Setting Up Questions

### Directory Structure
Place your questions in `.tex` files within the `topics/` directory. You can organize questions by topic, difficulty, or any other classification:

```
topics/
├── chapter1.tex
├── chapter2.tex
└── advanced_topics.tex
```

### Question File Format
Each question file should contain one or more questions in the following format:

```latex
\question[0.5] What is the energy of a photon with wavelength 500 nm?
\begin{oneparcheckboxes}
    \choice 1.24 eV
    \CorrectChoice 2.48 eV
    \choice 3.1 eV
    \choice 4.96 eV
\end{oneparcheckboxes}

\question[0.5] The forbidden energy gap for silicon at room temperature is:
\begin{oneparcheckboxes}
    \choice 0.7 eV
    \CorrectChoice 1.1 eV
    \choice 1.5 eV
    \choice 2.1 eV
\end{oneparcheckboxes}
```

## Question Format

### Basic Structure
- Use `\question[points]` to start each question
- Points are specified in square brackets
- Use `\begin{oneparcheckboxes}` for multiple choice options
- Mark correct answers with `\CorrectChoice`
- Mark incorrect answers with `\choice`

### Including Mathematical Expressions
```latex
\question[1] Solve the equation: \( E = mc^2 \) for \( m \) when \( E = 10 \) J and \( c = 3 \times 10^8 \) m/s.
```

### Including Figures
```latex
\question[1] What does this circuit diagram represent?
\begin{center}
\includegraphics[width=0.5\textwidth]{figures/circuit.png}
\end{center}
```

## LaTeX Formatting

### Available Packages
The template includes several useful packages:
- `siunitx` for SI units
- `amsmath` for mathematical expressions
- `graphicx` for images
- `color` for colored text

### Using SI Units
```latex
\question[0.5] A current of \SI{2}{\ampere} flows through a \SI{5}{\ohm} resistor. What is the voltage?
```

### Mathematical Formatting
```latex
\question[1] Evaluate the integral:
\[ \int_0^{\pi} \sin(x) dx \]
```

## Configuration

### Roll Numbers
Add student roll numbers to `roll_numbers.txt`:
```
BT24ECE001
BT24ECE002
BT24ECE003
```

### Customizing Headers
Modify the header in `preamble.tex` to change:
- Title format
- Department name
- Course information
- Time duration
- Maximum marks

### Customizing Layout
Adjust in `preamble.tex`:
- Page margins
- Font size
- Spacing between questions
- Choice formatting

## Generating Quizzes

### Basic Generation
```bash
python generate_papers.py
```

### Merging PDFs
```bash
python merge_pdfs.py
```

### Output Files
- Individual question papers: `papers/quiz_ROLLNUMBER.pdf`
- Individual answer keys: `papers/quiz_ROLLNUMBER_answers.pdf`
- Combined papers: `all_question_papers.pdf`
- Combined answers: `all_answer_keys.pdf`

## Troubleshooting

### Common Issues

1. **LaTeX Compilation Errors**
   - Check for missing packages
   - Verify mathematical expressions are properly formatted
   - Ensure image paths are correct

2. **Python Errors**
   - Verify Python version (3.8+ required)
   - Check virtual environment is activated
   - Confirm all required packages are installed

3. **PDF Generation Issues**
   - Ensure LaTeX distribution is properly installed
   - Check write permissions in output directories
   - Verify no PDFs are open in other programs

### Getting Help
If you encounter issues:
1. Check the error messages in the terminal
2. Review the LaTeX log files
3. Open an issue on GitHub with:
   - Error messages
   - Relevant code snippets
   - System information 