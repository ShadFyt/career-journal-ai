from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AuthProvider
from starlette_admin.exceptions import LoginFailed


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
        # Replace with values from environment variables
        if username == "admin" and password == "password":
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
