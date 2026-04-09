# Application Discovery Module for A.E.G.I.S
# Dynamically discovers all installed applications on the system

import os
import sys
import subprocess
import winreg
from pathlib import Path
from typing import List, Dict, Any, Set
import json

class AppDiscoverySystem:
    """Discovers and manages all installed applications on Windows."""
    
    def __init__(self):
        """Initialize app discovery system."""
        self.apps = {}
        self.app_cache_file = Path("data/apps_cache.json")
        self.load_or_discover_apps()
    
    def load_or_discover_apps(self):
        """Load apps from cache or discover them."""
        if self.app_cache_file.exists():
            try:
                with open(self.app_cache_file, 'r') as f:
                    self.apps = json.load(f)
                return
            except:
                pass
        
        # Discover apps
        self.discover_all_apps()
        self.cache_apps()
    
    def discover_all_apps(self):
        """Discover all installed applications."""
        self.apps = {}
        
        # Get apps from Program Files
        self._scan_program_files()
        
        # Get apps from Windows Registry
        self._scan_registry()
        
        # Get common system applications
        self._add_system_apps()
    
    def _scan_program_files(self):
        """Scan Program Files directories."""
        program_files = [
            os.path.expandvars(r'%ProgramFiles%'),
            os.path.expandvars(r'%ProgramFiles(x86)%'),
            os.path.expandvars(r'%ProgramW6432%'),
        ]
        
        for base_path in program_files:
            if not os.path.exists(base_path):
                continue
            
            try:
                for item in os.listdir(base_path):
                    item_path = os.path.join(base_path, item)
                    if os.path.isdir(item_path):
                        # Look for executables
                        for root, dirs, files in os.walk(item_path):
                            for file in files:
                                if file.endswith('.exe'):
                                    exe_path = os.path.join(root, file)
                                    app_name = os.path.splitext(file)[0]
                                    
                                    # Store with lowercase name as key
                                    key = app_name.lower().replace(' ', '')
                                    if key not in self.apps:
                                        self.apps[key] = {
                                            'name': app_name,
                                            'path': exe_path,
                                            'source': 'program_files'
                                        }
                            break  # Only check first level
            except PermissionError:
                pass
    
    def _scan_registry(self):
        """Scan Windows Registry for installed applications."""
        registry_paths = [
            r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
            r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall',
        ]
        
        try:
            for reg_path in registry_paths:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            try:
                                subkey_name = winreg.EnumKey(key, i)
                                with winreg.OpenKey(key, subkey_name) as subkey:
                                    try:
                                        display_name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                                        install_location = winreg.QueryValueEx(subkey, 'InstallLocation')[0]
                                        
                                        if display_name and install_location:
                                            key_name = display_name.lower().replace(' ', '')
                                            if key_name not in self.apps:
                                                self.apps[key_name] = {
                                                    'name': display_name,
                                                    'path': install_location,
                                                    'source': 'registry'
                                                }
                                    except:
                                        pass
                            except:
                                pass
                except:
                    pass
        except:
            pass
    
    def _add_system_apps(self):
        """Add common system applications."""
        system_apps = {
            'notepad': {'name': 'Notepad', 'path': 'notepad.exe', 'source': 'system'},
            'calculator': {'name': 'Calculator', 'path': 'calc.exe', 'source': 'system'},
            'wordpad': {'name': 'WordPad', 'path': 'wordpad.exe', 'source': 'system'},
            'paint': {'name': 'Paint', 'path': 'mspaint.exe', 'source': 'system'},
            'camera': {'name': 'Camera', 'path': 'cameracapture.exe', 'source': 'system'},
            'settings': {'name': 'Settings', 'path': 'ms-settings:', 'source': 'system'},
            'powershell': {'name': 'PowerShell', 'path': 'powershell.exe', 'source': 'system'},
            'cmd': {'name': 'Command Prompt', 'path': 'cmd.exe', 'source': 'system'},
            'explorer': {'name': 'File Explorer', 'path': 'explorer.exe', 'source': 'system'},
            'taskmgr': {'name': 'Task Manager', 'path': 'taskmgr.exe', 'source': 'system'},
            'devmgmt': {'name': 'Device Manager', 'path': 'devmgmt.msc', 'source': 'system'},
            'services': {'name': 'Services', 'path': 'services.msc', 'source': 'system'},
            'msconfig': {'name': 'System Configuration', 'path': 'msconfig.exe', 'source': 'system'},
            'control': {'name': 'Control Panel', 'path': 'control.exe', 'source': 'system'},
        }
        
        for key, app in system_apps.items():
            if key not in self.apps:
                self.apps[key] = app
    
    def cache_apps(self):
        """Cache discovered apps to JSON file."""
        try:
            Path("data").mkdir(exist_ok=True)
            with open(self.app_cache_file, 'w') as f:
                json.dump(self.apps, f, indent=2)
        except:
            pass
    
    def find_app(self, app_name: str) -> Dict[str, Any]:
        """
        Find an application by name.
        
        Args:
            app_name: Name of application to find
            
        Returns:
            App info dict or None
        """
        key = app_name.lower().replace(' ', '')
        if key in self.apps:
            return self.apps[key]
        
        # Try fuzzy matching
        for k, v in self.apps.items():
            if app_name.lower() in v['name'].lower() or app_name.lower() in k:
                return v
        
        return None
    
    def list_apps(self, pattern: str = None) -> List[Dict[str, Any]]:
        """
        List applications, optionally filtered.
        
        Args:
            pattern: Optional filter pattern
            
        Returns:
            List of app dicts
        """
        apps = list(self.apps.values())
        
        if pattern:
            pattern_lower = pattern.lower()
            apps = [a for a in apps if pattern_lower in a['name'].lower()]
        
        # Sort by name
        apps.sort(key=lambda x: x['name'])
        return apps
    
    def launch_app(self, app_name: str) -> Dict[str, Any]:
        """
        Launch an application.
        
        Args:
            app_name: Name of application to launch
            
        Returns:
            Status dict
        """
        app = self.find_app(app_name)
        
        if not app:
            return {"status": "error", "message": f"Application '{app_name}' not found"}
        
        try:
            path = app['path']
            
            # Handle ms-settings: URLs
            if path.startswith('ms-'):
                os.startfile(path)
            else:
                os.startfile(path)
            
            return {"status": "success", "message": f"Launched {app['name']}"}
        
        except Exception as e:
            return {"status": "error", "message": f"Failed to launch: {str(e)}"}
    
    def get_app_count(self) -> int:
        """Get total number of discovered apps."""
        return len(self.apps)
    
    def refresh_cache(self):
        """Refresh application cache."""
        self.discover_all_apps()
        self.cache_apps()
        return {"status": "success", "message": f"Discovered {len(self.apps)} applications"}

# Global instance
app_discovery = AppDiscoverySystem()
