# PyTeXMCQ Contributor Guide

This guide provides detailed information about the project's architecture, development practices, and contribution guidelines.

## Project Architecture

### Core Components

1. **Configuration Management** (`pytexmcq/config/config.py`)
   - Centralizes all configurable parameters
   - Defines project paths and directory structure
   - Sets quiz parameters (title, department, course code)
   - Configures question selection per topic
   - Manages LaTeX compilation settings

2. **Quiz Generation** (`pytexmcq/core/generator.py`)
   - `QuizGenerator` class: Main class for generating quizzes
   - Methods:
     - `load_questions()`: Loads and parses question files
     - `_get_seed()`: Generates consistent random seeds
     - `_randomize_options()`: Shuffles MCQ options
     - `generate_paper()`: Creates individual quiz papers
     - `_select_questions()`: Implements question selection logic

3. **PDF Operations** (`pytexmcq/utils/pdf_utils.py`)
   - Handles PDF merging and manipulation
   - Uses PyPDF2 for PDF operations
   - Provides utility functions for file management

4. **LaTeX Templates** (`pytexmcq/templates/`)
   - `preamble.tex`: Defines document structure and formatting
   - Supports mathematical equations and scientific notation
   - Configurable through the exam document class

### Data Flow

1. **Question Loading**
   - Questions are loaded from `.tex` files in the `topics/` directory
   - Each question file contains multiple questions with options
   - Questions are parsed and stored in memory for processing

2. **Randomization Process**
   - Each roll number generates a unique seed using MD5 hashing
   - Questions are selected randomly from each topic
   - Multiple-choice options are shuffled while preserving correct answers
   - Question order is randomized for each student

3. **Paper Generation**
   - LaTeX files are generated for each student
   - Files are compiled using pdflatex
   - Answer keys are generated simultaneously
   - PDFs are merged into consolidated files

## Development Practices

### Code Style
- Follow PEP 8 guidelines
- Use type hints for better code clarity
- Document all public functions and classes
- Keep functions focused and single-purpose

### Testing
- Write unit tests for core functionality
- Test randomization consistency
- Verify LaTeX compilation
- Check PDF generation and merging

### Documentation
- Keep docstrings up to date
- Document configuration options
- Maintain clear examples
- Update guides when adding features

## Contribution Guidelines

1. **Setting Up Development Environment**
   ```bash
   git clone https://github.com/ArnabCodes/PyTeXMCQ.git
   cd PyTeXMCQ
   pip install -e ".[dev]"
   ```

2. **Making Changes**
   - Create a new branch for each feature
   - Follow the existing code structure
   - Add tests for new functionality
   - Update documentation as needed

3. **Submitting Changes**
   - Write clear commit messages
   - Include tests with new features
   - Update relevant documentation
   - Submit pull requests with detailed descriptions

## Project Structure Best Practices

The project follows a professional Python package structure:

```
pytexmcq/
├── core/          # Core business logic
├── config/        # Configuration management
├── templates/     # LaTeX templates
└── utils/         # Utility functions
```

This structure:
- Separates concerns logically
- Makes the codebase maintainable
- Follows Python packaging standards
- Facilitates testing and documentation

## Configuration Management

The project uses a centralized configuration approach:

1. **Path Configuration**
   - All paths are defined relative to the project root
   - Uses `pathlib` for cross-platform compatibility
   - Ensures consistent file organization

2. **Quiz Settings**
   - Title, department, and course information
   - Time duration and marks
   - Question distribution per topic

3. **LaTeX Settings**
   - Compilation options
   - Physical constants
   - Document formatting

## Error Handling

The project implements robust error handling:

1. **File Operations**
   - Checks for file existence
   - Validates file formats
   - Handles permission errors

2. **LaTeX Compilation**
   - Catches compilation errors
   - Provides meaningful error messages
   - Cleans up temporary files

3. **PDF Operations**
   - Validates PDF files
   - Handles merge errors
   - Ensures file integrity

## Performance Considerations

1. **Memory Management**
   - Questions are loaded once and reused
   - Large files are processed in chunks
   - Temporary files are cleaned up

2. **Randomization Efficiency**
   - Uses efficient random number generation
   - Implements consistent seeding
   - Minimizes redundant operations

3. **PDF Processing**
   - Merges files efficiently
   - Handles large PDFs appropriately
   - Manages system resources

## Future Improvements

Potential areas for enhancement:

1. **Features**
   - Web interface for configuration
   - Question bank management
   - Template customization
   - Export to different formats

2. **Technical**
   - Parallel processing for large batches
   - Caching for repeated operations
   - Enhanced error recovery
   - More comprehensive testing

3. **Documentation**
   - API documentation
   - More examples
   - Tutorial videos
   - User case studies 