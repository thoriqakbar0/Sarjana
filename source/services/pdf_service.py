from pathlib import Path

from langchain.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader
from llama_index.readers.file import PyMuPDFReader
from pypdf import PdfReader
from PySide6.QtCore import Slot
from typing import List

from source.models.model_store import ModelStore
from source.models.pdf_data_model import Pdf
from source.services.service import Service, ServiceName

# Thor: add embedidng model
from transformers import AutoTokenizer, AutoModel
import torch



class PdfService(Service):
    """Service to handle PDF data"""

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def name() -> str:
        return ServiceName.PDF_SERVICE.name

    def load_pdf(self, path: Path) -> list[Document]:
        pdf_loader = PyPDFLoader(str(path))
        documents = pdf_loader.load_and_split()
        return documents

    def get_first_page_pdf_text(self, pdf_path: Path) -> str:
        pdf = PdfReader(pdf_path)
        first_page = pdf.pages[0]
        contents = first_page.get_contents()
        texts = first_page.extract_text()
        print(contents)
        print(texts)
        return texts

    def append_data(self, key: str, value: Pdf):
        ModelStore().pdf().append_data(key, value)

    def update_summaries(self, key: str, value: dict):
        ModelStore().pdf().add_summaries(key, value)

    def create_pdf_obj(self, path: Path, documents: list[Document], metadata: dict):
        pdf_obj = Pdf(filename=path.name, path=path, documents=documents, metadata=metadata, summaries=None)
        print(path)
        print(documents)
        print(metadata)
        first_page_text = self.get_first_page_pdf_text(path)
        pdf_obj.embeddings = self.generate_embeddings(first_page_text)
        return pdf_obj
    
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
        # Generate embeddings for the first page text
        first_page_text = self.get_first_page_pdf_text(path)
        pdf_obj.first_page_embedding = self.generate_embeddings(first_page_text)

        # Add embeddings to each document
        for doc in pdf_obj.documents:
            doc.embeddings = self.generate_embeddings(doc.page_content)

        return pdf_obj
