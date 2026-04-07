# A.E.G.I.S - Autonomous Execution & Guidance Intelligent System
# Main entry point for the AI desktop assistant

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import QApplication
from ui.app_window import AegisWindow
from core.agent import AegisAgent

def main():
    """Initialize and run the A.E.G.I.S system."""
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Initialize the AI agent
    agent = AegisAgent()
    
    # Create and show the main window
    window = AegisWindow(agent)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
