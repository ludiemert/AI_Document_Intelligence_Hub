# This file reads text from uploaded files.
# TXT files work now. Image OCR works with Tesseract.

# This imports Path from Python.
# We use Path to work with file paths.
from pathlib import Path

# This imports Image from Pillow.
# Pillow opens image files.
from PIL import Image

# This imports pytesseract.
# pytesseract connects Python to Tesseract OCR.
import pytesseract

# This imports the OCR text cleaner.
# It fixes small OCR mistakes before extraction.
from services.text_cleaner import clean_ocr_text

# This tells Python where Tesseract is installed on Windows.
# Change this path only if Tesseract is installed in another folder.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def get_file_extension(file_path):
    """Get the file extension from a file path."""
    # This converts the file path to a Path object.
    path = Path(file_path)

    # This gets the extension without the dot.
    file_extension = path.suffix.replace(".", "").lower()

    # This returns the file extension.
    return file_extension


def read_text_from_image(file_path):
    """Read text from an image using OCR."""
    # This opens the image file.
    image = Image.open(file_path)

    # This uses Tesseract OCR to read text from the image.
    raw_text = pytesseract.image_to_string(image)

    # This cleans small OCR mistakes.
    cleaned_text = clean_ocr_text(raw_text)

    # This returns the cleaned OCR text.
    return cleaned_text


def read_text_from_file(file_path):
    """Read text from TXT files or image files."""
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

    # This checks if the file is an image.
    if file_extension in ["png", "jpg", "jpeg"]:
        # This reads text from the image using OCR.
        text = read_text_from_image(file_path)

        # This returns the OCR text.
        return {
            "success": True,
            "text": text,
            "message": "Image OCR completed successfully.",
        }

    # This checks if the file is PDF.
    if file_extension == "pdf":
        # PDF OCR will be added later.
        return {
            "success": False,
            "text": "",
            "message": "PDF OCR is not implemented yet.",
        }

    # This returns an error for unknown file types.
    return {
        "success": False,
        "text": "",
        "message": "Unsupported file type.",
    }


# This runs only when we test this file directly.
# It does not run when Flask imports this file.
if __name__ == "__main__":
    # This is a test image path.
    # Change this path to an image inside uploads/pending_ocr.
    test_file_path = "uploads/pending_ocr/invoice_013.jpg"

    # This reads text from the test file.
    result = read_text_from_file(test_file_path)

    # This prints if OCR worked or not.
    print("OCR RESULT")
    print("----------")
    print(f"success: {result['success']}")
    print(f"message: {result['message']}")
    print()
    print("TEXT")
    print("----")
    print(result["text"])
