import os

from PyQt6.QtWidgets import QMessageBox
from library.metadata import MetadataExtractor

from library.song import Song

SUPPORTED_FORMATS = {
    ".mp3",
    ".flac",
    ".wav",
    ".m4a",
    ".aac",
    ".ogg",
    ".opus"
}

class MusicScanner:
    def __init__(self):
        self.metadata = MetadataExtractor()
    
    def is_music_file(self, filename):
        extension = os.path.splitext(filename)[1].lower()
        
        return extension in SUPPORTED_FORMATS
    
    def scan_folder(self, folder_path):
        
        songs = []
        
        artist, album = self.get_folder_metadata(folder_path)
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if not self.is_music_file(file):
                    continue
                
                full_path = os.path.join(root, file)
                    
                title = os.path.splitext(file)[0]
                
                album_folder = os.path.basename(root)
                artist, album = self.parse_album_folder(album_folder)
                
                metadata = self.metadata.extract(full_path)
                
                # Folder fallback
                if not metadata.get("artist"):
                    metadata["artist"] = artist
                    
                if not metadata.get("album"):
                    metadata["album"] = album
                    
                if not metadata.get("title"):
                    metadata["title"] = title
                    
                songs.append(
                    Song(
                        full_path,
                        metadata["title"],
                        metadata["artist"],
                        metadata["album"],
                        metadata["duration"]
                    )
                )
                                
        
        return songs
    
    def parse_album_folder(self, folder_name):
        if "-" in folder_name:
            parts = folder_name.split("-", 1)
            
            return (parts[0].strip(), parts[1].strip())
        return ("Unknown Artist", folder_name)
    
    def get_folder_metadata(self, folder):
        folder_name = os.path.basename(folder)
        
        # Expected:     "Artist Name" - "Album Name"
        
        if "-" in folder_name:
            parts = folder_name.split(
                "-",
                1
            )
            
            artist = parts[0].strip()
            album = parts[1].strip()
            
            return artist, album
        
        return None, None
                