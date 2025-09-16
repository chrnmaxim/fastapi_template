import uuid
from typing import Any, Generic, Literal, Tuple, Type, TypeVar, overload

from pydantic import BaseModel
from sqlalchemy import Select, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from sqlalchemy.sql._typing import _ColumnExpressionArgument

from src.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    The main interface class for basic CRUD operations with DB models.

    Attributes:
        model (Type[ModelType]): SQLAlchemy model.
    """

    model: Type[ModelType]

    # MARK: Create
    @overload
    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        create_data: CreateSchemaType | dict[str, Any],
        return_type: Literal["model"] = "model",
    ) -> ModelType: ...
    @overload
    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        create_data: CreateSchemaType | dict[str, Any],
        return_type: Literal["id_int"],
    ) -> int: ...
    @overload
    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        create_data: CreateSchemaType | dict[str, Any],
        return_type: Literal["id_uuid"],
    ) -> uuid.UUID: ...
    @overload
    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        create_data: CreateSchemaType | dict[str, Any],
        return_type: None,
    ) -> None: ...

    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        create_data: CreateSchemaType | dict[str, Any],
        return_type: Literal["model", "id_int", "id_uuid"] | None = "model",
    ) -> ModelType | uuid.UUID | int | None:
        """
        Add a record to the current session.

        If `create_data` is a Pydantic model, fields not explicitly set are excluded.

        Args:
            session(AsyncSession): Asynchronous SQLAlchemy session.
            create_data(CreateSchemaType|dict[str, Any]): Pydantic schema or dictionary of data to update.
            return_type(Literal["model", "id"] | None): function return type, `model` by default.

        Returns:
            ModelType|uuid.UUID|None:
                created model instance or `id` of the created model instance
                or `None` depends on `return_type`.
        """

        if isinstance(create_data, dict):
            create_data = create_data
        else:
            create_data = create_data.model_dump(exclude_unset=True)

        stmt = insert(cls.model).values(**create_data)

        if return_type is None:
            await session.execute(stmt)
            return None
        elif return_type in ("id_int", "id_uuid"):
            stmt = stmt.returning(cls.model.id)  # type: ignore
        elif return_type == "model":
            stmt = stmt.returning(cls.model)

        result = await session.execute(stmt)
        return result.scalar_one()

    @overload
    @classmethod
    async def add_bulk(
        cls,
        session: AsyncSession,
        create_data: list[dict[str, Any]],
        return_type: Literal["model"] = "model",
    ) -> list[ModelType]: ...
    @overload
    @classmethod
    async def add_bulk(
        cls,
        session: AsyncSession,
        create_data: list[dict[str, Any]],
        return_type: Literal["id"],
    ) -> list[uuid.UUID]: ...
    @overload
    @classmethod
    async def add_bulk(
        cls, session: AsyncSession, create_data: list[dict[str, Any]], return_type: None
    ) -> None: ...

    @classmethod
    async def add_bulk(
        cls,
        session: AsyncSession,
        create_data: list[dict[str, Any]],
        return_type: Literal["model", "id"] | None = "model",
    ) -> list[ModelType] | list[uuid.UUID] | None:
        """
        Add multiple records to the current session.

        Args:
            session(AsyncSession): Asynchronous SQLAlchemy session.
            create_data(list[dict[str, Any]]): data to create.
            return_type(Literal["model", "id"] | None): function return type, `model` by default.

        Returns:
            list[ModelType]|list[uuid.UUID]|None:
                list of created model instances or list of created model ids
                or `None` depends on `return_type`.
        """

        stmt = insert(cls.model)

        if return_type is None:
            await session.execute(stmt, create_data)
            return None
        elif return_type == "id":
            stmt = stmt.returning(cls.model.id)  # type: ignore
        elif return_type == "model":
            stmt = stmt.returning(cls.model)

        result = await session.execute(stmt, create_data)
        return result.scalars().all()

    # MARK: Read
    @classmethod
    async def get_one_or_none(
        cls, *where: _ColumnExpressionArgument[bool], session: AsyncSession
    ) -> ModelType | None:
        """
        Return a single record matching `where` clauses or `None` if no record was found.

        Args:
            where: where clauses.
            session(AsyncSession): Asynchronous SQLAlchemy session.

        Returns:
            ModelType|None: The model instance found, or `None` if no record was found.
        """

        stmt = select(cls.model).where(*where)
        return await session.scalar(stmt)

    @classmethod
    async def get_one_or_none_id(
        cls, *where: _ColumnExpressionArgument[bool], session: AsyncSession
    ) -> uuid.UUID | None:
        """
        Return an `id` of single record matching `where` clauses or `None` if no record was found.

        Args:
            where: where clauses.
            session(AsyncSession): Asynchronous SQLAlchemy session.

        Returns:
            uuid.UUID|None: The model instance id found, or `None` if no record was found.
        """

        stmt = select(cls.model.id).where(*where)  # type: ignore
        return await session.scalar(stmt)

    @classmethod
    async def get_exactly_one(
        cls, *where: _ColumnExpressionArgument[bool], session: AsyncSession
    ) -> ModelType:
        """
        Return exactly one result matching `where` clauses or raise an exception.

        Args:
            where: where clauses.
            session(AsyncSession): Asynchronous SQLAlchemy session.

        Returns:
            ModelType: The model instance found.
        """

        stmt = select(cls.model).where(*where)
        result = await session.execute(stmt)
        return result.scalar_one()

    # MARK: Update
    @overload
    @classmethod
    async def update(
        cls,
        *where: _ColumnExpressionArgument[bool],
        session: AsyncSession,
        update_data: UpdateSchemaType | dict[str, Any],
        return_type: Literal["model"] = "model",
    ) -> ModelType | None: ...
    @overload
    @classmethod
    async def update(
        cls,
        *where: _ColumnExpressionArgument[bool],
        session: AsyncSession,
        update_data: UpdateSchemaType | dict[str, Any],
        return_type: Literal["id_uuid"],
    ) -> uuid.UUID | None: ...
    @overload
    @classmethod
    async def update(
        cls,
        *where: _ColumnExpressionArgument[bool],
        session: AsyncSession,
        update_data: UpdateSchemaType | dict[str, Any],
        return_type: Literal["id_int"],
    ) -> int | None: ...
    @overload
    @classmethod
    async def update(
        cls,
        *where: _ColumnExpressionArgument[bool],
        session: AsyncSession,
        update_data: UpdateSchemaType | dict[str, Any],
        return_type: None,
    ) -> None: ...

    @classmethod
    async def update(
        cls,
        *where: _ColumnExpressionArgument[bool],
        session: AsyncSession,
        update_data: UpdateSchemaType | dict[str, Any],
        return_type: Literal["model", "id_uuid", "id_int"] | None = "model",
    ) -> ModelType | uuid.UUID | int | None:
        """
        Update a record in the current session matching `where` clauses.

        If `update_data` is a Pydantic model, fields not explicitly set are excluded.

        Args:
            where: where clauses.
            session(AsyncSession): Asynchronous SQLAlchemy session.
            update_data(UpdateSchemaType|dict[str, Any]): Pydantic schema or dictionary of data to update.
            return_type(Literal["model", "id_int", "id_uuid] | None): function return type, `model` by default.

        Returns:
            ModelType|uuid.UUID|None:
                updated model instance, `id` of the updated model instance
                or `None` depends on `return_type` or if no record was found.
        """

        if isinstance(update_data, dict):
            update_data = update_data
        else:
            update_data = update_data.model_dump(exclude_unset=True)

        stmt = update(cls.model).where(*where).values(**update_data)

        if return_type is None:
            await session.execute(stmt)
            return None
        elif return_type in ("id_uuid", "id_int"):
            stmt = stmt.returning(cls.model.id)  # type: ignore
        elif return_type == "model":
            stmt = stmt.returning(cls.model)

        return await session.scalar(stmt)

    @classmethod
    async def update_bulk(
        cls, session: AsyncSession, update_data: list[dict[str, Any]]
    ) -> None:
        """
        Update multiple records in the database at once with different data.

        Args:
            session(AsyncSession): асинхронная сессия SQLAlchemy;
            data(list[dict[str, Any]]):
                a list containing dictionaries of each record's primary key and the data to update it with.
        """

        await session.execute(update(cls.model), update_data)

    # MARK: Delete
    @overload
    @classmethod
    async def delete(
        cls,
        *where: _ColumnExpressionArgument[bool],
        session: AsyncSession,
        return_type: Literal["model"] = "model",
    ) -> ModelType | None: ...
    @overload
    @classmethod
    async def delete(
        cls,
        *where: _ColumnExpressionArgument[bool],
        session: AsyncSession,
        return_type: Literal["id_uuid"],
    ) -> uuid.UUID | None: ...
    @overload
    @classmethod
    async def delete(
        cls,
        *where: _ColumnExpressionArgument[bool],
        session: AsyncSession,
        return_type: Literal["id_int"],
    ) -> int | None: ...
    @overload
    @classmethod
    async def delete(
        cls,
        *where: _ColumnExpressionArgument[bool],
        session: AsyncSession,
        return_type: None,
    ) -> None: ...

    @classmethod
    async def delete(
        cls,
        *where: _ColumnExpressionArgument[bool],
        session: AsyncSession,
        return_type: Literal["model", "id_uuid", "id_int"] | None = "model",
    ) -> ModelType | uuid.UUID | int | None:
        """
        Delete a record matching `where` clauses.

        Args:
            where: where clauses.
            session(AsyncSession): Asynchronous SQLAlchemy session.
            return_type(Literal["model", "id_uuid", "id_int"] | None): function return type, `model` by default.

        Returns:
            ModelType|uuid.UUID|None:
                deleted model instance, `id` of the deleted model instance
                or `None` depends on `return_type` or if no record was found.
        """

        if return_type is None:
            stmt = delete(cls.model).where(*where)
            await session.execute(stmt)
            return None
        elif return_type in ("id_uuid", "id_int"):
            stmt = delete(cls.model).where(*where).returning(cls.model.id)  # type: ignore
        elif return_type == "model":
            stmt = delete(cls.model).where(*where).returning(cls.model)  # type: ignore

        return await session.scalar(stmt)

    # MARK: Count
    @classmethod
    async def count(
        cls, *where: _ColumnExpressionArgument[bool], session: AsyncSession
    ) -> int:
        """
        Count rows in the database matching `where` clauses.

        Args:
            where: where clauses.
            session(AsyncSession): Asynchronous SQLAlchemy session.

        Returns:
            rows_count: number of rows found, or 0 if no matches were found.
        """

        stmt = select(func.count()).select_from(cls.model).where(*where)
        return await session.scalar(stmt) or 0

    @classmethod
    async def count_from_stmt(
        cls, session: AsyncSession, count_stmt: Select[Tuple[int]]
    ) -> int:
        """
        Get the total number of entities in the database using the expression
        for counting rows in the database, previously compiled.

        Args:
            session(AsyncSession): Asynchronous SQLAlchemy session.
            count_stmt(Select[Tuple[int]]): expression for counting rows in the database.

        Returns:
            rows_count: number of rows found, or 0 if no matches were found.
        """

        return await session.scalar(count_stmt) or 0

    # MARK: Exists
    @classmethod
    async def check_if_exists(
        cls, *where: _ColumnExpressionArgument[bool], session: AsyncSession
    ) -> bool:
        """
        Check if record matching where clauses exists in the database

        Args:
            where: where clauses.
            session(AsyncSession): Asynchronous SQLAlchemy session.

        Returns:
            bool: `True` if record exists, `False` otherwise.
        """

        stmt = select(1).select_from(cls.model).where(*where)
        return bool(await session.scalar(stmt))
