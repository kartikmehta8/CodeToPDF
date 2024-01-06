import os
import sys
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <folder_path> <output_pdf>")
        sys.exit(1)

    folder_path = sys.argv[1]
    output_pdf = sys.argv[2]
    unallowed_files = ['file1.txt', 'file2.txt']  # Add your unallowed file names here
    unallowed_folders = ['folder1', 'folder2']  # Add your unallowed folder names here

    process_folder(folder_path, output_pdf, unallowed_files, unallowed_folders)