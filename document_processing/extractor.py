"""
extractor.py
Main document processing pipeline for FactoryBrain AI.
Orchestrates parsing, OCR (if needed), metadata extraction, and chunking.
"""

import os
from typing import Dict, Any

# Import internal modules
from document_processing.pdf_parser import parse_document, clean_text
from document_processing.ocr import OCRProcessor
from document_processing.metadata import MetadataExtractor
from document_processing.chunking import chunk_document


class DocumentExtractor:
    """
    Main pipeline for processing industrial documents.
    Handles text extraction, OCR fallback, metadata, and chunking.
    """
    
    def __init__(self):
        self.ocr = OCRProcessor()
        self.metadata_extractor = MetadataExtractor()

    def _needs_ocr(self, text: str, min_length: int = 100) -> bool:
        """Determine if OCR is needed based on extracted text quality."""
        return len(text.strip()) < min_length

    def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Process a single document through the complete pipeline.
        
        Returns:
            dict: Processed document with metadata, text, and chunks.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document not found: {file_path}")

        used_ocr = False

        # Step 1: Initial Parsing (PyMuPDF for PDFs, simple read for TXT)
        document = parse_document(file_path)

        # Step 2: OCR Fallback for Scanned PDFs
        if file_path.lower().endswith(".pdf"):
            if self._needs_ocr(document["text"]):
                print(f"🔍 Applying OCR to scanned document: {os.path.basename(file_path)}")
                document["text"] = self.ocr.extract(file_path)
                used_ocr = True

        # Step 3: Clean extracted text
        document["text"] = clean_text(document["text"])

        # Step 4: Extract Metadata
        metadata = self.metadata_extractor.extract(file_path, document["text"])

        # Step 5: Chunk the document
        chunked = chunk_document(document)

        # Final Processed Document
        return {
            "status": "success",
            "filename": metadata["filename"],
            "file_path": file_path,
            "metadata": metadata,
            "full_text": document["text"],
            "chunks": chunked["chunks"],
            "num_chunks": chunked["num_chunks"],
            "used_ocr": used_ocr,
            "processed_at": metadata.get("processed_at"),
        }

    def process_multiple(self, file_paths: list) -> list:
        """Process multiple documents and return results."""
        results = []
        for path in file_paths:
            try:
                result = self.process_document(path)
                results.append(result)
            except Exception as e:
                results.append({
                    "status": "error",
                    "filename": os.path.basename(path),
                    "error": str(e)
                })
        return results


# ====================================================
# Demo / Testing
# ====================================================
if __name__ == "__main__":
    extractor = DocumentExtractor()
    sample = "uploads/sample.pdf"
    
    if os.path.exists(sample):
        print(f"Processing: {sample}\n")
        
        result = extractor.process_document(sample)
        
        print("=" * 70)
        print("✅ Document Processing Complete")
        print("=" * 70)
        print(f"Filename     : {result['filename']}")
        print(f"OCR Used     : {result['used_ocr']}")
        print(f"Pages        : {result['metadata'].get('pages', 'N/A')}")
        print(f"Chunks       : {result['num_chunks']}")
        print(f"Word Count   : {result['metadata'].get('word_count', 0):,}")
        print(f"Processed At : {result['processed_at']}")
        print("=" * 70)
    else:
        print("⚠️ Sample file not found. Please place a test document in 'uploads/sample.pdf'")
