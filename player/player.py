from PyQt6.QtCore import QUrl, QObject, pyqtSignal
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

class MusicPlayer(QObject):
    song_changed = pyqtSignal(str)
    position_changed = pyqtSignal(int)
    duration_changed = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        
        self.player = QMediaPlayer()
        self.audio_output =  QAudioOutput()
        
        self.player.setAudioOutput(self.audio_output)
        self.player.positionChanged.connect(self.position_changed.emit)
        self.player.durationChanged.connect(self.duration_changed.emit)
        
        self.current_song = None
        
    def play_song(self, song):
        self.current_song = song
        
        url = QUrl.fromLocalFile(song.path)
        
        self.player.setSource(url)
        self.player.play()
        
        self.song_changed.emit(song.title)
    
    def toggle_play(self):
        if self.player.isPlaying():
            self.player.pause()
        else:
            self.player.play()
    
    def set_volume(self, value):
        self.audio_output.setVolume(value / 100)
        
    def seek(self, position):
        self.player.setPosition(position)
