from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QVBoxLayout,
    QToolBar,
    QLabel
)

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog, QStackedWidget

from library.scanner import MusicScanner
from library.database import MusicDatabase
from library.sync import LibrarySync

from player.player import MusicPlayer

from ui.metadata_dialog import MetadataDialog
from ui.library_view import LibraryView
from ui.playback_bar import PlaybackBar
from ui.overview import  AlbumView
from ui.album_detail_view import AlbumDetailView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Music Player")
        self.resize(1000,700)
        
        # Backend
        self.scanner = MusicScanner()
        self.database = MusicDatabase()
        self.library_sync = LibrarySync(self.database)
        self.library_sync.sync()

        # Player
        self.player = MusicPlayer()
        
        # Widget Views
        self.album_view = AlbumView()
        self.album_detail = AlbumDetailView()
        self.library = LibraryView()
        
        # Widget Signals
        self.album_view.album_selected.connect(self.show_album)
        self.album_detail.back_requested.connect(self.show_albums)
        self.album_view.play_album_requested.connect(self.play_album)
        self.album_detail.play_album_requested.connect(self.play_album)
        
        # Pages
        self.pages = QStackedWidget()
        self.pages.addWidget(self.album_view)
        self.pages.addWidget(self.library)
        self.pages.addWidget(self.album_detail)
        
        # UI
        self.create_toolbar()
        self.create_main_area()
        
        # Load Database
        self.all_songs = []
        self.load_library()
        
        # Playback Signals
        self.player.position_changed.connect(self.playback.update_postiion)
        self.player.duration_changed.connect(self.playback.update_duration)
        self.player.current_song_changed.connect(self.playback.update_song)
        self.player.playback_state_changed.connect(self.playback.update_playback_state)
        self.playback.seek_requested.connect(self.player.seek)
        
        self.playback.play.clicked.connect(self.player.toggle_play)
        self.playback.previous.clicked.connect(self.player.play_previous)
        self.playback.next.clicked.connect(self.player.play_next)
        self.playback.update_playback_state(False)
        
    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        
        self.addToolBar(toolbar)
        
        actions = [
            "Open Folder",
            "Open File",
            "Playlists",
            "Albums",
            "Library",
            "Settings",
            "Refresh"
        ]
        
        for action_name in actions:
            action = QAction(action_name, self)
            
            if action_name == "Open Folder":
                action.triggered.connect(self.open_folder)
            if action_name == "Albums":
                action.triggered.connect(self.show_albums)
            if action_name == "Refresh":
                action.triggered.connect(self.refresh)
            if action_name == "Library":
                action.triggered.connect(self.show_library)
            
            toolbar.addAction(action)
    
    def create_main_area(self):
        central_widget = QWidget()
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.pages)
        
        # Playback
        self.playback = PlaybackBar()
        main_layout.addWidget(self.playback)
        
        # Player
        self.library.song_selected.connect(self.play_song)
        
        # Overview Window as Default Widget
        self.pages.setCurrentWidget(self.album_view)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
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
        self.library_sync.sync()
        self.load_library()
            
    def load_library(self):
        songs = self.database.get_all_songs()
        
        self.all_songs = songs
        
        self.library.load_songs(songs)
        self.album_view.load_albums(songs=songs)
        
    def play_song(self, song):
        index = next(
            (i for i, item in enumerate(self.all_songs)
            if item.path == song.path),
            None
        )
        
        if index is None:
            return
        
        self.player.play_queue(self.all_songs, index)
        
    def play_album(self, songs):
        if not songs:
            return
        self.player.play_queue(songs, 0)
        
    def show_albums(self):
        self.pages.setCurrentWidget(self.album_view)
        
    def show_album(self, artist, album, songs, artwork):
        self.album_detail.load_album(artist, album, songs, artwork)
        self.pages.setCurrentWidget(self.album_detail)
        
    def show_library(self):
        self.pages.setCurrentWidget(self.library)