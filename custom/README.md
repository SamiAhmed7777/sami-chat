# OpenWebUI Container Management Plugin

This plugin adds container management capabilities to OpenWebUI, allowing you to monitor, update, and restart the container directly from the web interface.

## Features

- View container status and version
- Update container to the latest version
- Restart container when needed
- User-friendly interface integrated into OpenWebUI settings

## Installation

### Installing in Docker-based OpenWebUI

1. If your OpenWebUI is running in Docker, mount the plugin directory into the container by adding this volume to your docker-compose.yml:
   ```yaml
   services:
     openwebui:
       volumes:
         - ./custom:/app/custom  # Mount the plugin directory
   ```

2. Copy the `custom` directory to your OpenWebUI installation directory (where your docker-compose.yml is located)

3. Restart your OpenWebUI container:
   ```bash
   docker-compose restart openwebui
   ```

The plugin will be automatically detected and loaded by OpenWebUI when it starts.

### Dependencies

The plugin requires the following Python packages which are already included in the OpenWebUI Docker image:
- fastapi
- docker-py

## Usage

1. Navigate to the OpenWebUI settings page
2. Look for the "Container Management" section
3. You can:
   - View the current container status and version
   - Click "Update Container" to update to the latest version
   - Click "Restart Container" to restart the container

## API Endpoints

The plugin exposes the following API endpoints:

- `GET /api/container/status` - Get container status and version
- `POST /api/container/update` - Update the container
- `POST /api/container/restart` - Restart the container

## Development

To modify or extend the plugin:

1. Frontend components are in `custom/components/`
2. Backend API routes are in `custom/api/`
3. Container management logic is in `custom/container_manager.py`
4. Plugin registration is handled in `custom/plugin.py`

### Development Workflow

1. Make changes to the plugin code
2. The changes will be reflected immediately in the OpenWebUI container due to the volume mount
3. If you modify Python files, you'll need to restart the OpenWebUI container:
   ```bash
   docker-compose restart openwebui
   ```
4. Frontend changes (Svelte components) will be hot-reloaded automatically

## Contributing

Feel free to submit issues and pull requests to improve the plugin. 