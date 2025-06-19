"""
Authentication dependencies
API key verification utilities
"""
from fastapi import Header, HTTPException

async def verify_api_key(api_key: str = Header(...)):
    """Verify API key middleware"""
    if api_key != "secretcode":
        raise HTTPException(status_code=401)
    return True
