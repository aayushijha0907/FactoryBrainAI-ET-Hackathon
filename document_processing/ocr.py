"""
ocr.py
High-quality OCR text extraction for scanned PDFs and images using Tesseract + PyMuPDF.
"""

import os
import tempfile
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from typing import Optional, Dict, Any


class OCRProcessor:
    """
    OCR Processor for scanned documents and images.
    Optimized for industrial documents (manuals, reports, drawings).
    """
    
    def __init__(self, tesseract_cmd: Optional[str] = None, lang: str = "eng"):
        """
        Initialize OCR Processor.
        
        Args:
            tesseract_cmd: Path to tesseract executable (required on Windows)
            lang: Language code (default: English)
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        
        self.lang = lang
        self.custom_config = r'--oem 3 --psm 6'  # Good for documents

    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from a single image."""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(
                image, 
                lang=self.lang, 
                config=self.custom_config
            )
            return text.strip()
        except Exception as e:
            raise Exception(f"Image OCR failed for {image_path}: {e}")

    def extract_text_from_pdf(self, pdf_path: str, dpi: int = 300) -> str:
        """
        Extract text from scanned PDF using high-quality rendering + OCR.
        """
        try:
            document = fitz.open(pdf_path)
            extracted_text = []
            
            for page_number in range(len(document)):
                page = document.load_page(page_number)
                
                # Render page as image at high DPI
                pix = page.get_pixmap(dpi=dpi, colorspace=fitz.csRGB)
                
                # Use temporary file in system temp directory
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                    temp_path = tmp.name
                    pix.save(temp_path)
                
                try:
                    page_text = pytesseract.image_to_string(
                        temp_path,
                        lang=self.lang,
                        config=self.custom_config
                    )
                    
                    extracted_text.append(
                        f"\n\n----- Page {page_number + 1} -----\n{page_text.strip()}"
                    )
                finally:
                    # Clean up temp file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
            
            document.close()
            return "\n".join(extracted_text).strip()
            
        except Exception as e:
            raise Exception(f"PDF OCR failed for {pdf_path}: {e}")

    def extract(self, file_path: str) -> str:
        """
        Main method: Detect file type and extract text using OCR.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return self.extract_text_from_pdf(file_path)
        elif extension in [".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"]:
            return self.extract_text_from_image(file_path)
        else:
            raise ValueError(
                f"Unsupported file type: {extension}. "
                f"Supported: PDF, PNG, JPG, JPEG, BMP, TIFF"
            )

    def get_supported_formats(self) -> list:
        return [".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".tiff"]


# =====================================================
# Demo / Testing
# =====================================================
if __name__ == "__main__":
    processor = OCRProcessor()
    
    sample_file = "uploads/sample_scanned.pdf"
    
    if os.path.exists(sample_file):
        print("🔍 Running OCR on:", sample_file)
        try:
            text = processor.extract(sample_file)
            print("\n" + "="*80)
            print(text[:1500])  # Show first 1500 characters
            print("="*80)
            print(f"\nTotal characters extracted: {len(text)}")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("⚠️  Sample file not found.")
        print("Please place a scanned PDF in 'uploads/sample_scanned.pdf'")
