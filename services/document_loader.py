# This imports Path from Python.
# We use Path to work with folder paths.
from pathlib import Path

# This is the sample documents folder path.
# The app reads invoice text files from this folder.
SAMPLE_DOCUMENTS_FOLDER = Path("sample_documents")

# This creates the sample documents folder if it does not exist.
SAMPLE_DOCUMENTS_FOLDER.mkdir(exist_ok=True)


# This function reads invoice text files from the sample documents folder.
# It returns a list with invoice text and file path.
def load_invoice_texts():
    """Load invoice text files and source file paths."""
    # This list will save all invoice documents.
    invoice_documents = []

    # This loop finds all .txt files in this folder and subfolders.
    # rglob means recursive search.
    for file_path in SAMPLE_DOCUMENTS_FOLDER.rglob("*.txt"):
        invoice_text = file_path.read_text(encoding="utf-8")

        invoice_documents.append(
            {
                "text": invoice_text,
                "source_file": str(file_path),
            }
        )

    return invoice_documents
