"""
Configuration settings for PyTeXMCQ.
"""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
TOPICS_DIR = PROJECT_ROOT / "topics"
OUTPUT_DIR = PROJECT_ROOT / "papers"
ANSWERS_DIR = PROJECT_ROOT / "answers"
TEMPLATES_DIR = PROJECT_ROOT / "pytexmcq/templates"

# File paths
PREAMBLE_FILE = TEMPLATES_DIR / "preamble.tex"
ROLL_NUMBERS_FILE = PROJECT_ROOT / "roll_numbers.txt"

# Quiz settings
QUIZ_TITLE = "QUIZ 2"
DEPARTMENT = "Department of Physics"
COURSE_CODE = "PHL102, S Section"
INSTITUTE = "Visvesvaraya National Institute of Technology, Nagpur"
FULL_MARKS = 10
TIME_DURATION = "1 hr"

# Question selection configuration
QUESTIONS_PER_TOPIC = {
    "quantum_mechanics": 0,
    "quantum_applications": 0,
    "crystal_structure": 0,
    "semiconductor_physics": 10,
    "device_physics": 10,
    "laser_optics": 1
}

# Constants for quiz header
PHYSICAL_CONSTANTS = {
    "electron_charge": "1.602 \\times 10^{-19}",
    "electron_mass": "9.1 \\times 10^{-31}",
    "planck_constant": "6.6 \\times 10^{-34}",
    "boltzmann_constant": "1.38 \\times 10^{-23}"
}

# LaTeX settings
LATEX_COMPILE_OPTIONS = ["-interaction=nonstopmode"] 