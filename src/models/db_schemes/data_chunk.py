from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class DataChunk(BaseModel):
    """Validate a single text segment produced during RAG document processing."""
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: ObjectId
    chunk_asset_id : ObjectId
    


    class Config:
        """Allow Pydantic to retain MongoDB ``ObjectId`` references."""
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
            """Describe the index used to retrieve or reset project chunks.

            Returns:
                list[dict]: Non-unique index definition for ``chunk_project_id``.
            """
            return[
                {
                    "key": [("chunk_project_id",1)
                        
                    ],
    
                    "name":"chunk_project_id_index_1",
    
                    "unique": False
    
                }
            ]
