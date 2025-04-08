# PyTeXMCQ

<div align="center">
  <img src="PyTeXMCQ_logo.svg" alt="PyTeXMCQ Logo" width="200" height="200"/>
</div>

A Python-based tool for generating randomized multiple-choice quiz papers and answer keys in LaTeX format. Perfect for educators who need to create different versions of the same quiz for multiple students while maintaining consistency and professional formatting.

## Features

- 🔑 Generates unique quiz versions for each student using roll numbers as seeds
- 📑 Automatically creates answer keys
- 📐 Maintains consistent formatting across all versions
- 📚 Combines all quizzes and answer keys into consolidated PDFs
- ⚙️ Supports custom LaTeX preamble for advanced formatting
- ⚡ Compiles documents in parallel for better performance
- 📄 Adds blank pages when needed for easier printing
- 📊 Automatically calculates and displays total marks

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
└── topics/              # Directory for question banks
```

## Usage

1. Create your question bank:
   - Place your questions in `.tex` files in the `topics/` directory
   - Follow the template format:
     ```latex
     \begin{question}[2]  % Points for this question
     Which experiment provided direct evidence for the particle nature of light?

     \begin{oneparcheckboxes}
     \choice Young's double-slit experiment
     \choice Michelson-Morley experiment
     \correctchoice Compton effect
     \choice Davisson-Germer experiment
     \end{oneparcheckboxes}
     \end{question}
     ```
   - If no points are specified, the question is worth 1 mark
   - For consistent total marks across papers, group questions with same marks in the same file

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

## Important Notes

- Roll numbers act as seeds for randomization, ensuring the same roll number always gets the same paper
- Questions are compiled in parallel for better performance
- Total marks are automatically calculated and displayed
- Blank pages are added when needed for easier double-sided printing
- For consistent total marks, group questions with same marks in the same file

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

## Technical Architecture

The codebase is built around two main classes that handle different aspects of the quiz generation process:

### 1. ProgressIndicator Class
This class provides a visual progress indicator during the quiz generation process. It features:
- An animated spinner with percentage completion
- Thread-safe operation
- Customizable messages
- Success/failure status indicators

### 2. QuestionPaperGenerator Class
This is the core class that handles the quiz generation process. It consists of several key components:

#### Question Management
- **Question Loading**: Loads questions from `.tex` files in the topics directory
- **Question Parsing**: Splits questions into individual components and extracts marks
- **Question Randomization**: Uses roll numbers as seeds to ensure consistent randomization

#### Paper Generation
- **Seed Generation**: Converts roll numbers into consistent integer seeds using MD5 hashing
- **Option Randomization**: Randomizes multiple-choice options while preserving correct answers
- **Paper Assembly**: Combines questions, formatting, and student information
- **Answer Key Generation**: Creates parallel answer keys with correct choices marked

#### LaTeX Processing
- **Temporary Directory Management**: Creates isolated workspaces for each compilation
- **Parallel Compilation**: Uses multiprocessing to compile multiple papers simultaneously
- **Error Handling**: Provides detailed error messages for LaTeX compilation issues
- **PDF Merging**: Combines individual papers into consolidated PDFs

#### Configuration Handling
The system uses a JSON configuration file (`config.json`) that defines:
- Number of questions per topic
- Roll number patterns
- Topic-specific settings

### Workflow
1. The system reads questions from topic-specific `.tex` files
2. For each roll number:
   - Generates a unique seed based on the roll number
   - Randomizes question order and options
   - Creates both question paper and answer key
   - Compiles LaTeX files to PDF
3. Combines all papers and answer keys into consolidated PDFs
4. Cleans up temporary files

### Key Technical Features
- **Deterministic Randomization**: Same roll number always gets the same paper
- **Parallel Processing**: Uses Python's multiprocessing for faster compilation
- **Memory Management**: Uses temporary directories to prevent file system clutter
- **Error Resilience**: Comprehensive error handling and reporting
- **Modular Design**: Easy to extend with new question types or features

## System Flowchart

The following flowchart illustrates the system's core components and their interactions:

```mermaid
flowchart TB
    subgraph Input["Input Processing"]
        direction TB
        D1[Parse Topic Files]
        D2[Extract & Validate]
        D3[Build Question Bank]
        D1 --> D2 --> D3
    end
    
    subgraph Generation["Paper Generation"]
        direction TB
        E1[Create Unique Seeds]
        E2[Select Questions]
        E3[Randomize Content]
        E1 --> E2 --> E3
    end
    
    subgraph Compilation["Document Processing"]
        direction TB
        F1[Generate LaTeX]
        F2[Create Answer Keys]
        F3[Compile Documents]
        F1 --> F2 --> F3
    end
    
    subgraph Parallel["Parallel Processing"]
        direction TB
        G1[Worker Pool]
        G2[Process Tasks]
        G3[Merge Results]
        G1 --> G2 --> G3
    end
    
    A([Start]) --> B[Load Configuration]
    B --> C[Initialize System]
    C --> Input
    Input --> Generation
    Generation --> Compilation
    Compilation --> Parallel
    Parallel --> H[Cleanup & Finalize]
    H --> I([End])
    
    style A fill:#4a5568,stroke:#2d3748,stroke-width:2px,color:white
    style I fill:#4a5568,stroke:#2d3748,stroke-width:2px,color:white
    style Input fill:#f7fafc,stroke:#cbd5e0,stroke-width:2px,color:#2d3748
    style Generation fill:#f0fff4,stroke:#c6f6d5,stroke-width:2px,color:#2d3748
    style Compilation fill:#fff5f5,stroke:#fed7d7,stroke-width:2px,color:#2d3748
    style Parallel fill:#ebf8ff,stroke:#bee3f8,stroke-width:2px,color:#2d3748
```

### Component Descriptions

1. **📥 Input Processing**
   - Loads and validates configuration
   - Parses question files
   - Builds structured question bank
   - Validates content integrity

2. **⚙️ Paper Generation**
   - Generates deterministic seeds
   - Implements smart question selection
   - Applies randomization algorithms
   - Ensures fair distribution

3. **📄 Document Processing**
   - Creates LaTeX templates
   - Generates answer keys
   - Handles document compilation
   - Manages formatting

4. **⚡ Parallel Processing**
   - Optimizes resource usage
   - Manages concurrent tasks
   - Ensures data consistency
   - Handles error recovery

5. **🔄 System Flow**
   - Input → Generation → Compilation → Output
   - Maintains data integrity
   - Provides progress tracking
   - Ensures clean cleanup

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 