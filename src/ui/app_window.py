# A.E.G.I.S Holographic Display
# Minimalist UI - Only the 3D Iron Man Holographic Core

from pathlib import Path
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWebEngineWidgets import QWebEngineView


class HolographicDisplay(QWebEngineView):
    """Embedded 3D holographic animation."""
    
    def __init__(self):
        super().__init__()
        html_path = Path(__file__).parent.parent.parent / "holographic_core.html"
        self.load(QUrl.fromLocalFile(str(html_path.resolve())))


class AegisWindow(QMainWindow):
    """Minimalist fullscreen holographic display window."""
    
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.setWindowTitle("A.E.G.I.S - Holographic Core")
        self.showMaximized()
        
        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("background-color: #000000;")
        
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.holo = HolographicDisplay()
        layout.addWidget(self.holo)
        
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
        self.setPalette(palette)
    
    def closeEvent(self, event):
        super().closeEvent(event)