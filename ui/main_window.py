from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QVBoxLayout,
    QToolBar,
    QLabel
)

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog

from library.scanner import MusicScanner
from library.database import MusicDatabase
from library.sync import LibrarySync

from player.player import MusicPlayer

from ui.metadata_dialog import MetadataDialog
from ui.library_view import LibraryView
from ui.playback_bar import PlaybackBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Music Player")
        
        self.resize(1000,700)
        
        self.create_toolbar()
        self.create_main_area()
        self.scanner = MusicScanner()
        self.database = MusicDatabase()
        self.load_library()
        self.sync = LibrarySync(self.database)
        self.player = MusicPlayer()
        
        self.player.position_changed.connect(self.playback.update_postiion)
        self.player.duration_changed.connect(self.playback.update_duration)
        self.playback.seek_requested.connect(self.player.seek)
        
        self.playback.pause.clicked.connect(self.player.toggle_play)
        self.playback.play.clicked.connect(self.player.toggle_play)
        
    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        
        self.addToolBar(toolbar)
        
        actions = [
            "Open Folder",
            "Open File",
            "Playlists",
            "Proflie",
            "Settings",
            "Refresh"
        ]
        
        for action_name in actions:
            action = QAction(action_name, self)
            
            if action_name == "Open Folder":
                action.triggered.connect(self.open_folder)
            if action_name == "Refresh":
                action.triggered.connect(self.refresh)
            
            toolbar.addAction(action)
    
    def create_main_area(self):
        central_widget = QWidget()
        
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Library
        self.library = LibraryView()
        layout.addWidget(self.library)
        
        # Playback
        self.playback = PlaybackBar()
        layout.addWidget(self.playback)
        
        # Player
        self.library.song_selected.connect(self.play_song)
        
        central_widget.setLayout(layout)
        
    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Music Folder")
        
        if folder:
            self.database.add_library_location(folder)
            songs = self.scanner.scan_folder(folder)
            
            print(f"Found {len(songs)} songs")
            
            for song in songs:
                print(
                    song.title,
                    song.duration,
                    type(song.duration)
                )
                self.database.add_song(song)
            
            self.load_library()
            
            print(f"Imported {len(songs)} songs")
    
    def refresh(self):
        self.sync.sync()
        self.load_library()
            
    def load_library(self):
        songs = self.database.get_all_songs()
        
        self.library.load_songs(songs)
        
    def play_song(self, song):
        self.player.play_song(song)
        self.playback.update_song(song)