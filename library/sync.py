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
        locations = self.database.get_library_locations()
        
        valid_locations = [
            os.path.abspath(os.path.normpath(location))
            for location in locations
            if os.path.exists(location)
        ]
        
        songs = self.database.get_all_songs()
        
        missing_paths = []
        for song in songs:
            path = os.path.abspath(os.path.normpath(song.path))
            
            if not os.path.exists(path):
                belongs_to_library = any(
                    os.path.commonpath([path, location]) == location
                    for location in valid_locations
                )
                
                if belongs_to_library:
                    missing_paths.append(song.path)
        for path in missing_paths:
            print("Removing:", path)
            self.database.remove_song(path)