
import os


def get_file_extension(filename):
    # Extract the file extension
    extension = os.path.splitext(filename)[1]

    # Convert extension to lowercase
    return extension.lower()


def get_file_type(extension):
    # Define supported file categories
    file_types = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".pptx", ".xlsx"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
        "Audio": [".mp3", ".wav", ".aac", ".flac"],
        "Programming": [".py", ".js", ".html", ".css", ".java", ".cpp"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"]
    }

    # Identify the file category
    for category, extensions in file_types.items():
        if extension in extensions:
            return category

    return "Unknown File Type"


def analyze_file(filename):
    # Extract the file name and extension
    name, extension = os.path.splitext(filename)

    if not extension:
        return {
            "filename": filename,
            "extension": "No extension",
            "type": "Unknown File Type"
        }

    extension = extension.lower()

    return {
        "filename": name,
        "extension": extension,
        "type": get_file_type(extension)
    }


def main():
    print("=" * 50)
    print("          FILE EXTENSION EXTRACTOR")
    print("=" * 50)

    while True:
        filename = input("\nEnter a file name (e.g. document.pdf): ").strip()

        if not filename:
            print("Please enter a valid file name.")
            continue

        result = analyze_file(filename)

        print("\nFILE ANALYSIS")
        print("-" * 50)
        print(f"File Name : {result['filename']}")
        print(f"Extension : {result['extension']}")
        print(f"File Type : {result['type']}")

        choice = input("\nAnalyze another file? (yes/no): ").strip().lower()

        if choice != "yes":
            print("\nThank you for using File Extension Extractor!")
            break


if __name__ == "__main__":
    main()