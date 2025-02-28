from core.exceptions import BaseDomainError
from domain.user.user_dependencies import UserServiceDep
from domain.user.user_schema import UserCreate, UserRead, UserUpdate
from fastapi import APIRouter, status

router = APIRouter()


@router.get("", response_model=list[UserRead])
async def get_users(
    service: UserServiceDep,
) -> list[UserRead]:
    """Get all users sorted by email.

    Returns:
        list[User]: List of all users

    Raises:
        UserDatabaseError: If database operation fails
    """
    try:
        return await service.get_users()
    except BaseDomainError as e:
        raise e


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def add_user(
    user: UserCreate,
    service: UserServiceDep,
) -> UserRead:
    """Add a new user.

    Args:
        user: User creation data
        service: User service instance

    Returns:
        User: The newly created user

    Raises:
        UserDatabaseError: If database operation fails or user with given email already exists
        DuplicateUserError: If user with email already exists
    """
    try:
        return await service.add_user(user)
    except BaseDomainError as e:
        raise e


@router.get("/{id}", response_model=UserRead)
async def get_user(
    id: str,
    service: UserServiceDep,
) -> UserRead:
    """Get a single user by ID.

    Args:
        id: User ID
        service: User service instance

    Returns:
        User: The requested user
    """
    try:
        return await service.get_user(id)
    except BaseDomainError as e:
        raise e


@router.patch("/{id}")
async def update_user(
    id: str,
    user: UserUpdate,
    service: UserServiceDep,
) -> UserRead:
    """Update an existing user.

    Args:
        id: User ID
        user: User update data
        service: User service instance

    Returns:
        User: The updated user

    Raises:
        UserDatabaseError: If database operation fails
        UserNotFoundError: If user not found
    """
    try:
        return await service.update_user(id, user)
    except BaseDomainError as e:
        raise e


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: str,
    service: UserServiceDep,
) -> None:
    """Delete a user from the database by its ID.

    Args:
        id: Unique identifier of the user to delete
        service: User service instance

    Raises:
        HTTPException: If the request fails
    """
    try:
        await service.delete_user(id)
    except BaseDomainError as e:
        raise e
