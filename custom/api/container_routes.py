from fastapi import APIRouter, HTTPException
from typing import Dict
from ..container_manager import ContainerManager

router = APIRouter()
container_manager = ContainerManager()

@router.get("/status")
async def get_container_status() -> Dict:
    """Get the current status and version of the container."""
    try:
        status = container_manager.get_status()
        version = container_manager.get_version()
        return {
            "status": status,
            "version": version
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update")
async def update_container() -> Dict:
    """Update the container to the latest version."""
    try:
        success = container_manager.update()
        return {
            "success": success,
            "message": "Container updated successfully" if success else "Update failed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/restart")
async def restart_container() -> Dict:
    """Restart the container."""
    try:
        success = container_manager.restart()
        return {
            "success": success,
            "message": "Container restarted successfully" if success else "Restart failed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 