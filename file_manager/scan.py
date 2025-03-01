import os
import logging
import time

from model.document import Document  # Import the Document class
from model.document_store import DocumentStore  # Import the DocumentStore class


def scan_text_files(directory: str) -> DocumentStore:
    """
    Scans the specified directory for text files (.txt)
    and loads their content into a DocumentStore object.

    :param directory: The path to the directory to scan.
    :return: A DocumentStore object containing the loaded documents.
    """
    start_time = time.time()

    store = DocumentStore()
    logging.info(f"Scanning directory: {directory}")

    if not os.path.isdir(directory):
        logging.error(f"Directory does not exist: {directory}")
        return store

    counter = 1  # Use a numeric identifier for each document
    try:
        for filename in os.listdir(directory):
            # Process only files with the .txt extension
            if filename.endswith(".txt"):
                filepath = os.path.join(directory, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        content = file.read()
                    # Create a Document object with a short id, filename, and content
                    doc = Document(id=str(counter), filename=filename, content=content)
                    store.add_document(doc)
                    logging.debug(f"Loaded file: {filename} with id: {counter}")
                    counter += 1
                except Exception as e:
                    logging.error(f"Error reading file {filename}: {e}")
    except Exception as e:
        logging.error(f"Error scanning directory {directory}: {e}")

    elapsed_time = time.time() - start_time
    logging.info("Scanning completed. Total files loaded: %s . Scanned and loading content completed in %.4f seconds",
                 {len(store.all_documents())}, elapsed_time)
    return store
