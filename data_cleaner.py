import csv
import re

def clean_text(text):
    """Removes extra spaces and normalizes text."""
    if not text:
        return ""
    # Remove leading/trailing spaces and collapse multiple spaces
    return re.sub(r'\s+', ' ', text.strip())

def clean_csv(input_file, output_file):
    """Reads a messy CSV, cleans strings, drops duplicate rows, and exports a clean file."""
    seen_rows = set()
    cleaned_data = []

    print(f"Processing '{input_file}'...")

    try:
        with open(input_file, mode='r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader, None)
            
            if header:
                cleaned_header = [clean_text(col).title() for col in header]
                cleaned_data.append(cleaned_header)

            for row in reader:
                # Clean each cell in the row
                cleaned_row = tuple(clean_text(cell) for cell in row)
                
                # Skip completely empty rows
                if not any(cleaned_row):
                    continue

                # Remove duplicates
                if cleaned_row not in seen_rows:
                    seen_rows.add(cleaned_row)
                    cleaned_data.append(list(cleaned_row))

        # Write cleaned data to output CSV
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(cleaned_data)

        print(f"Success! Cleaned data saved to '{output_file}'.")

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage
    input_filename = "raw_data.csv"
    output_filename = "cleaned_data.csv"
    clean_csv(input_filename, output_filename)
