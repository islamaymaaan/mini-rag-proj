from bson.objectid import ObjectId
from pymongo import InsertOne

from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum


class ChunckModel(BaseDataModel):
    """Store and manage text chunks used later for RAG retrieval.

    The existing class name is retained for compatibility, despite its spelling.
    """

    def __init__(self, db_client: object):
        """Connect this model to the collection of processed text chunks.

        Args:
            db_client (object): Async MongoDB database handle.

        Returns:
            None: Chunk operations use the selected collection.
        """
        super().__init__(db_client)
        self.collection = self.db_client[
            DataBaseEnum.COLLECTION_CHUNK_NAME.value
        ]
    @classmethod
    async def create_instance(cls, db_client : object):
        """Create a chunk model and ensure its project index is available.

        Args:
            db_client (object): Async MongoDB database handle.

        Returns:
            ChunckModel: Initialized model for persisting processed RAG chunks.
        """
        instance=cls(db_client)
        await instance.init_collection()
        return instance


    async def init_collection(self):
            """Create indexes for the chunks collection when it is new.

            Returns:
                None: The project index supports resetting and querying chunks
                associated with a single RAG project.
            """
            all_collections= await self.db_client.list_collection_names()
            if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:
                        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
                        indexes = DataChunk.get_indexes()
                        for index in indexes:
                            await self.collection.create_index(
                                index["key"],
                                name=index["name"],
                                unique=index["unique"]
                            )

    async def creat_chunk(self, chunk: DataChunk):
        """Insert one retrieval-ready RAG chunk.

        Args:
            chunk (DataChunk): Text, metadata, ordering, and source references.

        Returns:
            DataChunk: Inserted chunk populated with its MongoDB ID.
        """
        result = await self.collection.insert_one(
            chunk.dict(by_alias=True, exclude_unset=True)
        )
        chunk._id = result.inserted_id
        return chunk

    async def get_chunk(self, chunk_id: str):
        """Retrieve one stored RAG chunk by its MongoDB ID.

        Args:
            chunk_id (str | ObjectId): ID of the chunk to fetch.

        Returns:
            DataChunk | None: The stored chunk, or ``None`` when not found.
        """
        result = await self.collection.find_one(
            {"_id": ObjectId(chunk_id) if isinstance(chunk_id, str) else chunk_id}
        )

        if result is None:
            return None

        return DataChunk(**result)

    async def insert_many_chunks(self, chuncks: list, batch_size: int = 100):
        """Insert multiple chunks in batches after a source file is split.

        Args:
            chuncks (list[DataChunk]): Chunks created from one or more sources.
            batch_size (int): Maximum inserts per MongoDB bulk operation.

        Returns:
            int: Number of chunks accepted for insertion.
        """
        if not chuncks:
            return 0

        # Step by batch size so each database write receives a distinct slice.
        for i in range(0, len(chuncks), batch_size):
            batch = chuncks[i : i + batch_size]

            operations = [
                InsertOne(chunk.dict(by_alias=True, exclude_unset=True))
                for chunk in batch
            ]

            await self.collection.bulk_write(operations)

        return len(chuncks)

    async def delete_chunks_by_project_id(self, project_id: str):
        """Remove all retrieval chunks for a project before reprocessing it.

        Args:
            project_id (str | ObjectId): MongoDB ID of the project to reset.

        Returns:
            int: Number of deleted chunks.
        """
        # Accept both old string values and normal ObjectId values in stored data.
        target_project_id = project_id
        if isinstance(project_id, str) and ObjectId.is_valid(project_id):
            target_project_id = ObjectId(project_id)

        # Match either representation to support existing database records.
        result = await self.collection.delete_many(
            {
                "$or": [
                    {"chunk_project_id": target_project_id},
                    {"chunk_project_id": str(project_id)},
                ]
            }
        )

        return result.deleted_count
