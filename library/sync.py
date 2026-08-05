import os

from library.scanner import MusicScanner

class LibrarySync:
    def __init__(self, database):
        self.database = database
        self.scanner = MusicScanner()
        
    def sync(self):
        locations = (self.database.get_library_locations())
        
        for location in locations:
            songs = self.scanner.scan_folder(location)
            
            for song in songs:
                self.database.add_song(song)
                
        self.remove_missing_files()
        
    def remove_missing_files(self):
        songs = self.database.get_all_songs()
        
        for song in songs:
            path = song.path
            
            if not os.path.exists(path):
                print("Missing:", path)
                
                self.database.remove_song(path)