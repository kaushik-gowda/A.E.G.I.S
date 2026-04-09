# Voice Input Module for A.E.G.I.S
# Handles speech-to-text and voice activation

import threading
from typing import Callable, Optional, Dict, Any
import queue

# Try to import speech recognition, but handle missing dependencies gracefully
try:
    import speech_recognition as sr
    VOICE_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    VOICE_AVAILABLE = False
    sr = None

class VoiceActivationSystem:
    """Handles voice input and speech-to-text functionality."""
    
    def __init__(self):
        """Initialize voice activation system."""
        self.voice_available = VOICE_AVAILABLE
        self.recognizer = None
        self.microphone = None
        self.is_listening = False
        self.listen_thread = None
        self.command_queue = queue.Queue()
        
        self.wake_words = ["aegis", "a.e.g.i.s", "hey aegis", "listen aegis"]
        self.confidence_threshold = 0.5
        
        # Don't initialize hardware until needed
        if VOICE_AVAILABLE:
            self._try_initialize()
    
    def _try_initialize(self):
        """Try to initialize voice hardware."""
        try:
            if sr is None:
                self.voice_available = False
                return
            
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.voice_available = True
            
            # Adjust recognizer settings
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
        except Exception as e:
            self.voice_available = False
            print(f"Voice initialization warning: {str(e)}")
    
    def start_listening(self, on_command_callback: Callable):
        """
        Start listening for voice commands.
        
        Args:
            on_command_callback: Callback function when command is recognized
        """
        # Try to initialize if not already done
        if self.recognizer is None and VOICE_AVAILABLE:
            self._try_initialize()
        
        if not self.voice_available:
            return "🎤 Voice system not available (PyAudio not installed). Use text commands instead."
        
        self.is_listening = True
        self.listen_thread = threading.Thread(
            target=self._listen_loop,
            args=(on_command_callback,),
            daemon=True
        )
        self.listen_thread.start()
        return "Voice activation started"
    
    def stop_listening(self):
        """Stop listening for voice commands."""
        self.is_listening = False
        return "Voice activation stopped"
    
    def _listen_loop(self, callback: Callable):
        """Main listening loop running in background thread."""
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for audio
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                # Try to recognize it
                try:
                    text = self.recognizer.recognize_google(audio)
                    
                    # Check for wake word
                    if self._check_wake_word(text):
                        # Extract command after wake word
                        command = self._extract_command(text)
                        if command:
                            callback(command)
                
                except sr.UnknownValueError:
                    # Couldn't understand audio, continue listening
                    pass
                except sr.RequestError as e:
                    # API error (network, etc.)
                    pass
            
            except sr.RequestError:
                # Timeout or no audio
                pass
            except Exception as e:
                if self.is_listening:
                    pass
    
    def _check_wake_word(self, text: str) -> bool:
        """Check if wake word is present."""
        text_lower = text.lower()
        for wake_word in self.wake_words:
            if wake_word in text_lower:
                return True
        return False
    
    def _extract_command(self, text: str) -> str:
        """Extract command from text after wake word."""
        text_lower = text.lower()
        
        # Remove wake words
        command = text_lower
        for wake_word in self.wake_words:
            command = command.replace(wake_word, "").strip()
        
        return command if command else None
    
    def recognize_command(self, timeout: int = 10) -> Optional[str]:
        """
        Recognize a single voice command (blocking).
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Recognized command or None
        """
        if not self.voice_available:
            return None
        
        try:
            with self.microphone as source:
                print("🎤 Listening for command...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
            
            try:
                command = self.recognizer.recognize_google(audio)
                print(f"Recognized: {command}")
                return command
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                return None
        
        except Exception as e:
            return None
    
    def get_voice_status(self) -> Dict[str, Any]:
        """Get voice system status."""
        return {
            "available": self.voice_available,
            "listening": self.is_listening if self.voice_available else False,
            "wake_words": self.wake_words if self.voice_available else [],
            "threshold": self.confidence_threshold if self.voice_available else 0,
            "status": "Active" if (self.voice_available and self.is_listening) else ("Inactive" if self.voice_available else "Not Available")
        }

# Global instance
voice_system = VoiceActivationSystem()
