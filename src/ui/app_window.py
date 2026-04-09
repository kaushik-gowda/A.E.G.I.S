# PyQt6 UI Module - Holographic AR Interface for A.E.G.I.S
# Autonomous Execution & Guidance Intelligent System

import sys
import math
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTextEdit, QLineEdit, QFrame,
                             QApplication)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import (QFont, QColor, QPainter, QPen, QBrush, QRadialGradient,
                         QLinearGradient, QPalette)
from datetime import datetime


class HolographicDisplay(QWidget):
    """Animated holographic display with rotating orbital rings and HUD elements."""
    
    def __init__(self):
        super().__init__()
        self.rotation = 0
        self.pulse = 0
        self.pulse_dir = 1
        self.setMinimumSize(300, 300)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)
    
    def update_animation(self):
        self.rotation = (self.rotation + 3) % 360
        self.pulse += self.pulse_dir
        if self.pulse >= 20:
            self.pulse_dir = -1
        elif self.pulse <= 0:
            self.pulse_dir = 1
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        cx, cy = self.width() / 2, self.height() / 2
        
        # Digital grid
        painter.setPen(QPen(QColor(0, 255, 65, 20), 1))
        for y in range(0, self.height(), 20):
            painter.drawLine(0, y, self.width(), y)
        for x in range(0, self.width(), 20):
            painter.drawLine(x, 0, x, self.height())
        
        # Concentric rings
        colors = [(0, 255, 65, 150), (0, 200, 255, 100), (255, 100, 200, 80), (0, 255, 65, 60)]
        radii = [40, 80, 120, 160]
        for r, color in zip(radii, colors):
            painter.setPen(QPen(QColor(*color), 2))
            painter.drawEllipse(int(cx - r), int(cy - r), r * 2, r * 2)
        
        # Rotating orbits with nodes
        for orbit_idx in range(3):
            orbit_r = 50 + orbit_idx * 40
            angle_off = self.rotation + orbit_idx * 120
            num_points = 3 + orbit_idx
            
            for i in range(num_points):
                angle = (360 / num_points * i + angle_off) * math.pi / 180
                x = cx + orbit_r * math.cos(angle)
                y = cy + orbit_r * math.sin(angle)
                
                # Draw node
                size = 4 + orbit_idx * 2
                node_c = QColor(0, 255 - orbit_idx * 30, 65 + orbit_idx * 20, 200)
                painter.setPen(QPen(node_c, 1))
                painter.setBrush(QBrush(node_c))
                painter.drawEllipse(int(x - size/2), int(y - size/2), size, size)
                
                # Connection line
                painter.setPen(QPen(QColor(0, 255, 65, 30 + orbit_idx * 20), 1))
                painter.drawLine(int(cx), int(cy), int(x), int(y))
        
        # Central pulsing core
        core_r = 25 + self.pulse
        gradient = QRadialGradient(int(cx), int(cy), int(core_r))
        gradient.setColorAt(0, QColor(0, 255, 65, 255))
        gradient.setColorAt(0.5, QColor(0, 255, 65, 100))
        gradient.setColorAt(1, QColor(0, 255, 65, 20))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(0, 255, 65, 200), 2))
        painter.drawEllipse(int(cx - core_r), int(cy - core_r), int(core_r * 2), int(core_r * 2))
        
        # Core label
        painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        painter.setPen(QPen(QColor(0, 255, 65, 255), 1))
        fm = painter.fontMetrics()
        text_w = fm.horizontalAdvance("A.E.G.I.S")
        painter.drawText(int(cx - text_w/2), int(cy + 4), "A.E.G.I.S")
        
        # HUD elements
        hud_items = [("ACTIVE", 20, 20), ("ONLINE", self.width() - 80, 20)]
        for text, hud_x, hud_y in hud_items:
            painter.setPen(QPen(QColor(0, 255, 65, 200), 1))
            painter.drawRect(hud_x, hud_y, 60, 30)
            painter.setFont(QFont("Consolas", 7, QFont.Weight.Bold))
            painter.drawText(hud_x + 3, hud_y + 10, text)
            painter.drawText(hud_x + 3, hud_y + 20, "✓")


class AegisWindow(QMainWindow):
    """Main holographic interface window for A.E.G.I.S."""
    
    agent_response_signal = pyqtSignal(str)
    status_update_signal = pyqtSignal(str)
    
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.setWindowTitle("A.E.G.I.S - Autonomous Execution & Guidance Intelligent System")
        self.setMinimumSize(1200, 800)
        self.current_status = "Initializing"
        
        self.setup_ui()
        self.position_window()
        
        self.agent_response_signal.connect(self.display_response)
        self.status_update_signal.connect(self.on_status_update)
        
        self.current_status = "Ready"
        self.update_status_display("System initialized. Awaiting commands...")
        
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.refresh_time)
        self.time_timer.start(1000)
        self.refresh_time()
    
    def setup_ui(self):
        """Build the user interface."""
        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("background-color: #0a0a0a;")
        
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left: Holography display
        left = self.build_holo_panel()
        main_layout.addWidget(left, 1)
        
        # Right: Command center
        right = self.build_command_panel()
        main_layout.addWidget(right, 1)
        
        # Apply theme
        theme_stylesheet = """
            QMainWindow { background-color: #0a0a0a; }
            QLabel { color: rgba(0, 255, 65, 220); }
        """
        self.setStyleSheet(theme_stylesheet)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(10, 10, 10))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 255, 65))
        self.setPalette(palette)
    
    def build_holo_panel(self):
        """Create holographic panel."""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(10, 10, 20, 255),
                    stop:1 rgba(5, 20, 30, 255));
                border: 2px solid rgba(0, 255, 65, 80);
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Hologram
        self.holo = HolographicDisplay()
        layout.addWidget(self.holo)
        
        # Status panel
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(20, 40, 60, 180);
                border: 1px solid rgba(0, 255, 65, 100);
                border-radius: 5px;
            }
        """)
        status_layout = QVBoxLayout(status_frame)
        status_layout.setContentsMargins(10, 10, 10, 10)
        
        title = QLabel("◇ AR SYSTEM ◇")
        title.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        title.setStyleSheet("color: rgba(0, 255, 65, 200);")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_layout.addWidget(title)
        
        self.ar_status = QLabel("Status: INITIALIZED")
        self.ar_status.setFont(QFont("Consolas", 9))
        self.ar_status.setStyleSheet("color: rgba(0, 200, 255, 200);")
        status_layout.addWidget(self.ar_status)
        
        energy_label = QLabel("Energy: 100%")
        energy_label.setFont(QFont("Consolas", 9))
        energy_label.setStyleSheet("color: rgba(0, 255, 65, 200);")
        status_layout.addWidget(energy_label)
        
        self.time_display = QLabel()
        self.time_display.setFont(QFont("Consolas", 8))
        self.time_display.setStyleSheet("color: rgba(200, 200, 200, 150);")
        self.time_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_layout.addWidget(self.time_display)
        
        layout.addWidget(status_frame)
        
        # Buttons
        btn_frame = QFrame()
        btn_frame.setStyleSheet("background-color: transparent;")
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setSpacing(5)
        
        clear_btn = QPushButton("█ CLEAR")
        voice_btn = QPushButton("◆ VOICE")
        
        for btn in [clear_btn, voice_btn]:
            btn.setFont(QFont("Arial", 9, QFont.Weight.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(0, 100, 150, 200),
                        stop:1 rgba(0, 50, 100, 200));
                    color: rgba(0, 255, 65, 255);
                    border: 1px solid rgba(0, 255, 65, 150);
                    border-radius: 3px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(0, 255, 65, 200),
                        stop:1 rgba(0, 200, 65, 200));
                    color: rgba(0, 0, 0, 255);
                }
            """)
            btn_layout.addWidget(btn)
        
        clear_btn.clicked.connect(self.clear_display)
        voice_btn.clicked.connect(self.activate_voice)
        
        layout.addWidget(btn_frame)
        layout.addStretch()
        
        return panel
    
    def build_command_panel(self):
        """Create command center panel."""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(10, 30, 40, 255),
                    stop:1 rgba(20, 10, 30, 255));
                border-left: 2px solid rgba(0, 255, 65, 80);
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 50, 100, 100);
                border: 1px solid rgba(0, 255, 65, 100);
                border-radius: 3px;
            }
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 5, 10, 5)
        
        title = QLabel("▬ COMMAND CENTER ▬")
        title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        title.setStyleSheet("color: rgba(0, 255, 65, 220);")
        header_layout.addWidget(title)
        
        self.activity = QLabel("● ONLINE")
        self.activity.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        self.activity.setStyleSheet("color: rgba(0, 255, 65, 200);")
        header_layout.addStretch()
        header_layout.addWidget(self.activity)
        
        layout.addWidget(header)
        
        # Chat display
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setFont(QFont("Consolas", 10))
        self.chat.setStyleSheet("""
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(10, 10, 20, 200),
                    stop:1 rgba(5, 20, 30, 200));
                color: rgba(0, 255, 65, 220);
                border: 1px solid rgba(0, 255, 65, 80);
                border-radius: 3px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.chat, 2)
        
        # Status line
        self.status = QLabel("Status: Ready")
        self.status.setFont(QFont("Consolas", 8))
        self.status.setStyleSheet("color: rgba(100, 200, 255, 180);")
        layout.addWidget(self.status)
        
        # Input frame
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 50, 80, 80);
                border: 1px solid rgba(0, 255, 65, 80);
                border-radius: 3px;
            }
        """)
        input_layout = QVBoxLayout(input_frame)
        input_layout.setContentsMargins(8, 8, 8, 8)
        input_layout.setSpacing(5)
        
        input_label = QLabel("▼ INPUT SEQUENCE ▼")
        input_label.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        input_label.setStyleSheet("color: rgba(0, 200, 255, 200);")
        input_layout.addWidget(input_label)
        
        # Command input
        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Consolas", 10))
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: rgba(10, 10, 20, 200);
                color: rgba(0, 255, 65, 255);
                border: 1px solid rgba(0, 255, 65, 150);
                border-radius: 3px;
                padding: 6px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(0, 200, 255, 200);
                background: rgba(0, 50, 100, 150);
            }
        """)
        self.input_field.returnPressed.connect(self.execute_command)
        input_layout.addWidget(self.input_field)
        
        # Execute button
        exec_btn = QPushButton("▶ EXECUTE SEQUENCE ▶")
        exec_btn.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        exec_btn.setMinimumHeight(35)
        exec_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 100, 200, 200),
                    stop:1 rgba(0, 50, 150, 200));
                color: rgba(0, 255, 65, 255);
                border: 1px solid rgba(0, 255, 65, 180);
                border-radius: 3px;
                padding: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 255, 65, 220),
                    stop:1 rgba(0, 200, 65, 220));
                color: rgba(0, 0, 0, 255);
            }
        """)
        exec_btn.clicked.connect(self.execute_command)
        input_layout.addWidget(exec_btn)
        
        layout.addWidget(input_frame)
        
        return panel
    
    def execute_command(self):
        """Execute user command."""
        cmd = self.input_field.text().strip()
        if not cmd:
            return
        
        self.input_field.clear()
        ts = datetime.now().strftime("%H:%M:%S")
        self.chat.append(f"<span style='color: rgba(0, 200, 255, 220);'>[{ts}] ◆ USER: {cmd}</span>")
        self.update_status_display("Processing...")
        self.activity.setText("◉ PROCESSING")
        
        self.agent.process_command(cmd, self.on_response)
    
    def on_response(self, response):
        """Receive agent response."""
        self.agent_response_signal.emit(response)
    
    def display_response(self, response):
        """Display response in chat."""
        ts = datetime.now().strftime("%H:%M:%S")
        self.chat.append(f"<span style='color: rgba(0, 255, 65, 220);'>[{ts}] ◆ A.E.G.I.S: {response}</span>")
        self.activity.setText("● ONLINE")
        self.update_status_display("Ready")
        self.chat.verticalScrollBar().setValue(self.chat.verticalScrollBar().maximum())
    
    def update_status_display(self, msg):
        """Update status display."""
        self.current_status = msg
        ts = datetime.now().strftime("%H:%M:%S")
        self.status.setText(f"Status: {msg} [{ts}]")
    
    def on_status_update(self, msg):
        """Handle status update signal."""
        self.update_status_display(msg)
    
    def refresh_time(self):
        """Update time display."""
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.time_display.setText(f"{current_date}\n{current_time}")
    
    def clear_display(self):
        """Clear chat history."""
        self.chat.clear()
        self.chat.append("<span style='color: rgba(0, 255, 65, 220);'>[SYSTEM] Chat cleared</span>")
        self.update_status_display("Chat cleared")
    
    def activate_voice(self):
        """Activate voice mode."""
        self.update_status_display("Activating voice...")
        self.chat.append("<span style='color: rgba(255, 150, 0, 220);'>[SYSTEM] ▲ VOICE RECOGNITION ENABLED</span>")
        self.chat.append("<span style='color: rgba(0, 200, 255, 200);'>Listening for: 'Hey Aegis'...</span>")
        self.agent.process_command("activate voice", self.on_response)
    
    def position_window(self):
        """Position window on secondary screen or primary."""
        screens = QApplication.screens()
        
        if len(screens) > 1:
            screen = screens[1]
            self.setGeometry(screen.geometry())
        else:
            screen = screens[0]
            geo = screen.geometry()
            self.setGeometry(geo.right() - 1200 - 10, geo.top() + 10, 1200, 800)
    
    def closeEvent(self, event):
        """Handle window close."""
        self.time_timer.stop()
        if self.holo and hasattr(self.holo, 'timer'):
            self.holo.timer.stop()
        super().closeEvent(event)
