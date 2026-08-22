from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    """Validate options for turning uploaded files into RAG text chunks.

    A request can process one named source or every file belonging to a project.
    """
    file_id: str =None
    chunk_size: Optional[int] = 100  
    overlap_size: Optional[int] = 20
    do_reset : Optional[int] = 0
    
