"""
chunking.py
Handles intelligent text chunking for FactoryBrain AI.

Optimized for industrial documents (manuals, SOPs, reports, drawings).
Uses LangChain's RecursiveCharacterTextSplitter with industry-tuned settings.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import Dict, List, Any
import uuid

# ==========================
# Optimized Chunk Configuration
# ==========================
DEFAULT_CHUNK_SIZE = 1200      # Slightly larger for technical content
DEFAULT_CHUNK_OVERLAP = 250    # Good balance for context preservation

# Industrial document separators (prioritizes logical breaks)
INDUSTRIAL_SEPARATORS = [
    "\n\n\n",      # Paragraph breaks
    "\n\n",        # Section breaks
    "\n# ",        # Markdown-style headers
    "\n## ",
    "\n### ",
    ". ",          # Sentences
    ";\n",         # Technical lists
    "\n",
    " ",
    ""
]


def create_text_splitter(
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    separators: List[str] = None
) -> RecursiveCharacterTextSplitter:
    """
    Create a configured text splitter optimized for industrial documents.
    """
    if separators is None:
        separators = INDUSTRIAL_SEPARATORS

    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
        length_function=len,
        is_separator_regex=False,
        add_start_index=True,          # Helpful for traceability
    )


def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
) -> List[Dict[str, Any]]:
    """
    Split text into chunks with rich metadata.
    
    Returns:
        List of dictionaries, each containing chunk text and metadata.
    """
    if not text or not text.strip():
        return []

    splitter = create_text_splitter(chunk_size, chunk_overlap)
    
    # Split into raw text chunks
    raw_chunks = splitter.split_text(text)

    # Enrich chunks with metadata
    enriched_chunks = []
    for i, chunk in enumerate(raw_chunks):
        enriched_chunks.append({
            "chunk_id": str(uuid.uuid4()),
            "chunk_index": i,
            "text": chunk.strip(),
            "length": len(chunk),
            "metadata": {
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
            }
        })

    return enriched_chunks


def chunk_document(
    document: Dict[str, Any],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP
) -> Dict[str, Any]:
    """
    Chunk a parsed document and return enriched result.
    """
    chunks = chunk_text(document["text"], chunk_size, chunk_overlap)

    return {
        "filename": document["filename"],
        "pages": document.get("pages", 1),
        "total_chunks": len(chunks),
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "chunks": chunks
    }


# ==========================
# Testing
# ==========================
if __name__ == "__main__":
    sample_text = """
    FactoryBrain AI is an advanced industrial knowledge intelligence platform.
    It enables engineers and technicians to upload maintenance manuals,
    inspection reports, Standard Operating Procedures (SOPs), and safety documents.
    
    The system uses Retrieval-Augmented Generation (RAG) to provide accurate,
    context-aware answers with source citations.
    
    Key benefits include reduced downtime, improved compliance, and faster troubleshooting.
    """

    document = {
        "filename": "maintenance_manual_v2.pdf",
        "pages": 42,
        "text": sample_text
    }

    result = chunk_document(document, chunk_size=800, chunk_overlap=150)

    print("✅ Chunking Complete!")
    print(f"Filename      : {result['filename']}")
    print(f"Pages         : {result['pages']}")
    print(f"Total Chunks  : {result['total_chunks']}")
    print(f"Chunk Size    : {result['chunk_size']} | Overlap: {result['chunk_overlap']}\n")

    # Preview first 2 chunks
    for i, chunk in enumerate(result["chunks"][:2], start=1):
        print(f"Chunk {i} (ID: {chunk['chunk_id'][:8]}...) - {chunk['length']} chars")
        print("-" * 60)
        print(chunk["text"][:280] + "..." if len(chunk["text"]) > 280 else chunk["text"])
        print()