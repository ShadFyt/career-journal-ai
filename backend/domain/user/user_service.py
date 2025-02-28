from database.models import User
from domain.user.user_repo import UserRepo
from domain.user.user_schema import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repo: UserRepo) -> None:
        self.user_repo = user_repo

    async def get_users(self) -> list[User]:
        """Get all users sorted by email.

        Returns:
            list[User]: List of all users

        Raises:
            UserDatabaseError: If database operation fails
        """
        return await self.user_repo.get_users()

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
        return await self.user_repo.get_user(id)

    async def add_user(self, user: UserCreate) -> User:
        """Add a new user to the database.

        Args:
            user (UserCreate): User creation data

        Returns:
            User: The newly created user

        Raises:
            UserDatabaseError: If database operation fails or user with
            DuplicateUserError: If user with email already exists
        """
        return await self.user_repo.add_user(user)

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
        return await self.user_repo.update_user(id, user)

    async def delete_user(self, id: str) -> None:
        """Delete a user by ID.

        Args:
            id (str): User ID

        Raises:
            UserDatabaseError: If user has associated journal entries or database operation fails
            UserNotFoundError: If user not found
        """
        return await self.user_repo.delete_user(id)
