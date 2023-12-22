from google.auth.transport import requests
from google.oauth2 import id_token

from core.config import SETTINGS


async def verify_token(token):
    try:
        id_info: dict = id_token.verify_oauth2_token(token, requests.Request(), SETTINGS.GOOGLE_CLIENT_ID)
        return id_info["email"], id_info.get("name", None), id_info.get("picture", None)
    except Exception as e:
        raise e
