import os
from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(input_dir, output_file, prefix):
    # Get all PDF files in the directory
    pdf_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.pdf') and f.startswith(prefix)])
    
    # Create a PDF writer object
    writer = PdfWriter()
    
    # Process each PDF file
    for pdf_file in pdf_files:
        # Read the PDF
        reader = PdfReader(os.path.join(input_dir, pdf_file))
        
        # Add all pages from the current PDF
        for page in reader.pages:
            writer.add_page(page)
        
        # Check if the number of pages is odd
        if len(reader.pages) % 2 != 0:
            # Add a blank page
            writer.add_blank_page()
    
    # Write the merged PDF to the output file
    with open(output_file, 'wb') as output:
        writer.write(output)

# Merge question papers
merge_pdfs('papers', 'all_question_papers.pdf', 'quiz_')

# Merge answer keys
merge_pdfs('answers', 'all_answer_keys.pdf', 'quiz_') 