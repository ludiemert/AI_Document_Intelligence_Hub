# This file cleans text extracted by OCR.
# OCR text can have small mistakes.

# This imports re from Python.
# We use re to find text patterns.
import re


def fix_short_dates(text):
    """Fix dates like 2026-2-26 to 2026-02-26."""
    # This pattern finds dates with 1 or 2 digits for month and day.
    date_pattern = r"(\d{4})-(\d{1,2})-(\d{1,2})"

    # This function formats one date match.
    def format_date(match):
        # This gets the year from the match.
        year = match.group(1)

        # This gets the month and adds zero if needed.
        month = match.group(2).zfill(2)

        # This gets the day and adds zero if needed.
        day = match.group(3).zfill(2)

        # This returns the fixed date.
        return f"{year}-{month}-{day}"

    # This replaces short dates with fixed dates.
    return re.sub(date_pattern, format_date, text)


def fix_vat_number(text):
    """Fix common OCR mistakes in VAT numbers."""
    # This replaces VAT Number: 1E with VAT Number: IE.
    text = re.sub(r"VAT Number:\s*1E", "VAT Number: IE", text)

    # This returns the cleaned text.
    return text


def clean_extra_spaces(text):
    """Clean extra spaces and empty lines."""
    # This splits the text into lines.
    lines = text.splitlines()

    # This removes extra spaces from each line.
    cleaned_lines = [line.strip() for line in lines]

    # This removes empty lines.
    cleaned_lines = [line for line in cleaned_lines if line]

    # This joins lines again.
    return "\n".join(cleaned_lines)


def clean_ocr_text(text):
    """Clean OCR text before extracting invoice fields."""
    # This fixes short date formats.
    text = fix_short_dates(text)

    # This fixes common VAT OCR mistakes.
    text = fix_vat_number(text)

    # This cleans spaces and empty lines.
    text = clean_extra_spaces(text)

    # This returns the cleaned OCR text.
    return text
