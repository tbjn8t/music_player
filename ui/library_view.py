from PyQt6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
)

from PyQt6.QtCore import pyqtSignal

class LibraryView(QTableWidget):
    song_selected = pyqtSignal(object)
    
    def __init__(self):
            super().__init__()
            
            self.setup_ui()
            self.songs = []
            
    def setup_ui(self):
        # Number of rows initially
        self.setRowCount(0)
        
        # Columns
        columns = [
            "Title",
            "Artist",
            "Ablum",
            "Length"
        ]
        
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)
        
        # Make columns stretch
        self.horizontalHeader().setStretchLastSection(True)
        
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)
        
        self.cellDoubleClicked.connect(self.select_song)
    
    def load_songs(self, songs):
        self.songs = songs
        self.setRowCount(0)
        
        for song in songs:
            row = self.rowCount()
            
            self.insertRow(row)
            
            values = [
                song.title,
                song.artist,
                song.album,
                self.format_time(song.duration)
            ]
            
            for column, value in enumerate(values):
                self.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(value))
                )
                
    def format_time(self, seconds):
        if seconds is None:
            return "0:00"
        
        try:
            seconds = float(seconds)
        except ValueError:
            return "0:00"
        
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        
        return f"{minutes}:{seconds:02d}"
    
    def select_song(self, row, column):
        song = self.songs[row]
        
        self.song_selected.emit(song)