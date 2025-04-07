"""
Utility functions for PDF operations.
"""

import os
from pathlib import Path
from PyPDF2 import PdfMerger

def merge_pdfs(source_dir: Path, output_file: str, prefix: str = '') -> None:
    """
    Merge multiple PDF files into a single PDF.
    
    Args:
        source_dir: Directory containing PDF files to merge
        output_file: Name of the output merged PDF file
        prefix: Optional prefix to filter PDF files
    """
    merger = PdfMerger()
    
    # Get all PDF files that match the prefix
    pdf_files = sorted([
        f for f in os.listdir(source_dir)
        if f.endswith('.pdf') and f.startswith(prefix)
    ])
    
    # Add each PDF to the merger
    for pdf_file in pdf_files:
        file_path = source_dir / pdf_file
        merger.append(str(file_path))
    
    # Write the merged PDF
    if pdf_files:
        with open(output_file, 'wb') as f:
            merger.write(f)
    
    merger.close() 