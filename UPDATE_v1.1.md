# A.E.G.I.S v1.1 - Voice & Advanced System Control Update

## 🎉 What's New

Complete voice activation system and advanced Windows control with permission-based full system management.

---

## 🎤 Voice Activation System

### How to Use Voice Commands

1. **Click "Speak" Button** or type "activate voice"
2. **Say**: "Hey Aegis" (wake word)
3. **Follow with**: Your command

### Voice Commands Examples
```
"Hey Aegis, launch Chrome"
"Hey Aegis, what's the system info?"
"Hey Aegis, open settings"
"Hey Aegis, set volume to 50"
"Hey Aegis, shutdown in 60 seconds"
```

### Voice Features
✅ Continuous listening mode  
✅ Wake word detection ("Hey Aegis", "Aegis", "Listen Aegis")  
✅ Google Speech-to-Text integration  
✅ Background processing (non-blocking)  
✅ Start/stop voice at any time  

---

## 📱 Dynamic Application Discovery

### Automatically Finds All Apps

A.E.G.I.S now scans your entire system for installed applications:
- Program Files directories
- Windows Registry
- System applications
- Cached for fast access

### New Launch Capabilities

**Before**: Limited to 10 known apps  
**Now**: Can launch ANY installed application!

### Examples
```
"Launch Adobe Photoshop"
"Open OBS Studio"
"Start Visual Studio"
"Run VLC Media Player"
"Launch Microsoft Word"
"Open Firefox"
"Start Steam"
```

---

## 🎮 Advanced System Control

### New Power Commands

#### Shutdown & Restart
```
"Shutdown" - Immediate shutdown
"Shutdown in 60 seconds" - Delayed shutdown
"Restart" - Immediate restart
"Restart in 60 seconds" - Delayed restart
```

#### Sleep & Lock
```
"Sleep" - Put computer to sleep
"Hibernate" - Hibernate computer
"Lock screen" - Lock Windows
```

### Settings & Control Panel Access

#### Windows Settings
```
"Open Settings Display" - Display settings
"Open Settings Sound" - Sound settings
"Open Settings Network" - Network settings
"Open Settings Bluetooth" - Bluetooth settings
"Open Settings Keyboard" - Keyboard settings
"Open Settings Mouse" - Mouse settings
"Open Settings Power" - Power settings
"Open Settings Update" - Windows Update
"Open Settings Privacy" - Privacy settings
```

#### Control Panel
```
"Open Control Panel" - Main control panel
"Control Panel Network" - Network settings
"Control Panel Sound" - Sound settings
"Control Panel Display" - Display settings
"Control Panel Devices" - Device settings
"Control Panel System" - System settings
"Control Panel Power" - Power settings
```

#### System Tools
```
"Task Manager" - Open Task Manager
"Device Manager" - Open Device Manager
"System Information" - Detailed system info
```

### System Monitoring

#### Get Detailed Information
```
"System info" - Full system specifications
"Disk info" - Disk usage for all partitions
"Show processes" - Top processes by CPU/memory
"Network info" - Network status
"Internet speed" - Connection status
```

---

## 🔐 Permission & Security

### Features Requiring Confirmation
Some power commands require administrative action:
- System shutdown/restart
- Screen locking
- Process termination

### Safety Features
✅ Delayed shutdown (allows cancellation with Command Prompt)  
✅ Clear command feedback  
✅ Warning messages for destructive actions  
✅ Graceful error handling  

---

## 🗜️ Architecture Updates

### New Modules

#### 1. **voice_input.py**
- Speech Recognition via Google API
- Wake word detection
- Continuous listening
- Command extraction

#### 2. **app_discovery.py**
- Registry scanning
- Program Files scanning
- Application caching (JSON)
- Fuzzy matching for app names
- 50+ pre-configured system apps

#### 3. **system_control.py**
- Power management (shutdown, restart, sleep)
- Screen control (lock, sleep, brightness)
- Settings access (20+ control panel sections)
- Process management
- Network monitoring
- Detailed system information

### Updated Files
- **agent.py** - New command handlers
- **app_window.py** - Enhanced voice button
- **os_commands.py** - No changes (kept for backward compatibility)

---

## 📊 Command Routing

```
User Input
    ↓
UI or Voice System
    ↓
Agent._handle_command()
    ├─ [launch] → app_discovery.launch_app()
    ├─ [settings] → system_control.open_settings()
    ├─ [shutdown] → system_control.shutdown()
    ├─ [power] → system_control (various)
    ├─ [voice] → voice_system (control)
    ├─ [task] → task_manager
    ├─ [system] → system_control
    └─ [other] → general handlers
    ↓
Response Back to UI
```

---

## 🚀 Quick Start with New Features

### 1. Launch Any Application
```
"Launch Adobe Photoshop"
→ A.E.G.I.S finds it in registry/Program Files and launches it
```

### 2. Enable Voice Mode
```
Click "Speak" button or say "activate voice"
→ Listen for "Hey Aegis" wake word
→ Say command after wake word
```

### 3. Access Settings Quickly
```
"Open Settings Sound" 
→ Windows Settings opens to Sound section
```

### 4. System Shutdown with Delay
```
"Shutdown in 120 seconds"
→ System will shutdown in 2 minutes
→ Allows time to save work or cancel
```

### 5. Check Full System Status
```
"System Info"
→ Shows: CPU cores, memory, disk space, temp, OS version, etc.
```

---

## 🔄 Cache Management

### App Cache
- **Location**: `data/apps_cache.json`
- **Updated**: On discovery or manual refresh
- **Purpose**: Fast app lookup

### Refresh Apps
```
"Refresh apps" - Re-scans system for new applications
→ Updates cache with latest installations
```

---

## 📝 New Command Examples

### Scenario 1: Morning Routine
```
"Launch Spotify" → Opens Spotify
"Set volume to 60" → Adjusts volume
"Open Settings Display" → Display settings
```

### Scenario 2: System Maintenance
```
"System info" → View specs
"Disk info" → Check storage
"Show processes" → Monitor running apps
"Task Manager" → Open Task Manager
```

### Scenario 3: Meeting Prep
```
"Launch Teams" → Start Teams
"Mute microphone" → (future feature)
"Lock screen" → Lock before meeting
```

### Scenario 4: Shutdown
```
"Shutdown in 60" → Stop work in 1 minute
→ Saves data and initiates shutdown
```

---

## 🎤 Voice System Details

### How Voice Works

1. **Listen Mode**: App listens for audio via microphone
2. **Wake Word Detection**: Checks if "Aegis" is mentioned
3. **Speech-to-Text**: Converts audio to text using Google API
4. **Command Extraction**: Removes wake word and extracts command
5. **Processing**: Sends to main command handler
6. **Response**: A.E.G.I.S executes and provides feedback

### Voice Settings

Default wake words:
- "aegis"
- "a.e.g.i.s"
- "hey aegis"
- "listen aegis"

### Microphone Setup
- Automatically detects system microphone
- Adjusts for ambient noise
- 10-second timeout per utterance
- Tries Google Speech Recognition API

---

## 🛠️ Troubleshooting New Features

### Voice Not Working

1. **Check Microphone**
   ```
   Windows Settings → Sound → Input devices
   ```

2. **Check Internet**
   - Voice uses Google API (requires internet)
   - Test: `ping google.com`

3. **Try Manual Command**
   ```
   Type: "activate voice"
   Or click: "Speak" button
   ```

### Apps Not Discovered

1. **Refresh Cache**
   ```
   "Refresh apps"
   ```

2. **Try Full Name**
   ```
   "Launch Microsoft Teams" instead of "Launch Teams"
   ```

3. **Check Installation**
   - Ensure app is installed properly
   - Check Program Files or registry

### Settings Won't Open

1. **Try Control Panel**
   ```
   "Control Panel Display" instead of "Settings Display"
   ```

2. **Check Windows Version**
   - Some sections only in Windows 10/11

3. **Verify Paths**
   ```
   Check: src/tools/system_control.py
   ```

---

## 🔔 Complete Permission Model

### User Commands (Always Allowed)
✅ Launch applications  
✅ Open settings  
✅ Check system info  
✅ Manage tasks  
✅ Change volume  
✅ Read files  

### System Commands (May Require Auth)
⚠ Shutdown/Restart - Gracefully handled  
⚠ Sleep/Lock - PC control  
⚠ Settings changes - Windows manages  
⚠ Process termination - Windows manages  

### Denied Commands (Never)
❌ Change system files  
❌ Modify registry directly  
❌ Elevate privileges  

---

## 📖 Updated Help Command

Type or say: **"Help"**

Shows all available commands organized by category:
- 🚀 Applications - Launch apps
- 💻 System Control - Settings, power
- ⚡ Power Commands - Shutdown, restart, sleep
- 📋 Tasks - Todo management
- 🔊 System - Volume, info
- 🎤 Voice - Voice control
- ❓ Info - Settings and help

---

## 🎯 Feature Roadmap (Future)

Currently Being Tested:
- [ ] Microphone array support (multiple mics)
- [ ] Custom wake words
- [ ] Voice response feedback (TTS)
- [ ] Advanced scheduling

Planned:
- [ ] Context-aware commands
- [ ] Multi-step workflows
- [ ] Voice profiles
- [ ] Command macros

---

## ✅ Testing Checklist

- [x] Voice activation tested
- [x] App discovery verified
- [x] Settings access confirmed
- [x] Power commands working
- [x] Error handling robust
- [x] UI updates responsive
- [x] Command routing correct

---

## 🚀 How to Use

### Update Your A.E.G.I.S

Your application automatically has these features if installed from the latest source. No reinstallation needed!

Simply run:
```powershell
cd e:\A.E.G.I.S
.\venv\Scripts\python.exe main.py
```

### First Time Setup Voice

1. Ensure microphone is connected and working
2. Check Windows microphone permissions
3. Verify internet connection
4. Click "Speak" button or say "activate voice"

---

**Version**: 1.1.0  
**Release Date**: April 7, 2026  
**Status**: Production Ready  

**Your AI assistant just got smarter! 🤖💚**
