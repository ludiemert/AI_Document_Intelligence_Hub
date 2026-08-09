# This file reads text from uploaded files.
# TXT files work now. PDF and image OCR will be added later.

# This imports Path from Python.
# We use Path to work with file paths.
from pathlib import Path


def get_file_extension(file_path):
    """Get the file extension from a file path."""
    # This converts the file path to a Path object.
    path = Path(file_path)

    # This gets the extension without the dot.
    file_extension = path.suffix.replace(".", "").lower()

    # This returns the file extension.
    return file_extension


def read_text_from_file(file_path):
    """Read text from TXT files or prepare OCR files."""
    # This gets the file extension.
    file_extension = get_file_extension(file_path)

    # This checks if the file is TXT.
    if file_extension == "txt":
        # This reads the TXT file as text.
        text = Path(file_path).read_text(encoding="utf-8")

        # This returns the extracted text.
        return {
            "success": True,
            "text": text,
            "message": "TXT file read successfully.",
        }

    # This checks if the file is PDF or image.
    if file_extension in ["pdf", "png", "jpg", "jpeg"]:
        # OCR is not ready yet.
        # The app knows this file needs OCR later.
        return {
            "success": False,
            "text": "",
            "message": "OCR is not implemented yet for this file type.",
        }

    # This returns an error for unknown file types.
    return {
        "success": False,
        "text": "",
        "message": "Unsupported file type.",
    }
