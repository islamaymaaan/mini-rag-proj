from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader,PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum

class ProcessController(BaseController):
    """Load project files and split their text into retrieval-ready documents."""

    def __init__(self,project_id:str):
        """Set up file processing for one RAG project.

        Args:
            project_id (str): Project whose stored files will be loaded.

        Returns:
            None: Stores the project's asset directory for later file lookups.
        """
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str):
        """Extract a stored file's extension for loader selection.

        Args:
            file_id (str): Stored RAG asset filename.

        Returns:
            str: Extension including the leading period, such as ``.pdf``.
        """
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):
        """Choose a LangChain loader for one stored RAG source.

        Args:
            file_id (str): Stored filename to load from the current project.

        Returns:
            TextLoader | PyMuPDFLoader | None: A compatible loader, or ``None``
            when the source file is absent.

        Raises:
            ValueError: If the file extension is not supported by the pipeline.
        """

        file_ext = self.get_file_extension(file_id)

        file_path = os.path.join(
            self.project_path,
              file_id)

        if not os.path.exists(file_path):
            return None

        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        
        elif file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        
        else:
            raise ValueError(f"Unsupported file extension: {file_ext}")

    def get_file_content(self, file_id: str):
        """Load a source file into LangChain document objects.

        Args:
            file_id (str): Stored filename for the source asset.

        Returns:
            list | None: Loaded documents and metadata, or ``None`` if the file
            no longer exists. These documents are the input to chunking.
        """
        loader = self.get_file_loader(file_id=file_id)
        if loader:
            return loader.load()
        return None

    def process_file_content(self, file_content: list,file_id: str,
                              chunk_size: int = 100, overlap_size: int = 20):
        """Split loaded documents into overlapping chunks for RAG retrieval.

        Args:
            file_content (list): LangChain documents loaded from one source file.
            file_id (str): Stored filename being processed; retained for the
                processing interface.
            chunk_size (int): Maximum characters per chunk. Defaults to 100.
            overlap_size (int): Characters shared by neighboring chunks. Defaults
                to 20, preserving context across chunk boundaries.

        Returns:
            list: LangChain document chunks with their source metadata preserved.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )

        # Split text and metadata separately so every output chunk retains context.
        file_content_text = [
            rec.page_content
            for rec in file_content
        ]
        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(
            file_content_text,
            metadatas=file_content_metadata 
        )

        return chunks
        
