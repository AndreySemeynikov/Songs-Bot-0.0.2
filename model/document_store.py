import logging
import time
from typing import Optional, Dict, List
from model.document import Document  # Import the Document class


class DocumentStore:
    """
    The DocumentStore class stores documents and provides fast lookup
    by short id, by filename, and by content.
    """

    def __init__(self):
        # Dictionary for fast access by id (key - short id)
        self._by_id: Dict[str, Document] = {}
        # Additional index by filename (key - filename)
        self._by_filename: Dict[str, Document] = {}
        logging.debug("DocumentStore initialized")

    def add_document(self, doc: Document) -> None:
        """
        Adds a document to the store.
        If a document with the same id or filename already exists,
        it will be overwritten.
        """
        self._by_id[doc.id] = doc
        self._by_filename[doc.filename] = doc
        logging.debug("Document added: id=%s, filename=%s", doc.id, doc.filename)

    def get_by_id(self, id: str) -> Optional[Document]:
        """
        Returns the document by short id, or None if not found.
        """
        return self._by_id.get(id)

    def get_by_filename(self, filename: str) -> Optional[Document]:
        """
        Returns the document by filename, or None if not found.
        """
        return self._by_filename.get(filename)

    def remove_by_id(self, id: str) -> bool:
        """
        Removes a document by id.
        Returns True if the document was removed, otherwise False.
        """
        doc = self._by_id.pop(id, None)
        if doc:
            self._by_filename.pop(doc.filename, None)
            logging.info("Document removed: id=%s, filename=%s", id, doc.filename)
            return True
        logging.warning("Document with id=%s not found for removal", id)
        return False

    def all_documents(self) -> List[Document]:
        """
        Returns a list of all documents.
        """
        return list(self._by_id.values())

    def search_by_content(self, query: str) -> List[Document]:
        """
        Searches for documents by content.
        The search is case-insensitive.
        Returns a list of documents whose content contains the query.
        Execution time is logged.
        """
        start_time = time.time()
        query_lower = query.lower()
        result = [doc for doc in self._by_id.values() if query_lower in doc.content.lower()]
        elapsed_time = time.time() - start_time
        logging.info("Search for content '%s' completed in %.4f seconds. Documents found: %d",
                     query, elapsed_time, len(result))
        return result
