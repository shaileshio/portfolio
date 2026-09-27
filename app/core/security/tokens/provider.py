from .manager import TokenManager
from .verifier import TokenVerifier


def get_token_manager() -> TokenManager:
    return TokenManager(TokenVerifier())
