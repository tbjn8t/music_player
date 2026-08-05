class Song:
    def __init__(
        self,
        path,
        title=None,
        artist=None,
        album=None,
        duration=0,
        artwork=None
    ):
        self.path = path
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.artwork = artwork
        
    def __str__(self):
        return (
            f"{self.artist} - "
            f"{self.album} - "
            f"{self.title}"
        )