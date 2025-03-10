"""
type: action
name: Container Manager
description: Manage chat.Sami container updates
version: 1.0.0
author: chat.Sami
"""

import os
import subprocess
import json
import requests
from typing import Dict, Any

class Action:
    def __init__(self):
        self.actions = [
            {
                "id": "update_container",
                "name": "Update Container",
                "description": "Update chat.Sami to the latest version"
            },
            {
                "id": "container_status",
                "name": "Container Status",
                "description": "Get current container status and version"
            },
            {
                "id": "check_updates",
                "name": "Check Updates",
                "description": "Check for available updates"
            }
        ]

    def execute(self, action_id: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        if action_id == "update_container":
            return self._update_container()
        elif action_id == "container_status":
            return self._get_container_status()
        elif action_id == "check_updates":
            return self._check_updates()
        else:
            raise ValueError(f"Unknown action: {action_id}")

    def _get_container_config(self) -> Dict[str, Any]:
        """Get current container configuration"""
        try:
            result = subprocess.run(
                ["docker", "inspect", "chat-sami"],
                capture_output=True,
                text=True,
                check=True
            )
            container_info = json.loads(result.stdout)[0]
            
            # Extract current configuration
            config = {
                "port": None,
                "volumes": [],
                "env": {}
            }
            
            # Get port mapping
            ports = container_info["HostConfig"]["PortBindings"]
            if "8080/tcp" in ports:
                port_info = ports["8080/tcp"][0]
                config["port"] = port_info["HostPort"]
            
            # Get volume mappings
            mounts = container_info["HostConfig"]["Mounts"]
            for mount in mounts:
                config["volumes"].append({
                    "source": mount["Source"],
                    "target": mount["Target"]
                })
            
            # Get environment variables
            env_list = container_info["Config"]["Env"]
            for env in env_list:
                if "=" in env:
                    key, value = env.split("=", 1)
                    config["env"][key] = value
            
            return config
        except Exception as e:
            return None

    def _get_current_version(self) -> str:
        try:
            result = subprocess.run(
                ["docker", "inspect", "chat-sami"],
                capture_output=True,
                text=True,
                check=True
            )
            container_info = json.loads(result.stdout)[0]
            image_tag = container_info["Config"]["Image"].split(":")[-1]
            return image_tag
        except:
            return "unknown"

    def _get_latest_version(self) -> str:
        try:
            response = requests.get(
                "https://api.github.com/repos/open-webui/open-webui/releases/latest",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()["tag_name"].lstrip('v')
            return "unknown"
        except:
            return "unknown"

    def _check_updates(self) -> Dict[str, Any]:
        current = self._get_current_version()
        latest = self._get_latest_version()
        
        return {
            "success": True,
            "data": {
                "current_version": current,
                "latest_version": latest,
                "update_available": latest != "unknown" and current != latest
            }
        }

    def _update_container(self) -> Dict[str, Any]:
        try:
            # Get current container configuration
            config = self._get_container_config()
            if not config:
                raise Exception("Failed to get current container configuration")

            # Pull the latest image
            subprocess.run(
                ["docker", "pull", "ghcr.io/open-webui/open-webui:main"],
                check=True,
                capture_output=True
            )
            
            # Stop the current container
            subprocess.run(
                ["docker", "stop", "chat-sami"],
                check=True,
                capture_output=True
            )
            
            # Remove the old container but keep the volumes
            subprocess.run(
                ["docker", "rm", "chat-sami"],
                check=True,
                capture_output=True
            )
            
            # Create new container with same configuration
            cmd = ["docker", "run", "-d", "--name", "chat-sami"]
            
            # Add port mapping
            if config["port"]:
                cmd.extend(["-p", f"{config['port']}:8080"])
            
            # Add volume mappings
            for volume in config["volumes"]:
                cmd.extend(["-v", f"{volume['source']}:{volume['target']}"])
            
            # Add environment variables
            for key, value in config["env"].items():
                cmd.extend(["-e", f"{key}={value}"])
            
            # Add image name
            cmd.append("ghcr.io/open-webui/open-webui:main")
            
            # Run the new container
            subprocess.run(cmd, check=True, capture_output=True)
            
            return {
                "success": True,
                "message": "Updated to latest version. The page will refresh in a few moments."
            }
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "message": f"Update failed: {e.stderr.decode() if e.stderr else str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error during update: {str(e)}"
            }

    def _get_container_status(self) -> Dict[str, Any]:
        try:
            # Get container info
            result = subprocess.run(
                ["docker", "inspect", "chat-sami"],
                capture_output=True,
                text=True,
                check=True
            )
            container_info = json.loads(result.stdout)[0]
            
            # Get update status
            update_info = self._check_updates()
            current_version = update_info["data"]["current_version"]
            latest_version = update_info["data"]["latest_version"]
            update_available = update_info["data"]["update_available"]
            
            return {
                "success": True,
                "data": {
                    "status": container_info["State"]["Status"],
                    "health": container_info["State"]["Health"]["Status"] if "Health" in container_info["State"] else "N/A",
                    "current_version": current_version,
                    "latest_version": latest_version,
                    "update_available": update_available,
                    "created": container_info["Created"]
                }
            }
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "message": f"Failed to get container status: {e.stderr.decode() if e.stderr else str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            } 