from database.models import User
from database.session import SessionDep
from domain.user.user_exceptions import (
    DuplicateUserError,
    UserDatabaseError,
    UserNotFoundError,
)
from domain.user.user_schema import UserCreate, UserUpdate
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlmodel import select


class UserRepo:
    def __init__(self, session: SessionDep):
        self.session = session

    async def get_users(self) -> list[User]:
        """Get all users sorted by email.

        Returns:
            list[User]: List of all users

        Raises:
            UserDatabaseError: If database operation fails
        """
        try:
            statement = select(User).order_by(User.email)
            result = await self.session.exec(statement)
            return result.all()
        except SQLAlchemyError as e:
            raise UserDatabaseError(message=f"Failed to fetch users: {str(e)}")

    async def get_user(self, id: str) -> User:
        """Get a single user by ID.

        Args:
            id (str): User ID

        Returns:
            User: The requested user

        Raises:
            UserDatabaseError: If user not found or database operation fails
            UserNotFoundError: If user not found
        """
        try:
            found_user = await self.session.get(User, id)
            if not found_user:
                raise UserNotFoundError(
                    message=f"User with ID '{id}' not found",
                )
            return found_user
        except SQLAlchemyError as e:
            raise UserDatabaseError(message=f"Failed to fetch user: {str(e)}")

    async def get_user_by_email(self, email: str) -> User:
        """Get a single user by email.

        Args:
            email (str): User email

        Returns:
            User: The requested user

        Raises:
            UserDatabaseError: If user not found or database operation fails
            UserNotFoundError: If user not found
        """
        try:
            statement = select(User).where(User.email == email)
            result = await self.session.exec(statement)
            found_user = result.first()

            if not found_user:
                raise UserNotFoundError(
                    message=f"User with email '{email}' not found",
                )
            return found_user
        except SQLAlchemyError as e:
            raise UserDatabaseError(message=f"Failed to fetch user: {str(e)}")

    async def add_user(self, user: UserCreate) -> User:
        """Add a new user to the database.

        Args:
            user (UserCreate): User creation data

        Returns:
            User: The newly created user

        Raises:
            UserDatabaseError: If database operation fails or user with
        """
        try:
            db_user = User.model_validate(user)
            return await self._save_user(db_user)
        except IntegrityError:
            await self.session.rollback()
            raise DuplicateUserError(
                message=f"User with email '{user.email}' already exists",
            )
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise UserDatabaseError(message=f"Failed to add user: {str(e)}")

    async def update_user(self, id: str, user: UserUpdate) -> User:
        """Update an existing user.

        Args:
            id (str): User ID
            user (UserUpdate): User update data

        Returns:
            User: The updated user

        Raises:
            UserDatabaseError: If user not found, database operation fails, or user with new email already exists
            UserNotFoundError: If user not found
            DuplicateUserError: If user with new email already exists
        """
        try:
            db_user = await self.get_user(id)
            # Update user data excluding None values
            user_data = user.model_dump(exclude_unset=True)
            for key, value in user_data.items():
                setattr(db_user, key, value)

            return await self._save_user(db_user)
        except UserDatabaseError as e:
            raise e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise UserDatabaseError(message=f"Failed to update user: {str(e)}")

    async def delete_user(self, id: str):
        """Delete a user by ID.

        Args:
            id (str): User ID

        Raises:
            UserDatabaseError: If user has associated journal entries or database operation fails
            UserNotFoundError: If user not found
        """
        try:
            async with self.session.begin():
                user = await self.get_user(id)
                await self.session.delete(user)
        except SQLAlchemyError as e:
            raise UserDatabaseError(
                message=f"Failed to delete user: {str(e)}",
            )

    async def _save_user(self, user: User) -> User:
        """Save user to database and refresh.

        Args:
            user: User instance to save

        Returns:
            User: Refreshed user instance

        Raises:
            SQLAlchemyError: If database operation fails
        """
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
