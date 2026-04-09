# Windows OS Control Module
# Handles system-level operations and automation

import subprocess
import os
import sys
import psutil
import json
from pathlib import Path
from typing import Dict, List, Any

class OSCommands:
    """Control and automate Windows operating system functions."""
    
    def __init__(self):
        """Initialize OS Commands."""
        self.known_apps = {
            "spotify": "spotify.exe",
            "vscode": "code.exe",
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "file explorer": "explorer.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe",
        }
    
    def launch_application(self, app_name: str) -> Dict[str, Any]:
        """
        Launch an application.
        
        Args:
            app_name: Name of the application to launch
            
        Returns:
            Dictionary with status and message
        """
        try:
            app_name_lower = app_name.lower()
            
            # Check known apps
            if app_name_lower in self.known_apps:
                app_exe = self.known_apps[app_name_lower]
            else:
                app_exe = app_name
            
            # Use os.startfile on Windows
            os.startfile(app_exe)
            return {"status": "success", "message": f"Launched {app_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_running_applications(self) -> Dict[str, Any]:
        """
        Get list of running applications.
        
        Returns:
            Dictionary with running process names
        """
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    processes.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return {"status": "success", "processes": list(set(processes))[:20]}  # Return top 20
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def close_application(self, app_name: str) -> Dict[str, Any]:
        """
        Close a running application.
        
        Args:
            app_name: Name of the application to close
            
        Returns:
            Dictionary with status and message
        """
        try:
            app_name_lower = app_name.lower()
            
            if app_name_lower in self.known_apps:
                app_exe = self.known_apps[app_name_lower]
            else:
                app_exe = app_name
            
            os.system(f"taskkill /IM {app_exe} /F")
            return {"status": "success", "message": f"Closed {app_name}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get system information.
        
        Returns:
            Dictionary with system details
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "status": "success",
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_available_gb": memory.available / (1024**3),
                "disk_usage": disk.percent,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def set_volume(self, level: int) -> Dict[str, Any]:
        """
        Set system volume (0-100).
        
        Args:
            level: Volume level (0-100)
            
        Returns:
            Dictionary with status and message
        """
        try:
            level = max(0, min(100, level))
            os.system(f"powershell -Command \"(New-Object -ComObject WMPlayer.OCX.7).settings.volume={level}\"")
            return {"status": "success", "message": f"Volume set to {level}%"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def open_file(self, file_path: str) -> Dict[str, Any]:
        """
        Open a file with default application.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with status and message
        """
        try:
            if os.path.exists(file_path):
                os.startfile(file_path)
                return {"status": "success", "message": f"Opened {file_path}"}
            else:
                return {"status": "error", "message": f"File not found: {file_path}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def open_url(self, url: str) -> Dict[str, Any]:
        """
        Open a URL in default browser.
        
        Args:
            url: URL to open
            
        Returns:
            Dictionary with status and message
        """
        try:
            os.startfile(url)
            return {"status": "success", "message": f"Opened {url}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def execute_command(self, command: str) -> Dict[str, Any]:
        """
        Execute a shell command.
        
        Args:
            command: Command to execute
            
        Returns:
            Dictionary with status and output
        """
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True, timeout=10)
            return {
                "status": "success",
                "output": result.stdout,
                "error": result.stderr if result.stderr else None
            }
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Command timed out"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_tools_description(self) -> List[Dict[str, Any]]:
        """Get description of available tools for LLM function calling."""
        return [
            {
                "name": "launch_application",
                "description": "Launch an application by name (e.g., 'Spotify', 'VS Code', 'Chrome')",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "app_name": {"type": "string", "description": "Name of the application to launch"}
                    },
                    "required": ["app_name"]
                }
            },
            {
                "name": "close_application",
                "description": "Close a running application by name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "app_name": {"type": "string", "description": "Name of the application to close"}
                    },
                    "required": ["app_name"]
                }
            },
            {
                "name": "get_running_applications",
                "description": "Get list of currently running applications",
                "parameters": {"type": "object", "properties": {}}
            },
            {
                "name": "get_system_info",
                "description": "Get system performance information (CPU, memory, disk usage)",
                "parameters": {"type": "object", "properties": {}}
            },
            {
                "name": "set_volume",
                "description": "Set system volume level",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "level": {"type": "integer", "description": "Volume level (0-100)"}
                    },
                    "required": ["level"]
                }
            },
            {
                "name": "open_file",
                "description": "Open a file with its default application",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Full path to the file"}
                    },
                    "required": ["file_path"]
                }
            },
            {
                "name": "open_url",
                "description": "Open a URL in the default browser",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "URL to open"}
                    },
                    "required": ["url"]
                }
            },
            {
                "name": "execute_command",
                "description": "Execute a shell command",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Command to execute"}
                    },
                    "required": ["command"]
                }
            }
        ]

# Global instance
os_commands = OSCommands()
