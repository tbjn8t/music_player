from PyQt6.QtWidgets import (QFrame, QLabel, QVBoxLayout, QPushButton, QStackedLayout, QWidget)

from PyQt6.QtCore import Qt, pyqtSignal, QEvent
from PyQt6.QtGui import QPixmap, QCursor

class AlbumCard(QFrame):
    clicked = pyqtSignal(object)
    play_requested = pyqtSignal(object)
    
    def __init__(self, album, artist, songs, artwork=None):
        super().__init__()
        
        self.album = album
        self.artist = artist
        self.songs = songs
                        
        self.setup_ui(artwork)
        
        self.play_button.clicked.connect(self.play_album)
            
    def setup_ui(self, artwork):
        self.setFixedSize(180, 240)
                
        # Main Layout
        layout = QVBoxLayout()
        
        layout.setContentsMargins(10, 10,10, 10)
        layout.setSpacing(5)
        
        # Album Artwork
        self.artwork = QLabel()
        
        self.artwork.setFixedSize(160, 160)
        self.artwork.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Load Artwork
        if artwork:
            pixmap = QPixmap()

            if pixmap.loadFromData(artwork):
                pixmap = pixmap.scaled(
                    160,
                    160,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.artwork.setPixmap(pixmap)
            else:
                self.artwork.setText("No Artwork")
        else:
            self.artwork.setText("No Artwork")

        # Artwork + Play Button Container
        self.artwork_container = QWidget()
        
        artwork_layout = QStackedLayout()
        artwork_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        
        self.artwork_container.setLayout(artwork_layout)
        
        artwork_layout.addWidget(self.artwork)
        
        # Play Button
        self.play_button = QPushButton("▶")
        self.play_button.setFixedSize(55, 55)
        self.play_button.setVisible(False)
        self.play_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 220);
                color: black;
                border-radius: 27px;
                font-size: 30px;
            }

            QPushButton:hover {
                background-color: white;
            }
        """)
        artwork_layout.addWidget(self.play_button)
        artwork_layout.setAlignment(self.play_button, Qt.AlignmentFlag.AlignCenter)   
            
        # Album Title
        self.album_label = QLabel(self.album)
        
        self.album_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.album_label.setWordWrap(True)
        
        # Artist Label
        self.artist_label = QLabel(self.artist)
        self.artist_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        layout.addWidget(self.artwork_container)
        layout.addWidget(self.album_label)
        layout.addWidget(self.artist_label)
        
        self.setLayout(layout)
    
    # Play Album when clicked  
    def play_album(self):
        self.play_requested.emit(self.songs)
    
    def enterEvent(self, event):
        self.play_button.show()
        self.play_button.raise_()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        cursor_pos = self.mapFromGlobal(QCursor.pos())
        
        if not self.rect().contains(cursor_pos):
            self.play_button.hide()
            
        super().leaveEvent(event)
                    
    # Click Album event    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self)
            
        super().mousePressEvent(event)