import os

from dotenv import load_dotenv
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AuthProvider
from starlette_admin.exceptions import LoginFailed

load_dotenv()


class AdminAuth(AuthProvider):
    """Custom authentication provider for admin interface."""

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        """Validate login credentials."""
        admin_username = os.getenv("ADMIN_USERNAME")
        admin_password = os.getenv("ADMIN_PASSWORD")

        if not admin_username or not admin_password:
            raise LoginFailed("Admin credentials not configured")

        if username == admin_username and password == admin_password:
            request.session.update({"username": username})
            return response
        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request: Request) -> bool:
        """Check if user is authenticated."""
        if request.session.get("username", None) is not None:
            return True
        return False

    async def logout(self, request: Request, response: Response) -> Response:
        """Handle logout."""
        request.session.clear()
        return response
