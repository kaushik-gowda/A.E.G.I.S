# A.E.G.I.S Professional Setup Guide

## 🎯 System Requirements

- **OS**: Windows 10/11 64-bit
- **RAM**: Minimum 4GB (8GB recommended)
- **Python**: 3.10+
- **Microphone**: For voice input
- **Internet**: Required for first-time TTS voice download

## 📦 Installation Steps

### Step 1: Install Dependencies

#### Option A: Automatic Setup (if setup script exists)
```bash
python setup.py
```

#### Option B: Manual Setup

Open PowerShell in the project directory and run:

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install required packages
pip install --upgrade pip
pip install PyQt6==6.7.1
pip install PyQt6-WebEngineWidgets==6.7.1
pip install SpeechRecognition==3.10.0
pip install pocketsphinx==0.1.15
pip install pyaudio==0.2.13
pip install edge-tts==6.1.1
pip install psutil==5.9.6
pip install GPUtil==1.4.0
```

### Step 2: Audio Input Setup

A.E.G.I.S requires PyAudio for microphone access.

**Windows Installation:**
```powershell
pip install pipwin
pipwin install pyaudio
```

If that fails:
```powershell
pip install --only-binary=:all: pyaudio
```

**Troubleshooting PyAudio:**
- If installation fails, download pre-compiled wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- Match your Python version and Windows bitness (32-bit or 64-bit)
- Install with: `pip install <wheel_file>.whl`

### Step 3: Setup System Startup (Optional)

To make A.E.G.I.S listen automatically on system startup:

#### Windows Task Scheduler Setup:

1. **Open PowerShell as Administrator**
   - Right-click Start Menu → Windows PowerShell (Admin)

2. **Navigate to project directory:**
   ```powershell
   cd "E:\A.E.G.I.S"
   ```

3. **Run the setup script:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File setup_scheduler.ps1 -Install
   ```

4. **Verify installation:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File setup_scheduler.ps1 -Status
   ```

**To disable auto-start:**
```powershell
powershell -ExecutionPolicy Bypass -File setup_scheduler.ps1 -Remove
```

## 🚀 Running A.E.G.I.S

### Manual Launch

**Option 1: Run Script**
```bash
.\launch_aegis.bat
```

**Option 2: Direct Python**
```powershell
.\venv\Scripts\python main.py
```

### Auto-Launch on Startup

If scheduling is set up, A.E.G.I.S will automatically:
1. Listen in the background for wake word
2. Stay hidden until activated
3. Open on "Hey aegis wake up" voice command

## 🎤 Usage

### Wake Word Activation

Say one of these phrases to activate:
- **"Hey aegis wake up"** (primary wake word)
- **"Hey aegis wakeup"**
- **"Hey aegis"** (quick activation)
- **"Aegis wake up"**

### System Interface Features

Once activated, A.E.G.I.S displays:

#### Left Panel - Chat Interface
- 🎤 Voice command input
- Bot responses with system info
- Command history

#### Right Panel - System Stats (Real-time)
- **CPU Usage**: Current percentage and cores
- **Memory**: RAM usage with available amount
- **Storage**: Disk usage and free space
- **Network**: Active interfaces
- **GPU**: VRAM usage (if available)

### Voice Commands Examples

**Application Control:**
- "Open Chrome"
- "Launch VS Code"
- "Close Teams"
- "Open Discord"

**Settings:**
- "Open display settings"
- "Open network settings"
- "Open sound settings"
- "Open WiFi settings"
- "Open Bluetooth settings"

**Exit Commands:**
- "Exit" / "Stop" / "Goodbye"
- System will power down after 2 seconds

## ⚙️ Configuration

### Wake Word Sensitivity

Edit `src/tools/wake_word_detector.py`:

```python
# In WakeWordDetector.__init__():
self.sensitivity = "medium"  # Options: 'low', 'medium', 'high'
```

- **low**: Fewer false activations (0.7 threshold)
- **medium**: Balanced (0.6 threshold) - Recommended
- **high**: More responsive (0.5 threshold)

### Voice Selection

Edit `src/tools/text_to_speech.py`:

```python
# Available voices:
# English US:
#   - en-US-AriaNeural (female, default)
#   - en-US-GuyNeural (male)
#   - en-US-AmberNeural (female)
#   - en-US-AshleyNeural (female)
#
# English UK:
#   - en-GB-SoniaNeural (female)
#   - en-GB-RyanNeural (male)

self.voice = "en-US-GuyNeural"  # Change this
```

### Application Aliases

Edit `src/tools/voice_commands.py` to add more apps:

```python
self.app_aliases = {
    'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
    'your_app': r'C:\Path\To\Your\Application.exe',
    # Add more...
}
```

### Settings Mappings

Add more Windows settings in `src/tools/voice_commands.py`:

```python
self.settings_map = {
    'display': 'ms-settings:display',
    'your_setting': 'ms-settings:YOUR-SETTINGS-URI',
    # List: https://docs.microsoft.com/en-us/windows/uwp/launch-resume/ms-settings-uri-scheme-reference
}
```

## 📊 System Monitoring

A.E.G.I.S displays comprehensive system metrics:

### Metrics Displayed
- CPU % (processor cores)
- Memory (GB used/available)
- Storage (GB used/free)
- Network interfaces (active count)
- GPU Memory (MB used, if available)

Updates every 3 seconds automatically.

## 🔐 Permissions

Windows may ask for permissions for:
- Microphone access (always required)
- Application launching (first time for each app)
- Settings access (may require admin)

Grant permissions as prompted.

## 🐛 Troubleshooting

### "PyAudio not found"
```powershell
pip install PyAudio
# Or if above fails:
pipwin install pyaudio
```

### "Google Cloud API error"
- Check internet connection
- Requires network for speech recognition
- Try again after a few seconds

### "Voice not working"
- Verify microphone is connected and enabled
- Check Windows audio settings
- Test microphone in Windows Settings → Sound

### "Wake word not detecting"
- Speak clearly and at normal volume
- Reduce background noise
- Adjust sensitivity in settings
- Try different wake word variations

### "Application won't launch"
- Try manual path in voice_commands.py
- Ensure application is installed
- Check if path is correct (some apps install differently)

### Task Scheduler Not Working
```powershell
# Check task status:
Get-ScheduledTask | Select-Object TaskName, State

# Manual task check:
Get-ScheduledTask -TaskName "A.E.G.I.S-WakeWordListener"

# Remove and reinstall:
powershell -ExecutionPolicy Bypass -File setup_scheduler.ps1 -Remove
powershell -ExecutionPolicy Bypass -File setup_scheduler.ps1 -Install
```

## 🎨 UI Components

### Professional Interface
- **Header**: Logo, status indicator, system time
- **Chat Panel**: Message history with syntax highlighting
- **Stats Panel**: Real-time system metrics with visual bars
- **Input Area**: Text input + voice button + send button

### Color Scheme
- **Primary**: Orange (#ff9500)
- **Accent**: Gold (#ffd700)
- **Background**: Deep Blue (#050810, #0a0e27)
- **Text**: Clean white on dark background

## 📝 File Structure

```
A.E.G.I.S/
├── main.py                          # Entry point
├── launch_aegis.bat                 # Launcher script
├── setup_scheduler.ps1              # Task Scheduler setup
├── professional_ui.html             # Professional UI
├── src/
│   ├── core/
│   │   └── agent.py                 # Main AI agent
│   ├── tools/
│   │   ├── wake_word_detector.py    # Wake word listener
│   │   ├── voice_input.py           # Speech recognition
│   │   ├── voice_commands.py        # Command processor
│   │   ├── text_to_speech.py        # Speech synthesis
│   │   ├── system_monitor.py        # System metrics
│   │   ├── system_control.py        # System control
│   │   ├── os_commands.py           # OS commands
│   │   └── app_discovery.py         # App discovery
│   └── ui/
│       └── app_window.py            # PyQt6 main window
└── venv/                            # Virtual environment
```

## 🔗 References

- [Microsoft Settings URI Scheme](https://docs.microsoft.com/en-us/windows/uwp/launch-resume/ms-settings-uri-scheme-reference)
- [PyQt6 Documentation](https://doc.qt.io/qtforpython/)
- [SpeechRecognition Docs](https://github.com/Uberi/speech_recognition)
- [Edge TTS Documentation](https://github.com/rany2/edge-tts)

## ✨ Features Summary

✅ Wake word detection ("Hey aegis wake up")
✅ Professional glassmorphism UI
✅ Real-time system monitoring
✅ Voice command processing
✅ Natural language responses
✅ Text-to-speech with neural voices
✅ Application launcher (40+ apps)
✅ Windows settings accessor (35+ settings)
✅ System startup auto-launch
✅ Full voice-based interface

---

**Version**: 2.0+
**Last Updated**: April 2026
**Status**: Production Ready ✨
