from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId


class Project(BaseModel):
    """Validate the database record that represents one RAG project."""
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @validator("project_id")
    def validate_project_id(cls, value):
        """Require a simple alphanumeric identifier for project storage paths.

        Args:
            value (str): Proposed user-facing project ID.

        Returns:
            str: The validated identifier used to link assets and chunks.

        Raises:
            ValueError: If the ID contains non-alphanumeric characters.
        """
        if not value.isalnum():
            raise ValueError("project_id must be alphanumeric")
        return value

    class Config:
        arbitrary_types_allowed = True
    
    @classmethod
    def get_indexes(cls):
        """Describe MongoDB indexes required by project records.

        Returns:
            list[dict]: Unique index definition for ``project_id``.
        """
        return[
            {
                "key": [("project_id",1)
                    
                ],

                "name":"project_id_index_1",

                "unique": True

            }
        ]
