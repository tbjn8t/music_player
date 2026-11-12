from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QSlider,
    QHBoxLayout,
    QVBoxLayout
)

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QByteArray
from PyQt6.QtCore import Qt, pyqtSignal

from library.artwork import ArtworkExtractor

class PlaybackBar(QWidget):
    seek_requested = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        
        self.duration = 0
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QHBoxLayout()
        
        # Album Cover
        self.album_cover = QLabel("Album\nCover") 
        self.album_cover.setFixedSize(100, 100)
        self.album_cover.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        
        # Song Information
        song_layout = QVBoxLayout()
        
        self.song_title = QLabel("No Song Playing")
        self.artist = QLabel("Unknown Artist")
        
        self.progress = QSlider(Qt.Orientation.Horizontal)
        self.progress.setRange(0, 100)
        
        self.runtime = QLabel("0:00 / 0:00")       
        
        song_layout.addWidget(self.song_title)
        song_layout.addWidget(self.artist)
        song_layout.addWidget(self.progress)
        song_layout.addWidget(self.runtime) 
        
        # Playback Controls
        controls_layout = QHBoxLayout()
        
        self.previous = QPushButton("⏮")
        self.play = QPushButton("▶")
        self.next = QPushButton("⏭")
        
        self.play.setFixedSize(45, 45)
        self.previous.setFixedSize(60, 45)
        self.next.setFixedSize(60, 45)
        
        controls_layout.addWidget(self.previous)
        controls_layout.addWidget(self.play)
        controls_layout.addWidget(self.next)
        
        main_layout.addWidget(self.album_cover)
        main_layout.addLayout(song_layout)
        main_layout.addLayout(controls_layout)
        
        self.setLayout(main_layout)
        self.setFixedHeight(130)
        
        self.progress.sliderMoved.connect(self.slider_moved)
    
    def update_song(self, song):
        self.song_title.setText(song.title)
        self.artist.setText(song.artist)
        
        artwork = ArtworkExtractor().get_artwork(song.path)
        
        if artwork:
            pixmap = QPixmap()
            
            pixmap.loadFromData(artwork)
            
            self.album_cover.setPixmap(pixmap.scaled(100, 100))
            
    def update_playback_state(self, is_playing):
        if is_playing:
            self.play.setText("⏸")
        else:
            self.play.setText("▶")
            
    def update_postiion(self, postiion):
        self.progress.blockSignals(True)
        self.progress.setValue(postiion)
        self.progress.blockSignals(False)
        
        self.update_runtime(postiion, self.duration)
    
    def update_duration(self,duration):
        self.duration = duration
        
        self.progress.setRange(0, duration)
        self.update_runtime(0, duration)
        
    def update_runtime(self, current, total):
        current_seconds = current // 1000
        total_seconds = total // 1000
        
        current_minutes = current_seconds // 60
        current_seconds = current_seconds % 60
        
        total_minutes = total_seconds // 60
        total_seconds = total_seconds % 60
        
        self.runtime.setText(
            f"{current_minutes}:{current_seconds:02d} / "
            f"{total_minutes}:{total_seconds:02d}"
        )
        
    def slider_moved(self, position):
        self.seek_requested.emit(position)
        