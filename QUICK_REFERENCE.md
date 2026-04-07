# A.E.G.I.S (Autonomous Execution & Guidance Intelligent System) Quick Reference

## 🚀 Quick Start

```powershell
cd e:\A.E.G.I.S
.\venv\Scripts\python.exe main.py
```

Or use the batch file:
```
run.bat
```

## 💬 Command Examples

### Launch Applications
```
"Launch Spotify"
"Open VS Code"
"Start Chrome"
"Run calculator"
```

### Close Applications  
```
"Close Spotify"
"Quit VS Code"
"Exit Chrome"
```

### System Information
```
"What's my system status?"
"System info"
"Show CPU usage"
"Check memory"
```

### Task Management
```
"Add task Remember to call mom"
"Show my tasks"
"List tasks"
"Complete task 1"
"Mark task 0 as done"
```

### Volume Control
```
"Set volume to 50"
"Volume 75"
"Mute" (set to 0)
"Full volume" (set to 100)
```

### Help & Information
```
"Hello"
"Help"
"Who are you?"
"What time is it?"
"What's the date?"
"What applications are running?"
```

## 🎨 UI Guide

### Left Panel (Avatar & Status)
- **A.E.G.I.S Avatar** (Autonomous Execution & Guidance Intelligent System): Central focus with glowing green aesthetic
- **Status Indicator**: Shows current system state
- **System Info**: Real-time performance metrics
- **Activity Light**: 🟢 Ready / 🔴 Processing
- **Time Display**: Current date and time
- **Action Buttons**: Clear chat history and voice input

### Right Panel (Command Center)
- **Title**: "COMMAND CENTER"
- **Chat Display**: Conversation history with color-coded messages
  - Green `#00ff41`: Your commands
  - Brighter green `#00aa00`: A.E.G.I.S responses
  - Orange `#ff6600`: System messages
- **Command Input**: Text field for entering commands
- **Execute Button**: Send command to A.E.G.I.S

## 📂 Project Structure

```
A.E.G.I.S/
├── main.py                 # Start here!
├── run.bat                 # Windows batch launcher
├── test_system.py          # Run diagnostics
├── requirements.txt        # Python dependencies
├── README.md               # Full documentation
├── SETUP.md                # Installation guide
├── assets/                 # Images and resources (future)
├── data/                   # Task storage (JSON)
│   └── tasks.json          # Your tasks
└── src/
    ├── ui/
    │   └── app_window.py   # PyQt6 interface
    ├── core/
    │   └── agent.py        # AI agent logic
    └── tools/
        └── os_commands.py  # System automation
```

## 🔧 Customization

### Add New Application to Known Apps
Edit `src/tools/os_commands.py`:
```python
self.known_apps = {
    "spotify": "spotify.exe",
    "vscode": "code.exe",
    # Add your app here:
    "myapp": "myapp.exe",
}
```

### Add New Command Handler
Edit `src/core/agent.py` in `_handle_command()`:
```python
elif any(word in command_lower for word in ["keyword"]):
    return self._handle_keyword(command)

def _handle_keyword(self, command: str) -> str:
    # Your implementation
    return "Response"
```

### Change UI Colors
Edit `src/ui/app_window.py`:
- `#00ff41` - Primary bright green
- `#00aa00` - Darker green accent
- `#0a0a0a` - Almost black background
- `#1a1a1a` - Dark gray panels

## ⌨️ Keyboard Shortcuts (In Application)

- `Enter` - Send command
- `Ctrl+L` - Clear chat (planned)
- `Alt+Tab` - Switch between windows

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| Window doesn't appear | Check secondary monitor, try Alt+Tab |
| "ModuleNotFoundError" | Run: `.\venv\Scripts\python.exe -m pip install -r requirements.txt` |
| Command not recognized | Check spelling and try simpler command |
| Application won't launch | Ensure app executable is in PATH or add to `known_apps` |
| Crashes on startup | Check Task Manager for conflicting processes |

## 📊 File Locations

- **Tasks stored**: `data/tasks.json`
- **Python executable**: `venv\Scripts\python.exe`
- **Configuration**: `src/core/agent.py` (rule-based prompts)

## 🎓 Learning Next Steps

1. **Voice Input** - Uncomment speech recognition in agent.py
2. **Cloud LLM** - Add OpenAI or Ollama integration
3. **Custom Avatar** - Replace avatar with your image
4. **Scheduled Tasks** - Add time-based reminders
5. **System Tray** - Minimize to system tray

## 📞 Getting Help

1. Check `README.md` for detailed documentation
2. Check `SETUP.md` for installation troubleshooting
3. Run `test_system.py` to diagnose issues
4. Review command examples on this page
5. Check application console for error messages

## 🎯 Feature Roadmap

- [ ] Voice-to-Text (Speech Recognition)
- [ ] Text-to-Speech (A.E.G.I.S speaks back)
- [ ] Cloud LLM integration (GPT-4, Mistral)
- [ ] Scheduled tasks & reminders
- [ ] Advanced application control
- [ ] Network/WiFi management
- [ ] Custom avatars & themes
- [ ] User profiles & authentication

---

**Pro Tip**: Keep this reference guide open while learning A.E.G.I.S commands!

**Version**: 1.0  
**Last Updated**: April 7, 2026
