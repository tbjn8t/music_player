from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
    QFrame
)

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap

class AlbumDetailView(QWidget):
    back_requested = pyqtSignal()
    play_album_requested = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        
        self.current_album = None
        self.current_artist = None
        self.songs = []
        
        self.setup_ui()
        
    def setup_ui(self):
        
        # Main Page Layout
        page_layout = QVBoxLayout()
        page_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll Area
        self.scroll_area = QScrollArea()
        
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Scrollable Content
        self.content = QWidget()
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)
        
        self.content.setLayout(self.main_layout)
        
        self.scroll_area.setWidget(self.content)
        
        page_layout.addWidget(self.scroll_area)
        
        self.setLayout(page_layout)
        
        # Back Button
        self.back_button = QPushButton("🡄 Back")
        self.back_button.clicked.connect(self.go_back)
        
        self.main_layout.addWidget(self.back_button)
        
        # Album Title (Header)
        header_layout = QHBoxLayout()
        
        # Artwork
        self.artwork = QLabel()
        
        self.artwork.setFixedSize(250, 250)
        self.artwork.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Info
        info_layout = QVBoxLayout()
        
        self.album_title = QLabel("Album")
        self.album_title.setStyleSheet("font-size: 28px; font-weight: bold;")
        
        self.artist_label = QLabel("Artist")
        self.artist_label.setStyleSheet("font-size: 18px;")
        
        self.album_info = QLabel("0 songs")
        
        # Play Button
        self.play_button = QPushButton("▶ Play")
        self.play_button.setFixedWidth(120)
        self.play_button.clicked.connect(self.play_album)
        
        info_layout.addStretch()
        info_layout.addWidget(self.album_title)
        info_layout.addWidget(self.artist_label)
        info_layout.addWidget(self.album_info)
        info_layout.addSpacing(20)
        info_layout.addWidget(self.play_button)
        info_layout.addStretch()
        
        header_layout.addWidget(self.artwork)
        header_layout.addSpacing(30)
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        
        self.main_layout.addLayout(header_layout)
        
        # Track List
        self.track_layout = QVBoxLayout()
        self.track_layout.setSpacing(2)
        
        self.main_layout.addLayout(self.track_layout)
        self.main_layout.addStretch()
        
    def play_album(self):
        if self.songs:
            self.play_album_requested.emit(self.songs)
            
    def load_album(self, artist, album, songs, artwork=None):
        self.current_album = album
        self.current_artist = artist
        
        unique_songs = []
        seen_paths = set()
        
        for song in songs:
            if song.path not in seen_paths:
                seen_paths.add(song.path)
                unique_songs.append(song)
        self.songs = unique_songs
        
        # Album info
        self.album_title.setText(album)
        self.artist_label.setText(artist)
        
        total_duration = sum(float(song.duration) for song in songs)
        
        self.album_info.setText(
            f"{len(songs)} songs - "
            f"{self.format_time(total_duration)}"
        )
        
        # Artwork
        self.artwork.clear()
        
        if artwork:
            pixmap = QPixmap()
            
            pixmap.loadFromData(artwork)
            
            pixmap = pixmap.scaled(250, 250,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.artwork.setPixmap(pixmap)
            
        # Remove old tracks
        self.clear_tracks()
        
        # Add tracks
        for index, song in enumerate(self.songs):
            track = self.create_track(index + 1, song)
            
            self.track_layout.addWidget(track)
            
    # Create Track
    def create_track(self, number, song):
        frame = QFrame()
        
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Track Num
        number_label = QLabel(str(number))
        number_label.setFixedWidth(30)
        
        # Track Title
        title_label = QLabel(song.title)
        
        # Track Duration
        duration_label = QLabel(self.format_time(song.duration))
        duration_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        layout.addWidget(number_label)
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(duration_label)
        
        frame.setLayout(layout)
        
        return frame
    
    def clear_tracks(self):
        while self.track_layout.count():
            item = self.track_layout.takeAt(0)
            
            widget = item.widget()
            
            if widget:
                widget.deleteLater()
    
    # Play Album
    def play_album(self):
        if self.songs:
            self.play_album_requested.emit(self.songs)
    
    # Back                    
    def go_back(self):
        self.back_requested.emit()
    
    # Format Track Duration            
    def format_time(self, seconds):
        seconds = int(seconds)
        minutes = seconds // 60
        seconds = seconds % 60
        
        return f"{minutes}:{seconds:02d}"
                
    
            
            