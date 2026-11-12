import os

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
        
        # Normalize library folder path
        folder_path = os.path.abspath(
            os.path.normpath(folder_path)
        )
                
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if not self.is_music_file(file):
                    continue
                
                # Build normalized path
                full_path = os.path.abspath(
                    os.path.normpath(os.path.join(root, file))
                )
                    
                title = os.path.splitext(file)[0]
                
                # Use library folder containing the music files
                album_folder = os.path.basename(root)
                artist, album = self.parse_album_folder(album_folder)
                
                # Extract metadata from file
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
                