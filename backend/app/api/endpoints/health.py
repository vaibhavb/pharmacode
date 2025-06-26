from fastapi import APIRouter
import time

router = APIRouter()

@router.get("/")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "PharmaCode API"
    }
