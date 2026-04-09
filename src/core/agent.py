# Core A.E.G.I.S (Autonomous Execution & Guidance Intelligent System) Agent Module
# Handles AI logic, task management, and command processing

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
import threading
import requests
from enum import Enum

# Import OS tools
from tools.os_commands import os_commands
from tools.app_discovery import app_discovery
from tools.system_control import system_control
from tools.voice_input import voice_system

class CommandType(Enum):
    """Types of commands the agent can process."""
    SYSTEM_CONTROL = "system_control"
    TASK_MANAGEMENT = "task_management"
    QUERY = "query"
    GENERAL = "general"

class TaskManager:
    """Manages daily tasks and reminders."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize task manager."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.tasks_file = self.data_dir / "tasks.json"
        self.tasks = self.load_tasks()
    
    def load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from file."""
        if self.tasks_file.exists():
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_tasks(self):
        """Save tasks to file."""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, title: str, description: str = "", priority: str = "medium") -> Dict[str, Any]:
        """Add a new task."""
        task = {
            "id": len(self.tasks),
            "title": title,
            "description": description,
            "priority": priority,
            "created": datetime.now().isoformat(),
            "completed": False
        }
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_tasks(self, filter_completed: bool = False) -> List[Dict[str, Any]]:
        """Get tasks, optionally filtered by completion status."""
        if filter_completed:
            return [t for t in self.tasks if not t.get('completed', False)]
        return self.tasks
    
    def complete_task(self, task_id: int) -> bool:
        """Mark task as completed."""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                self.save_tasks()
                return True
        return False

class PromptTemplate:
    """System prompt for A.E.G.I.S agent."""
    
    SYSTEM_PROMPT = """You are A.E.G.I.S (Autonomous Execution & Guidance Intelligent System), 
an advanced desktop AI assistant designed to control and manage Windows operating systems.

Your capabilities include:
1. Launching and closing applications
2. Getting system information (CPU, memory, disk usage)
3. Opening files and URLs
4. Managing tasks and reminders
5. Executing system commands
6. Controlling system settings (volume, etc.)

When the user makes a request:
- If it requires system action, call the appropriate tool
- Provide clear, concise responses
- Always confirm actions taken
- If something fails, explain the error clearly

Be helpful, efficient, and always maintain a professional tone."""

class AegisAgent:
    """Main A.E.G.I.S AI Agent."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the A.E.G.I.S agent.
        
        Args:
            data_dir: Directory for storing agent data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.task_manager = TaskManager(data_dir)
        self.os_commands = os_commands
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history = 20
        
        # Response callback (set by UI)
        self.response_callback: Optional[Callable] = None
        
        # API Configuration (can use local or cloud LLM)
        # For now, we'll use a simple rule-based system
        self.use_ollama = False  # Set to True to use Ollama
        self.ollama_url = "http://localhost:11434"
        self.model = "mistral"  # or "llama2", "neural-chat", etc.
    
    def process_command(self, command: str, callback: Optional[Callable] = None):
        """
        Process a command from the user.
        
        Args:
            command: User's command/query
            callback: Callback function to send response back to UI
        """
        self.response_callback = callback
        
        # Run in separate thread to avoid blocking UI
        thread = threading.Thread(target=self._process_command_thread, args=(command,))
        thread.daemon = True
        thread.start()
    
    def _process_command_thread(self, command: str):
        """Process command in background thread."""
        # Add to history
        self.conversation_history.append({"role": "user", "content": command})
        
        # Keep history size manageable
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
        
        try:
            # Determine command type and handle
            response = self._handle_command(command)
        except Exception as e:
            response = f"Error processing command: {str(e)}"
        
        # Add response to history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        # Send response back to UI
        if self.response_callback:
            self.response_callback(response)
    
    def _handle_command(self, command: str) -> str:
        """
        Handle a command and return response.
        
        Args:
            command: User's command
            
        Returns:
            Response string
        """
        command_lower = command.lower()
        
        # Extract intent
        if any(word in command_lower for word in ["launch", "open", "start", "run"]):
            return self._handle_launch_app(command)
        
        elif any(word in command_lower for word in ["close", "quit", "exit", "shut"]):
            return self._handle_close_app(command)
        
        elif any(word in command_lower for word in ["system", "info", "status", "performance"]):
            return self._handle_system_status(command)
        
        elif any(word in command_lower for word in ["task", "todo", "reminder"]):
            return self._handle_task_management(command)
        
        elif any(word in command_lower for word in ["open url", "browse", "visit", "go to"]):
            return self._handle_open_url(command)
        
        elif any(word in command_lower for word in ["open file", "file", "document"]):
            return self._handle_open_file(command)
        
        elif any(word in command_lower for word in ["volume", "sound", "audio"]):
            return self._handle_volume_control(command)
        
        elif any(word in command_lower for word in ["running", "processes", "applications"]):
            return self._handle_list_apps(command)
        
        elif any(word in command_lower for word in ["voice", "listen", "activate voice"]):
            return self._handle_voice_control(command)
        
        elif any(word in command_lower for word in ["settings", "config", "preferences", "options"]):
            return self._handle_settings(command)
        
        elif any(word in command_lower for word in ["shutdown", "power off", "turn off"]):
            return self._handle_shutdown(command)
        
        elif any(word in command_lower for word in ["restart", "reboot"]):
            return self._handle_restart(command)
        
        elif any(word in command_lower for word in ["sleep", "hibernate"]):
            return self._handle_sleep(command)
        
        elif any(word in command_lower for word in ["lock", "lock screen"]):
            return self._handle_lock(command)
        
        elif any(word in command_lower for word in ["find app", "search app", "app list"]):
            return self._handle_find_app(command)
        
        else:
            return self._handle_general_query(command)
    
    def _handle_launch_app(self, command: str) -> str:
        """Handle application launch commands."""
        # Extract app name from command
        apps = ["spotify", "vscode", "chrome", "firefox", "notepad", "calculator", "explorer"]
        app_to_launch = None
        
        for app in apps:
            if app in command.lower():
                app_to_launch = app
                break
        
        if not app_to_launch:
            return "I couldn't identify which application to launch. Please specify an app name (e.g., Spotify, VS Code, Chrome)."
        
        result = self.os_commands.launch_application(app_to_launch)
        if result["status"] == "success":
            return f"✓ Successfully launched {app_to_launch.title()}"
        else:
            return f"✗ Failed to launch {app_to_launch}: {result['message']}"
    
    def _handle_close_app(self, command: str) -> str:
        """Handle application close commands."""
        apps = ["spotify", "vscode", "chrome", "firefox", "notepad", "calculator", "explorer"]
        app_to_close = None
        
        for app in apps:
            if app in command.lower():
                app_to_close = app
                break
        
        if not app_to_close:
            return "I couldn't identify which application to close. Please specify an app name."
        
        result = self.os_commands.close_application(app_to_close)
        if result["status"] == "success":
            return f"✓ Successfully closed {app_to_close.title()}"
        else:
            return f"✗ Failed to close {app_to_close}: {result['message']}"
    
    def _handle_system_status(self, command: str) -> str:
        """Handle system information requests."""
        result = self.os_commands.get_system_info()
        if result["status"] == "success":
            return f"""
System Status:
├─ CPU Usage: {result['cpu_usage']:.1f}%
├─ Memory Usage: {result['memory_usage']:.1f}%
├─ Available RAM: {result['memory_available_gb']:.2f} GB
└─ Disk Usage: {result['disk_usage']:.1f}%
"""
        else:
            return f"Failed to get system status: {result['message']}"
    
    def _handle_list_apps(self, command: str) -> str:
        """Handle list running applications."""
        result = self.os_commands.get_running_applications()
        if result["status"] == "success":
            processes = result["processes"][:10]  # Show top 10
            apps_list = "\n".join([f"• {proc}" for proc in processes])
            return f"Running applications:\n{apps_list}"
        else:
            return f"Failed to get running applications: {result['message']}"
    
    def _handle_task_management(self, command: str) -> str:
        """Handle task management commands."""
        if "add" in command.lower() or "create" in command.lower():
            # Extract task title
            task_title = command.replace("add", "").replace("task", "").replace("create", "").strip()
            if not task_title:
                task_title = "New Task"
            
            task = self.task_manager.add_task(task_title)
            return f"✓ Task added: '{task['title']}' (ID: {task['id']})"
        
        elif "list" in command.lower() or "show" in command.lower():
            tasks = self.task_manager.get_tasks(filter_completed=True)
            if not tasks:
                return "No pending tasks."
            
            tasks_list = "\n".join([f"[{t['id']}] {t['title']} ({t.get('priority', 'normal')})" for t in tasks])
            return f"Your tasks:\n{tasks_list}"
        
        elif "complete" in command.lower() or "done" in command.lower():
            # Try to extract task ID
            import re
            ids = re.findall(r'\d+', command)
            if ids:
                task_id = int(ids[0])
                if self.task_manager.complete_task(task_id):
                    return f"✓ Task {task_id} marked as completed"
                else:
                    return f"✗ Task {task_id} not found"
            else:
                return "Please specify a task ID to complete"
        
        else:
            return "Task management options: add [task], list tasks, complete [task ID]"
    
    def _handle_open_url(self, command: str) -> str:
        """Handle URL opening commands."""
        # Simple URL extraction
        import re
        urls = re.findall(r'http[s]?://\S+', command)
        if urls:
            url = urls[0]
            result = self.os_commands.open_url(url)
            if result["status"] == "success":
                return f"✓ Opened URL: {url}"
            else:
                return f"✗ Failed to open URL: {result['message']}"
        else:
            return "No URL found in command. Please provide a URL (e.g., https://google.com)"
    
    def _handle_open_file(self, command: str) -> str:
        """Handle file opening commands."""
        # This would need more sophisticated parsing
        return "File opening requires full file path. Please specify the complete path."
    
    def _handle_volume_control(self, command: str) -> str:
        """Handle volume control commands."""
        import re
        numbers = re.findall(r'\d+', command)
        if numbers:
            volume = int(numbers[0])
            result = self.os_commands.set_volume(volume)
            if result["status"] == "success":
                return f"✓ Volume set to {volume}%"
            else:
                return f"✗ Failed to set volume: {result['message']}"
        else:
            return "Please specify a volume level (0-100)"
    
    def _handle_general_query(self, command: str) -> str:
        """Handle general queries."""
        responses = {
            "hello": "Hello! I'm A.E.G.I.S (Autonomous Execution & Guidance Intelligent System), your desktop AI assistant. How can I help?",
            "help": """Available Commands:
🚀 Applications:
  • Launch [app name] - Open any application
  • Close [app] - Close an application
  • List applications - Show running apps
  
💻 System Control:
  • System info - Performance stats
  • Settings [section] - Open Windows Settings
  • Control panel - Open Control Panel
  • Task Manager - Open Task Manager
  • Device Manager - Open Device Manager
  
⚡ Power Commands:
  • Shutdown - Shutdown system
  • Restart - Restart system
  • Sleep - Put to sleep
  • Lock screen - Lock Windows
  
📋 Tasks:
  • Add task [name] - Create task
  • List tasks - Show tasks
  • Complete task [id] - Mark done
  
🔊 System:
  • Set volume [0-100] - Control volume
  • Brightness [0-100] - Change brightness
  • Disk info - Show disk usage
  
🎤 Voice:
  • Activate voice - Start voice mode
  • Stop listening - Stop voice mode
  
❓ Info:
  • Who are you? - System info
  • What time is it? - Current time
  • What date is it? - Current date""",
            "who are you": "I'm A.E.G.I.S - Autonomous Execution & Guidance Intelligent System. I'm designed to give you complete control of your Windows desktop and manage your daily tasks.",
            "time": datetime.now().strftime("Current time: %H:%M:%S"),
            "date": datetime.now().strftime("Current date: %Y-%m-%d"),
        }
        
        for key, response in responses.items():
            if key in command.lower():
                return response
        
        return f"I understand you said: '{command}'. I'm still learning about this topic. Try asking me to launch an app, check system status, or manage tasks."
    
    def _handle_voice_control(self, command: str) -> str:
        """Handle voice activation control."""
        if "stop" in command.lower() or "disable" in command.lower():
            voice_system.stop_listening()
            return "✓ Voice activation stopped"
        else:
            voice_system.start_listening(self.on_voice_command)
            return "✓ Voice activation started. Say 'Hey Aegis' followed by your command"
    
    def on_voice_command(self, command: str):
        """Handle voice commands from voice system."""
        if self.response_callback:
            self.process_command(command, self.response_callback)
    
    def _handle_settings(self, command: str) -> str:
        """Handle settings and control panel commands."""
        keywords = {
            "display": "display",
            "sound": "sound",
            "network": "network",
            "bluetooth": "bluetooth",
            "keyboard": "keyboard",
            "mouse": "mouse",
            "power": "power",
            "update": "update",
            "privacy": "privacy",
        }
        
        section = None
        for key, value in keywords.items():
            if key in command.lower():
                section = value
                break
        
        result = system_control.open_settings(section)
        return f"✓ {result['message']}"
    
    def _handle_shutdown(self, command: str) -> str:
        """Handle shutdown commands."""
        import re
        numbers = re.findall(r'\d+', command)
        delay = int(numbers[0]) if numbers else 0
        
        result = system_control.shutdown(delay)
        if result["status"] == "success":
            return f"⚠ {result['message']}"
        else:
            return f"✗ {result['message']}"
    
    def _handle_restart(self, command: str) -> str:
        """Handle restart commands."""
        import re
        numbers = re.findall(r'\d+', command)
        delay = int(numbers[0]) if numbers else 0
        
        result = system_control.restart(delay)
        if result["status"] == "success":
            return f"⚠ {result['message']}"
        else:
            return f"✗ {result['message']}"
    
    def _handle_sleep(self, command: str) -> str:
        """Handle sleep commands."""
        result = system_control.sleep()
        if result["status"] == "success":
            return f"✓ {result['message']}"
        else:
            return f"✗ {result['message']}"
    
    def _handle_lock(self, command: str) -> str:
        """Handle screen lock commands."""
        result = system_control.lock_screen()
        if result["status"] == "success":
            return f"✓ {result['message']}"
        else:
            return f"✗ {result['message']}"
    
    def _handle_find_app(self, command: str) -> str:
        """Handle app discovery and launching."""
        # Extract app name
        app_name = command.replace("find app", "").replace("search app", "").replace("launch", "").strip()
        
        if not app_name:
            count = app_discovery.get_app_count()
            return f"✓ {count} applications available. Specify an app name to launch (e.g., 'Launch Chrome')"
        
        # Try to launch the app
        result = app_discovery.launch_app(app_name)
        if result["status"] == "success":
            return f"✓ {result['message']}"
        else:
            # Try to find similar apps
            similar_apps = app_discovery.list_apps(app_name)
            if similar_apps:
                app_list = "\n".join([f"• {app['name']}" for app in similar_apps[:5]])
                return f"Did you mean one of these?\n{app_list}"
            else:
                return f"✗ Application '{app_name}' not found"
    
    def get_conversation_context(self) -> str:
        """Get recent conversation context for LLM."""
        context = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in self.conversation_history[-5:]
        ])
        return context
