from pathlib import Path
<<<<<<< Updated upstream

from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader
from llama_index.readers.file import PyMuPDFReader
from pypdf import PdfReader
from PySide6.QtCore import Slot

from source.models.model_store import ModelStore
from source.models.pdf_data_model import Pdf
from source.services.service import Service, ServiceName

=======
from typing import List
from langchain.docstore.document import Document
from source.models.model_store import ModelStore
from source.models.pdf_data_model import Pdf
from source.services.service import Service, ServiceName
from transformers import AutoTokenizer, AutoModel
import torch
import rust_pdf_service
>>>>>>> Stashed changes

class PdfService(Service):
    def __init__(self) -> None:
        super().__init__()
        self.rust_service = rust_pdf_service.RustPdfService()

    @staticmethod
    def name() -> str:
        return ServiceName.PDF_SERVICE.name

    def load_pdf(self, path: Path) -> list[Document]:
        rust_documents = self.rust_service.load_pdf(str(path))
        return [Document(page_content=content, metadata={"page": i+1}) for i, content in enumerate(rust_documents)]

    def get_first_page_pdf_text(self, pdf_path: Path) -> str:
        return self.rust_service.get_first_page_pdf_text(str(pdf_path))

    def append_data(self, key: str, value: Pdf):
        ModelStore().pdf().append_data(key, value)

    def update_summaries(self, key: str, value: dict):
        ModelStore().pdf().add_summaries(key, value)

<<<<<<< Updated upstream
    def create_pdf_obj(self, path: Path, documents: list[Document], metadata: dict):
        print(path)
        print(documents)
        print(metadata)
        return Pdf(filename=path.name, path=path, documents=documents, metadata=metadata, summaries=None)
=======
    def generate_embeddings(self, text: str) -> list:
        """Generate embeddings using GTE-Small model."""
        model_name = "thenlper/gte-small"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)

        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
        return embeddings

    def create_pdf_obj(self, path: Path, documents: List[Document], metadata: dict):
        pdf_obj = Pdf(filename=path.name, path=path, documents=documents, metadata=metadata, summaries=None)
        first_page_text = self.get_first_page_pdf_text(path)
        pdf_obj.first_page_embedding = self.generate_embeddings(first_page_text)

        for doc in pdf_obj.documents:
            doc.embeddings = self.generate_embeddings(doc.page_content)

        return pdf_obj
>>>>>>> Stashed changes
