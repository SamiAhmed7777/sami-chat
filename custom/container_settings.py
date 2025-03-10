"""
type: settings
name: Container Settings
description: Manage chat.Sami container settings
version: 1.0.0
author: chat.Sami
"""

from typing import Dict, Any
import json
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ContainerSettings(BaseModel):
    """Container management settings."""
    enabled: bool = True

@router.get("/settings/container")
async def get_container_settings() -> Dict[str, Any]:
    """Get container management settings."""
    return {
        "id": "container",
        "title": "Container Management",
        "description": "Manage the chat.Sami container",
        "component": "ContainerStatus",
        "settings": ContainerSettings().dict()
    }

class Settings:
    def __init__(self):
        self.settings = {
            "container": {
                "title": "Container Management",
                "description": "Manage your chat.Sami container",
                "type": "object",
                "properties": {
                    "status": {
                        "type": "custom",
                        "component": "ContainerStatus",
                        "action": "container_status",
                        "refresh_interval": 30,  # Refresh every 30 seconds
                        "title": "Container Status"
                    },
                    "update": {
                        "type": "button",
                        "title": "Update Container",
                        "description": "Update chat.Sami to the latest version",
                        "action": "update_container",
                        "buttonText": "Update Now",
                        "confirmText": "Are you sure you want to update the container? The service will restart briefly."
                    }
                }
            }
        }

    def get_settings(self) -> Dict[str, Any]:
        return self.settings

    def update_settings(self, settings: Dict[str, Any]) -> Dict[str, Any]:
        # This is a read-only settings panel
        return {
            "success": True,
            "message": "Settings updated"
        } 