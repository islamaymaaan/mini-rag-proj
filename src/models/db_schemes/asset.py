from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class Asset(BaseModel):
    """Validate metadata for an uploaded source file in the RAG pipeline."""
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    asset_project_id: ObjectId
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: int = Field(ge=0, default=None)
    asset_config: dict = Field(default=None)
    asset_pushed_at: datetime = Field(default=datetime.utcnow)

    class Config:
            """Allow Pydantic to preserve MongoDB ``ObjectId`` values."""
            arbitrary_types_allowed = True
            
        
    @classmethod
    def get_indexes(cls):
          """Describe indexes used to find a project's uploaded source files.

          Returns:
              list[dict]: Project lookup and unique project/filename index rules.
          """
          return[
                {
                "key": [("asset_project_id",1)
                    
                ],

                "name":"asset_project_id_index_1",

                "unique": False

            },
            {
                "key": [("asset_project_id",1),
                        ("asset_name",1)
                        
                ],

                "name":"asset_project_id_name_index_1",

                "unique": True

                            },
                    ]
