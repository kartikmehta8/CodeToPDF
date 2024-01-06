# Folder to PDF Converter Script

## Introduction
This Python script is designed to recursively traverse through a specified folder, compile the contents of text files into a single PDF, and skip over specified unallowed files and folders. It's particularly useful for aggregating text data from multiple files into a single document.

## Dependencies
To run this script, you need Python installed on your system along with the following libraries:
- `PyPDF2`: Used for creating and manipulating PDF files.
- `reportlab`: Used for generating PDF documents with text content.

You can install these dependencies using pip:
```bash
pip install PyPDF2 reportlab
```

## Script Walkthrough

### Importing Libraries

```python
import os
import sys
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
```

-   `os` and `sys` are standard Python libraries used for file and system operations.
-   `PyPDF2` is used for PDF manipulation.
-   `io` provides core tools for working with streams.
-   `reportlab` is used for creating PDF documents.

### Function: `add_text_to_pdf`

```python
def add_text_to_pdf(text, pdf_writer):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    for i, line in enumerate(text.split('\n')):
        can.drawString(72, 800 - 15 * i, line)
    can.save()

    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    page = new_pdf.getPage(0)
    pdf_writer.addPage(page)
```
This function creates a PDF page with the provided text. It uses `reportlab` to draw text onto a canvas, which is then converted into a PDF page and added to the `PdfFileWriter` object.

### Function: `process_folder`

```python
def process_folder(folder_path, output_pdf, unallowed_files, unallowed_folders):
    pdf_writer = PdfFileWriter()

    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in unallowed_folders]

        for file in files:
            if file in unallowed_files:
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as f:
                    add_text_to_pdf(f.read(), pdf_writer)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    with open(output_pdf, 'wb') as out:
        pdf_writer.write(out)
```

This function traverses the directory tree starting from `folder_path`. It skips over unallowed folders and files, reads the content of allowed files, and uses `add_text_to_pdf` to add this content to the PDF.

### Main Script

```python
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <folder_path> <output_pdf>")
        sys.exit(1)

    folder_path = sys.argv[1]
    output_pdf = sys.argv[2]
    unallowed_files = ['file1.txt', 'file2.txt']
    unallowed_folders = ['folder1', 'folder2']

    process_folder(folder_path, output_pdf, unallowed_files, unallowed_folders) 
```

This part of the script checks for the correct usage, takes command-line arguments for the folder path and output PDF file name, and calls `process_folder` with these parameters along with the lists of unallowed files and folders.

## Usage

Run the script from the command line, providing the path to the folder and the output PDF file name:

```bash
python script.py /path/to/folder output.pdf 
```
## Use Cases

-   **Document Aggregation**: Combining multiple text documents into a single PDF for reporting or archival purposes.
-   **Data Compilation**: Gathering text data from various files for data analysis or research.

## Conclusion

This script is a versatile tool for anyone looking to consolidate text information from multiple files into a single PDF document. Its ability to exclude specific files and folders adds to its flexibility, making it suitable for a variety of use cases in both professional and personal settings.

Remember to adjust the script for different file types and formatting needs, as it currently handles basic text files.