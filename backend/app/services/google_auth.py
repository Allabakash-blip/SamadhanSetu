from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException
from app.core.config import settings

def verify_google_credential(credential: str):
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="GOOGLE_CLIENT_ID is not configured")
    try:
        info = id_token.verify_oauth2_token(
            credential, requests.Request(), settings.GOOGLE_CLIENT_ID
        )
        if info.get("iss") not in ("accounts.google.com", "https://accounts.google.com"):
            raise HTTPException(status_code=401, detail="Invalid Google issuer")
        return info
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google credential")
