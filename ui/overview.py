from PyQt6.QtWidgets import QWidget, QGridLayout, QScrollArea

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap

from library.artwork import ArtworkExtractor
from ui.album_card import AlbumCard

class AlbumView(QWidget):
    album_selected = pyqtSignal(str, str, object, object)
    play_album_requested = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
                
        self.artwork_extractor = ArtworkExtractor()
        
        self.column_count = 1
        self.album_cards = []
        
        self.setup_ui()
        
    def setup_ui(self):
        #Scroll Area
        self.scroll_area = QScrollArea()
        
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Container inside scroll area
        self.container = QWidget()
        
        # Album Grid
        self.layout = QGridLayout()
        
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(20)
        
        self.container.setLayout(self.layout)
        
        # Container inside scroll area
        self.scroll_area.setWidget(self.container)
        
        # Main layout
        main_layout = QGridLayout()
        
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)
        
    def clear_albums(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        self.album_cards.clear()
                
    def load_albums(self, songs):
        self.clear_albums()
        
        # Group by artist and album
        albums = {}
        for song in songs:
            key = (song.artist, song.album)
            
            if key not in albums:
                albums[key] = []
            albums[key].append(song)
            
        # Album Cards    
        for key, album_songs in albums.items():
            artist, album = key
            
            first_song = album_songs[0]
            
            artwork = self.artwork_extractor.get_artwork(first_song.path)
            
            card = AlbumCard(album, artist, album_songs, artwork)
            
            card.clicked.connect(self.album_clicked)
            card.play_requested.connect(self.request_play_album)
            self.album_cards.append(card)
        
        # Find column count and display cards    
        self.update_columns()
        self.rebuild_grid()
            
    def update_columns(self):
        card_width = 180
        spacing = 20
        
        available_width = (self.scroll_area.viewport().width())
        
        self.column_count = max(1, available_width // (card_width + spacing))
        
    def rebuild_grid(self):
        # Remove cards from layout
        while self.layout.count():
            self.layout.takeAt(0)
            
        # Re-add cards using new column count
        for index, card in enumerate(self.album_cards):
            row = index // self.column_count
            
            column = index % self.column_count
            
            self.layout.addWidget(card, row, column)
        
    def resizeEvent(self, event):
        self.update_columns()
        
        self.rebuild_grid()
        
        super().resizeEvent(event)
        
    def album_clicked(self, card):
        self.album_selected.emit(
            card.artist,
            card.album,
            card.songs,
            self.artwork_extractor.get_artwork(card.songs[0].path)
        )
        
    def request_play_album(self, songs):
        self.play_album_requested.emit(songs)