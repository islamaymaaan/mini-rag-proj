from .BaseDataModel import BaseDataModel
from .db_schemes import Project, Asset
from .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId


class AssetModel(BaseDataModel):
    """Persist uploaded RAG source files and retrieve them by project."""

    def __init__(self, db_client: object):
        """Connect this model to the source-asset collection.

        Args:
            db_client (object): Async MongoDB database handle.

        Returns:
            None: Asset operations use the selected collection.
        """
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        """Create an asset model and ensure its required indexes exist.

        Args:
            db_client (object): Async MongoDB database handle.

        Returns:
            AssetModel: Initialized model for upload and processing routes.
        """
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        """Create indexes for the asset collection when it is first used.

        Returns:
            None: The compound index prevents duplicate file names per project.
        """
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_asset(self, asset: Asset):
        """Save metadata for a file accepted into the RAG pipeline.

        Args:
            asset (Asset): File metadata including owner project and disk name.

        Returns:
            Asset: Inserted asset with its generated MongoDB ID.
        """
        result = await self.collection.insert_one(
            asset.dict(by_alias=True, exclude_unset=True)
        )
        asset.id = result.inserted_id
        return asset

    async def get_all_project_assets(self, asset_project_id: str,asset_type: str):
      """List a project's source assets of one type.

      Args:
          asset_project_id (str | ObjectId): MongoDB ID of the owning project.
          asset_type (str): Asset category, such as ``file``.

      Returns:
          list[Asset]: Files that should be loaded and chunked for RAG.
      """

      records= await self.collection.find({
          "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id,str) else asset_project_id,
          "asset_type":asset_type,
      }).to_list(length= None)

      return [
          Asset(**record)
          for record in records 
      ]

    async def get_asset_record(self, asset_project_id: str, asset_name: str):
        """Find one uploaded source by project and stored filename.

        Args:
            asset_project_id (str | ObjectId): MongoDB ID of the owner project.
            asset_name (str): Generated filename stored for the asset.

        Returns:
            Asset | None: Matching source metadata, or ``None`` when absent.
        """
        record = await self.collection.find_one({
            "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id,str) else asset_project_id,
            "asset_name": asset_name
        })

        if record:
            return Asset(**record)
        return None
