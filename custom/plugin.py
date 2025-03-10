from fastapi import FastAPI
from .api.container_routes import router as container_router

def register_plugin(app: FastAPI) -> None:
    """Register the container management plugin with OpenWebUI."""
    # Register API routes
    app.include_router(
        container_router,
        prefix="/api/container",
        tags=["container"]
    )

    # Register frontend components
    app.state.plugin_components = app.state.plugin_components or {}
    app.state.plugin_components["container_settings"] = {
        "name": "ContainerSettings",
        "path": "custom/components/ContainerSettings.svelte",
        "settings": {
            "title": "Container Management",
            "icon": "container",
            "description": "Manage container updates and status"
        }
    } 