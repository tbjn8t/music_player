import os
import subprocess
import tempfile

from mutagen import File
from mutagen.flac import FLAC
from mutagen.wave import WAVE

def get_wav_artwork(path):
    audio = WAVE(path)
    
    if audio.tags:
        for tag in audio.tags.values():
            
            if hasattr(tag, "data"):
                return tag.data
    return None


class ArtworkExtractor:
    def get_artwork(self, path):
        if not os.path.exists(path):
            return None
        
        try:
            audio = File(path)
        except Exception as e:
            print(f"Could not read artwork: {path}")
            print(e)
            return None
        
        if audio is None:
            return None
        
        if audio is None:
            return self.find_folder_art(path)
        
        # FLAC embedded artwork
        if isinstance(audio, FLAC):
            if audio.pictures:
                return audio.pictures[0].data
            
        # WAV Embedded Artwork
        if isinstance(audio, WAVE):
            artwork = get_wav_artwork(path)
            if artwork:
                return artwork
        
        # MP3 Embedded Art        
        if audio.tags:
            for tag in audio.tags.values():
                if hasattr(tag, "data"):
                    return tag.data
                    
        return self.find_folder_art(path)
    
    def find_folder_art(self, path):
        folder = os.path.dirname(path)
        
        image_extensions = [
            ".jpg",
            ".jpeg",
            ".png"
        ]
        
        for file in os.listdir(folder):
            
            file_path = os.path.join(folder, file)
            
            # Skip directories
            if not os.path.isfile(file_path):
                continue
            
            # Check extension
            if file.lower().endswith(tuple(image_extensions)):
                with open(file_path, "rb") as f:
                    return f.read()
        
        return None
    

    
