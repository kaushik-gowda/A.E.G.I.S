# A.E.G.I.S (Autonomous Execution & Guidance Intelligent System) Setup Guide

## Complete Setup Instructions

### Step 1: Initial Setup (One-Time)

#### Option A: Using Batch File (Recommended for Windows)
```batch
run.bat
```

This automatically handles:
- Virtual environment activation
- Application launch
- Error handling

#### Option B: Manual Setup
```powershell
cd e:\A.E.G.I.S

# Create virtual environment
python -m venv venv

# Install dependencies
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt

# Run application
.\venv\Scripts\python.exe main.py
```

### Step 2: Dependency Installation Details

If you encounter any issues, try installing core dependencies individually:

```powershell
cd e:\A.E.G.I.S

# Core packages
.\venv\Scripts\python.exe -m pip install PyQt6 --no-cache-dir
.\venv\Scripts\python.exe -m pip install psutil requests --no-cache-dir
.\venv\Scripts\python.exe -m pip install python-dotenv --no-cache-dir

# Voice/Audio packages (optional but recommended)
.\venv\Scripts\python.exe -m pip install SpeechRecognition pyttsx3 edge-tts pydub --no-cache-dir

# Image processing
.\venv\Scripts\python.exe -m pip install Pillow --no-cache-dir
```

### Step 3: First Launch

Run the application:
```powershell
cd e:\A.E.G.I.S
.\venv\Scripts\python.exe main.py
```

Expected behavior:
- PyQt6 window opens with A.E.G.I.S interface
- Left panel shows avatar and system status
- Right panel shows command input area
- Green terminal-style aesthetic

## 🖥️ Monitor Configuration

### Dual Monitor Setup
- **Recommended**: Use this for best experience
- A.E.G.I.S will automatically launch on secondary monitor
- Primary monitor remains free for other work

### Single Monitor Setup
- A.E.G.I.S launches on right side of screen
- Leave space on primary monitor
- Resize window as needed (min: 1200x800)

## 🎮 Test the System

### Quick Test (No UI)
```powershell
cd e:\A.E.G.I.S
.\venv\Scripts\python.exe test_system.py
```

### Interactive Test
Once the UI is running:
1. Try: `launch spotify`
2. Try: `system info`
3. Try: `add task Test Task`
4. Try: `help`

## 🔧 Troubleshooting

### "PyQt6 not found" Error
```powershell
.\venv\Scripts\python.exe -m pip install --force-reinstall PyQt6
```

### "psutil not found" Error
```powershell
.\venv\Scripts\python.exe -m pip install psutil
```

### Window won't appear
1. Check if secondary monitor is connected
2. Try moving window with Alt+Tab
3. Verify PyQt6 installation: 
   ```powershell
   .\venv\Scripts\python.exe -c "import PyQt6; print('OK')"
   ```

### Application crashes on launch
```powershell
# Check for missing dependencies
.\venv\Scripts\python.exe -c "import PyQt6, psutil, requests; print('All imports OK')"

# Reinstall all packages
.\venv\Scripts\python.exe -m pip install --force-reinstall -r requirements.txt
```

### Application runs but no window visible
- Check if it's running in background: Look for `python.exe` in Task Manager
- Try moving the window: Right-click taskbar button → Move
- Try different monitor configuration

## 📝 Configuration Files

All data is stored in the `data/` folder:
- `tasks.json` - Your saved tasks
- Future: conversation logs, preferences, etc.

## 🚀 Next Steps

1. **Basic Usage**: Try 5-10 commands to familiarize yourself
2. **Customize**: Add your favorite applications to `known_apps` in `os_commands.py`
3. **Extend**: Create custom command handlers in `agent.py`
4. **Integrate**: Add voice support with Speech Recognition module

## 💡 Pro Tips

### Keep A.E.G.I.S Always Visible
- Set window to "Always On Top":
  - Right-click window title bar
  - Use Alt+Space > P on Windows
- Position on secondary monitor for dedicated interface

### Quick Commands
- Save frequently used complex commands as tasks
- Use short keywords: "VS" for VS Code, "Spot" for Spotify
- Batch commands: "Launch VS Code, open chrome, set volume 60"

### Performance
- A.E.G.I.S uses minimal resources (~50MB memory)
- Safe to run alongside work applications
- Task data saved locally (no internet required for base functions)

## 📞 Support Resources

### Python Environment Issues
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Pip Documentation](https://pip.pypa.io/en/latest/)

### PyQt6
- [PyQt6 Getting Started](https://www.riverbankcomputing.com/static/Docs/PyQt6/getting_started.html)
- [PyQt6 API Reference](https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtwidgets/)

### Windows Automation
- [Python subprocess Module](https://docs.python.org/3/library/subprocess.html)
- [psutil Documentation](https://psutil.readthedocs.io/)

---

**Ready?** Run `.\venv\Scripts\python.exe main.py` and start commanding!
