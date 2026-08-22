from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum



class ProjectModel(BaseDataModel):
    """Persist RAG project records and their MongoDB indexes."""

    def __init__(self, db_client : object):
        """Connect this model to the projects collection.

        Args:
            db_client (object): Async MongoDB database handle.

        Returns:
            None: The selected collection is stored for project operations.
        """
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    @classmethod
    async def create_instance(cls, db_client : object):
        """Create a ready-to-use project model and ensure its indexes exist.

        Args:
            db_client (object): Async MongoDB database handle.

        Returns:
            ProjectModel: Initialized model used at the start of RAG requests.
        """
        instance=cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        """Create the projects collection indexes when the collection is new.

        Returns:
            None: Indexes enforce one database record per project identifier.
        """
        all_collections= await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            indexes = Project.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )


    async def create_project(self, project: Project):
        """Store a newly created RAG project.

        Args:
            project (Project): Validated project record to insert.

        Returns:
            Project: The same record populated with MongoDB's generated ID.
        """
        result = await  self.collection.insert_one(project.dict(by_alias=True,exclude_unset=True))
        project.id = result.inserted_id
        return project


    async def get_project_or_create_one(self, project_id: str):
        """Find a project or create it before files are ingested.

        Args:
            project_id (str): User-facing RAG project identifier.

        Returns:
            Project: Existing or newly inserted project database record.
        """

        record = await self.collection.find_one({
            "project_id": project_id
        })

        if record is None:
            # Every upload and processing request needs a project record to link data.
            project = Project(project_id=project_id)
            return await self.create_project(project)

            return project
        
        return Project(**record)

    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        """Read one page of RAG projects and report the page count.

        Args:
            page (int): One-based page number. Defaults to 1.
            page_size (int): Maximum projects returned per page. Defaults to 10.

        Returns:
            tuple[list[Project], int]: Project records and the total number of
            available pages.
        """

        # Count first so clients know whether more project pages are available.
        total_documents = await self.collection.count_documents({})

        # Round up when a partial final page remains.
        total_pages = total_documents // page_size 
        if total_documents % page_size > 0:
            total_pages += 1

        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects = []
        async for document in cursor:
            projects.append(
                Project(**document)
            )
        return projects, total_pages
