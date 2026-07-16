"""
helpers.py

General helper functions used across FactoryBrain AI.
"""

import os
from datetime import datetime


# ==========================================
# File Helpers
# ==========================================

def get_file_extension(file_path):

    return os.path.splitext(file_path)[1].lower()


def get_filename(file_path):

    return os.path.basename(file_path)


def file_exists(file_path):

    return os.path.exists(file_path)


# ==========================================
# Text Helpers
# ==========================================

def truncate_text(text, max_length=100):

    if len(text) <= max_length:
        return text

    return text[:max_length] + "..."


def word_count(text):

    return len(text.split())


# ==========================================
# Date & Time Helpers
# ==========================================

def current_timestamp():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# ==========================================
# List Helpers
# ==========================================

def remove_duplicates(items):

    return list(set(items))


def flatten(nested_list):

    return [
        item
        for sublist in nested_list
        for item in sublist
    ]


# ==========================================
# Dictionary Helpers
# ==========================================

def merge_dicts(dict1, dict2):

    return {**dict1, **dict2}


# ==========================================
# Demo
# ==========================================

if __name__ == "__main__":

    print(get_file_extension("report.pdf"))
    print(get_filename("uploads/report.pdf"))

    print(
        truncate_text(
            "FactoryBrain AI is an industrial knowledge platform.",
            25
        )
    )

    print(word_count(
        "Pump A requires maintenance."
    ))

    print(current_timestamp())

    print(
        remove_duplicates(
            ["A", "B", "A", "C"]
        )
    )
