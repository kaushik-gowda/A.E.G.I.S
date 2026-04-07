# A.E.G.I.S - Autonomous Execution & Guidance Intelligent System

A sophisticated desktop AI assistant for Windows that controls your operating system, manages daily tasks, and displays a sleek sci-fi interface on a secondary screen.

## 🚀 Features

- **Visual Interface**: Standalone PyQt6 GUI with A.E.G.I.S avatar on separate screen
- **OS Control**: Launch/close applications, manage files, control system settings
- **Task Management**: Create, list, and complete daily tasks
- **System Monitoring**: Real-time CPU, memory, and disk usage information
- **Smart Command Processing**: Natural language understanding for intuitive commands
- **Voice-Ready**: Infrastructure for speech-to-text and text-to-speech integration
- **Extensible Architecture**: Easy to add new commands and integrations

## 📋 Requirements

- Windows 10/11
- Python 3.10+
- PyQt6 for the GUI
- Optional: Secondary monitor for dedicated A.E.G.I.S display

## 🔧 Installation

### 1. Clone/Download the Project
```bash
cd e:\A.E.G.I.S
```

### 2. Create Virtual Environment
```powershell
python -m venv venv
```

### 3. Install Dependencies
```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Or manually install:
```powershell
.\venv\Scripts\python.exe -m pip install PyQt6 psutil requests python-dotenv SpeechRecognition pyttsx3 edge-tts pydub Pillow aiohttp
```

## 🎯 Quick Start

### Run A.E.G.I.S
```powershell
cd e:\A.E.G.I.S
.\venv\Scripts\python.exe main.py
```

The A.E.G.I.S window will appear on:
- **Dual Monitor Setup**: Secondary monitor (full screen)
- **Single Monitor**: Right side of primary monitor

## 💬 Available Commands

### Application Control
- `Launch Spotify` - Open Spotify
- `Open VS Code` - Launch Visual Studio Code
- `Open Chrome` - Launch Chrome browser
- `Close Spotify` - Close an application
- `List applications` - Show running apps

### System Information
- `System info` - Get CPU, memory, disk usage
- `What's my system status?` - Display system metrics

### Task Management
- `Add task Do laundry` - Create a new task
- `List tasks` - Show all pending tasks
- `Complete task 0` - Mark task as done
- `Show my tasks` - Display current tasks

### Volume Control
- `Set volume to 50` - Set system volume
- `Volume 100` - Maximize volume

### Information
- `Hello` - Greeting
- `Help` - Show available commands
- `What time is it?` - Current time
- `What date is it?` - Current date

## 📁 Project Structure

```
A.E.G.I.S/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── venv/                  # Virtual environment
├── src/
│   ├── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── app_window.py  # PyQt6 UI components
│   ├── core/
│   │   ├── __init__.py
│   │   └── agent.py       # AI agent logic & task manager
│   └── tools/
│       ├── __init__.py
│       └── os_commands.py # Windows system automation
├── assets/                # Placeholder for images/avatars
└── data/                  # Task storage (JSON)
```

## 🔌 Extending A.E.G.I.S

### Add a New OS Command

Edit `src/tools/os_commands.py`:
```python
def new_feature(self, param: str) -> Dict[str, Any]:
    """Your new feature implementation."""
    try:
        # Implementation here
        return {"status": "success", "message": "Success!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_tools_description(self) -> List[Dict[str, Any]]:
    # Add to the list:
    {
        "name": "new_feature",
        "description": "Description of your feature",
        "parameters": {...}
    }
```

### Add a New Command Handler

Edit `src/core/agent.py` in the `_handle_command` method:
```python
elif any(word in command_lower for word in ["keyword1", "keyword2"]):
    return self._handle_your_feature(command)

def _handle_your_feature(self, command: str) -> str:
    """Add your implementation here."""
    return "Response here"
```

## 🎨 UI Customization

### Change A.E.G.I.S Avatar
Currently displaying a green circle with "A.E.G.I.S" text. To use a custom image:

1. Place your image in `assets/` folder
2. Edit `src/ui/app_window.py`:
```python
pixmap = QPixmap("assets/your_image.png")
avatar_label.setPixmap(pixmap.scaled(200, 200))
```

### Customize Colors
Main colors are controlled in `app_window.py`:
- Primary Green: `#00ff41`
- Dark Background: `#0a0a0a`, `#1a1a1a`
- Accent Green: `#00aa00`

## 🔮 Advanced Features (Future Enhancements)

1. **Voice Integration**
   - Speech-to-text for hands-free commands
   - Text-to-speech for A.E.G.I.S responses

2. **Cloud LLM Integration**
   - Support for OpenAI GPT-4
   - Local Ollama for privacy

3. **Advanced Task Management**
   - Scheduled reminders
   - Task prioritization
   - Recurring tasks

4. **System Customization**
   - Brightness control
   - Network management
   - Window management

5. **Authentication**
   - User profiles
   - Command permissions
   - Activity logging

## 🐛 Troubleshooting

### PyQt6 Not Loading
```powershell
.\venv\Scripts\python.exe -m pip install --upgrade PyQt6
```

### Import Errors
```powershell
# Reinstall all dependencies
.\venv\Scripts\python.exe -m pip install --force-reinstall -r requirements.txt
```

### Window Not Appearing
- Ensure both monitors are connected and configured
- Check that PyQt6 OpenGL support is available
- Try running in windowed mode first

## 📝 Notes

- Tasks are stored locally in `data/tasks.json`
- Conversation history limited to 20 recent exchanges
- All system commands run with user privileges

## 📞 Support

For issues or improvements:
1. Check the troubleshooting section
2. Review the command list
3. Check `data/` and logs for error messages

## 🎓 Learning Resources

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Windows Automation with Python](https://docs.python.org/3/library/subprocess.html)
- [System Information with psutil](https://psutil.readthedocs.io/)

---

**Version**: 1.0.0  
**Last Updated**: April 7, 2026  
**Author**: Your Name
