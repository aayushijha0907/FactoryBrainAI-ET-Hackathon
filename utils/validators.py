"""
validators.py

Validation utilities for FactoryBrain AI.
"""

import os


class Validator:

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".txt",
        ".png",
        ".jpg",
        ".jpeg"
    }

    MAX_FILE_SIZE_MB = 25

    # ======================================
    # Validate File Exists
    # ======================================

    @staticmethod
    def file_exists(file_path):

        return os.path.exists(file_path)

    # ======================================
    # Validate Extension
    # ======================================

    @staticmethod
    def validate_extension(file_path):

        extension = os.path.splitext(
            file_path
        )[1].lower()

        return extension in Validator.ALLOWED_EXTENSIONS

    # ======================================
    # Validate File Size
    # ======================================

    @staticmethod
    def validate_size(file_path):

        size_mb = (
            os.path.getsize(file_path)
            / (1024 * 1024)
        )

        return size_mb <= Validator.MAX_FILE_SIZE_MB

    # ======================================
    # Validate Empty Text
    # ======================================

    @staticmethod
    def validate_text(text):

        return bool(text and text.strip())

    # ======================================
    # Complete Validation
    # ======================================

    @staticmethod
    def validate_document(file_path):

        if not Validator.file_exists(
            file_path
        ):
            return False, "File not found."

        if not Validator.validate_extension(
            file_path
        ):
            return False, "Unsupported file type."

        if not Validator.validate_size(
            file_path
        ):
            return False, "File exceeds size limit."

        return True, "Validation successful."


# ======================================
# Demo
# ======================================

if __name__ == "__main__":

    sample = "uploads/sample.pdf"

    status, message = (
        Validator.validate_document(
            sample
        )
    )

    print(status)
    print(message)
