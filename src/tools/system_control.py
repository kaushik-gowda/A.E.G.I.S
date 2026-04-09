# Enhanced System Control Module for A.E.G.I.S
# Advanced system control and settings management

import subprocess
import os
import psutil
import time
import ctypes
import winreg
from typing import Dict, Any, List

class SystemControlManager:
    """Advanced system control and management."""
    
    def __init__(self):
        """Initialize system control manager."""
        self.admin_required = ["shutdown", "restart", "screen_off"]
    
    # System Power Management
    
    def shutdown(self, delay_seconds: int = 0) -> Dict[str, Any]:
        """
        Shutdown the computer.
        
        Args:
            delay_seconds: Delay before shutdown
            
        Returns:
            Status dict
        """
        try:
            if delay_seconds > 0:
                cmd = f"shutdown /s /t {delay_seconds}"
            else:
                cmd = "shutdown /s /t 0"
            
            os.system(cmd)
            return {"status": "success", "message": f"Shutdown initiated (delay: {delay_seconds}s)"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def restart(self, delay_seconds: int = 0) -> Dict[str, Any]:
        """
        Restart the computer.
        
        Args:
            delay_seconds: Delay before restart
            
        Returns:
            Status dict
        """
        try:
            if delay_seconds > 0:
                cmd = f"shutdown /r /t {delay_seconds}"
            else:
                cmd = "shutdown /r /t 0"
            
            os.system(cmd)
            return {"status": "success", "message": f"Restart initiated (delay: {delay_seconds}s)"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def sleep(self) -> Dict[str, Any]:
        """Put computer to sleep."""
        try:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return {"status": "success", "message": "System going to sleep"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def lock_screen(self) -> Dict[str, Any]:
        """Lock the screen."""
        try:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return {"status": "success", "message": "Screen locked"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def screen_off(self) -> Dict[str, Any]:
        """Turn off the screen."""
        try:
            os.system("nircmd sendkey lwin+x")
            time.sleep(0.5)
            os.system("nircmd sendkey u u")
            return {"status": "success", "message": "Screen turning off"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # Display & Brightness
    
    def set_brightness(self, level: int) -> Dict[str, Any]:
        """
        Set screen brightness (0-100).
        
        Args:
            level: Brightness level
            
        Returns:
            Status dict
        """
        try:
            level = max(0, min(100, level))
            # Using WMI for brightness
            cmd = f"wmic path winmotorola_monitorbrightnessmethods call WmiSetBrightness instance='\\\\.\\DISPLAY1' currentbrightness={level}"
            os.system(cmd)
            return {"status": "success", "message": f"Brightness set to {level}%"}
        except Exception as e:
            return {"status": "error", "message": "Brightness control not available"}
    
    # Network Management
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get network information."""
        try:
            interfaces = psutil.net_if_addrs()
            net_info = {}
            
            for interface, addresses in interfaces.items():
                net_info[interface] = []
                for addr in addresses:
                    net_info[interface].append({
                        'family': str(addr.family),
                        'address': addr.address,
                        'broadcast': addr.broadcast
                    })
            
            return {"status": "success", "networks": len(interfaces), "data": net_info}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_internet_speed(self) -> Dict[str, Any]:
        """Get internet connection status."""
        try:
            # Simple ping test
            result = subprocess.run(['ping', '-n', '1', 'google.com'], 
                                  capture_output=True, timeout=5)
            
            if result.returncode == 0:
                return {"status": "success", "internet": "Connected", "provider": "Google DNS"}
            else:
                return {"status": "offline", "internet": "Disconnected"}
        except:
            return {"status": "error", "message": "Could not determine internet status"}
    
    # Process Management
    
    def kill_process(self, process_name: str) -> Dict[str, Any]:
        """
        Kill a process by name.
        
        Args:
            process_name: Name of process to kill
            
        Returns:
            Status dict
        """
        try:
            os.system(f"taskkill /IM {process_name} /F")
            return {"status": "success", "message": f"Process {process_name} terminated"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_top_processes(self, count: int = 10) -> Dict[str, Any]:
        """
        Get top processes by CPU/memory usage.
        
        Args:
            count: Number of processes to return
            
        Returns:
            List of process info
        """
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            return {"status": "success", "processes": processes[:count]}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # Settings & Control Panel
    
    def open_settings(self, section: str = None) -> Dict[str, Any]:
        """
        Open Windows Settings.
        
        Args:
            section: Specific settings section to open
            
        Returns:
            Status dict
        """
        try:
            settings_paths = {
                'display': 'ms-settings:display',
                'sound': 'ms-settings:sound',
                'network': 'ms-settings:network',
                'devices': 'ms-settings:devices',
                'system': 'ms-settings:system',
                'privacy': 'ms-settings:privacy',
                'update': 'ms-settings:windowsupdate',
                'power': 'ms-settings:powersleep',
                'bluetooth': 'ms-settings:bluetooth',
                'keyboard': 'ms-settings:keyboard',
                'mouse': 'ms-settings:mouse',
                'about': 'ms-settings:about',
            }
            
            if section and section.lower() in settings_paths:
                path = settings_paths[section.lower()]
            else:
                path = 'ms-settings:'
            
            os.startfile(path)
            return {"status": "success", "message": f"Opened Settings: {section or 'Main'}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def open_control_panel(self, section: str = None) -> Dict[str, Any]:
        """
        Open Windows Control Panel.
        
        Args:
            section: Specific control panel section
            
        Returns:
            Status dict
        """
        try:
            control_sections = {
                'network': 'ncpa.cpl',
                'sound': 'mmsys.cpl',
                'keyboard': 'main.cpl',
                'mouse': 'main.cpl',
                'display': 'desk.cpl',
                'date': 'timedate.cpl',
                'devices': 'hdwwiz.cpl',
                'system': 'sysdm.cpl',
                'power': 'powercfg.cpl',
            }
            
            if section and section.lower() in control_sections:
                cpl = control_sections[section.lower()]
                os.system(f"control {cpl}")
            else:
                os.system("control.exe")
            
            return {"status": "success", "message": f"Opened Control Panel: {section or 'Main'}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def open_task_manager(self) -> Dict[str, Any]:
        """Open Windows Task Manager."""
        try:
            os.system("taskmgr.exe")
            return {"status": "success", "message": "Task Manager opened"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def open_device_manager(self) -> Dict[str, Any]:
        """Open Windows Device Manager."""
        try:
            os.system("devmgmt.msc")
            return {"status": "success", "message": "Device Manager opened"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # System Information
    
    def get_detailed_system_info(self) -> Dict[str, Any]:
        """Get detailed system information."""
        try:
            import platform
            
            return {
                "status": "success",
                "os": platform.system(),
                "os_version": platform.release(),
                "processor": platform.processor(),
                "machine": platform.machine(),
                "python_version": platform.python_version(),
                "total_memory_gb": psutil.virtual_memory().total / (1024**3),
                "cpu_cores": psutil.cpu_count(),
                "cpu_freq_ghz": psutil.cpu_freq().current / 1000,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_disk_info(self) -> Dict[str, Any]:
        """Get disk information for all partitions."""
        try:
            disks = {}
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks[partition.device] = {
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total_gb": usage.total / (1024**3),
                        "used_gb": usage.used / (1024**3),
                        "free_gb": usage.free / (1024**3),
                        "percent": usage.percent,
                    }
                except PermissionError:
                    pass
            
            return {"status": "success", "disks": disks}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_tools_description(self) -> List[Dict[str, Any]]:
        """Get description of available system control tools for LLM."""
        return [
            {
                "name": "shutdown",
                "description": "Shutdown the computer",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "delay_seconds": {"type": "integer", "description": "Delay before shutdown (optional)"}
                    }
                }
            },
            {
                "name": "restart",
                "description": "Restart the computer",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "delay_seconds": {"type": "integer", "description": "Delay before restart (optional)"}
                    }
                }
            },
            {
                "name": "sleep",
                "description": "Put computer to sleep",
                "parameters": {"type": "object", "properties": {}}
            },
            {
                "name": "lock_screen",
                "description": "Lock the Windows screen",
                "parameters": {"type": "object", "properties": {}}
            },
            {
                "name": "open_settings",
                "description": "Open Windows Settings (optionally specific section)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "section": {"type": "string", "description": "Settings section (display, sound, network, etc)"}
                    }
                }
            },
            {
                "name": "open_control_panel",
                "description": "Open Windows Control Panel",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "section": {"type": "string", "description": "Control panel section"}
                    }
                }
            },
            {
                "name": "get_detailed_system_info",
                "description": "Get detailed system information",
                "parameters": {"type": "object", "properties": {}}
            },
            {
                "name": "get_disk_info",
                "description": "Get disk information for all partitions",
                "parameters": {"type": "object", "properties": {}}
            },
            {
                "name": "get_top_processes",
                "description": "Get top processes by CPU/memory usage",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer", "description": "Number of processes to show"}
                    }
                }
            },
            {
                "name": "kill_process",
                "description": "Terminate a process by name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "process_name": {"type": "string", "description": "Process name (e.g., notepad.exe)"}
                    },
                    "required": ["process_name"]
                }
            },
            {
                "name": "open_task_manager",
                "description": "Open Windows Task Manager",
                "parameters": {"type": "object", "properties": {}}
            },
            {
                "name": "open_device_manager",
                "description": "Open Windows Device Manager",
                "parameters": {"type": "object", "properties": {}}
            },
        ]

# Global instance
system_control = SystemControlManager()
