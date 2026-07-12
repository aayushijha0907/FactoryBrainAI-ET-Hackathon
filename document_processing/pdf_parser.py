"""
pdf_parser.py
Handles document parsing and text extraction for FactoryBrain AI.

Supported formats:
- PDF (.pdf) - using PyMuPDF (fitz)
- Text (.txt)

Future support: DOCX, images (OCR), etc.
"""

import fitz  # PyMuPDF
import os
from pathlib import Path
from typing import Dict, Any


def extract_pdf_text(pdf_path: str) -> Dict[str, Any]:
    """
    Extract text from a PDF file using PyMuPDF.
    
    Args:
        pdf_path (str): Path to the PDF file.
    
    Returns:
        dict: {
            "filename": str,
            "pages": int,
            "text": str,
            "success": bool
        }
    """
    try:
        document = fitz.open(pdf_path)
        
        extracted_text = []
        for page_num, page in enumerate(document):
            page_text = page.get_text("text")  # More reliable extraction
            if page_text.strip():
                extracted_text.append(page_text)
        
        document.close()

        full_text = "\n".join(extracted_text)

        return {
            "filename": os.path.basename(pdf_path),
            "pages": len(document),
            "text": full_text.strip(),
            "success": True
        }
        
    except Exception as e:
        raise Exception(f"PDF Parsing Error for {os.path.basename(pdf_path)}: {e}")


def extract_txt_text(txt_path: str) -> Dict[str, Any]:
    """
    Extract text from a plain text file.
    """
    try:
        with open(txt_path, "r", encoding="utf-8", errors="replace") as file:
            text = file.read()
        
        return {
            "filename": os.path.basename(txt_path),
            "pages": 1,
            "text": text.strip(),
            "success": True
        }
    except Exception as e:
        raise Exception(f"TXT Parsing Error for {os.path.basename(txt_path)}: {e}")


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing excessive whitespace and empty lines.
    """
    if not text:
        return ""
    
    lines = text.splitlines()
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if line:  # Remove empty lines
            cleaned_lines.append(line)
    
    return "\n".join(cleaned_lines)


def parse_document(file_path: str) -> Dict[str, Any]:
    """
    Main function to parse a document based on its file extension.
    
    Args:
        file_path (str): Path to the document.
    
    Returns:
        dict: Parsed document data.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_path = str(Path(file_path).resolve())
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        document = extract_pdf_text(file_path)
    elif extension == ".txt":
        document = extract_txt_text(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}. "
                        f"Supported formats: .pdf, .txt")

    # Clean the extracted text
    document["text"] = clean_text(document["text"])
    
    return document


# ==========================
# Testing / CLI Usage
# ==========================
if __name__ == "__main__":
    sample_file = "uploads/sample.pdf"
    
    if os.path.exists(sample_file):
        try:
            document = parse_document(sample_file)
            
            print("✅ Parsing Successful!")
            print(f"Filename     : {document['filename']}")
            print(f"Pages        : {document['pages']}")
            print(f"Characters   : {len(document['text']):,}")
            print(f"Preview      : {document['text'][:300]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("⚠️  Sample file not found. Please place a test PDF in 'uploads/sample.pdf'")