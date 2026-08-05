from mutagen import File

class MetadataExtractor:
    def extract(self, file_path):
        audio = File(file_path, easy=True)
        
        if audio is None:
            return {}
        
        metadata = {}
        
        metadata["title"] = self.get_value(audio, "title")
        metadata["artist"] = self.get_value(audio, "artist")
        metadata["album"] = self.get_value(audio, "album")
        
        if audio.info:
            metadata["duration"] = audio.info.length
        else:
            metadata["duration"] = 0
            
        return metadata
    
    def get_value(self, audio, key):
        value = audio.get(key)
        
        if value:
            return value[0]
        
        return None
        