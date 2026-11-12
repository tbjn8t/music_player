from PyQt6.QtCore import QUrl, QObject, pyqtSignal
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

class MusicPlayer(QObject):
    song_changed = pyqtSignal(str)
    current_song_changed = pyqtSignal(object)
    position_changed = pyqtSignal(int)
    playback_state_changed = pyqtSignal(bool)
    duration_changed = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        
        self.player = QMediaPlayer()
        self.audio_output =  QAudioOutput()
        
        self.player.setAudioOutput(self.audio_output)
        
        self.player.playbackStateChanged.connect(self.on_playback_state_changed)
        self.player.positionChanged.connect(self.position_changed.emit)
        self.player.durationChanged.connect(self.duration_changed.emit)
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)
        
        self.current_song = None
        self.queue = []
        self.queue_index = -1
    
    def play_queue(self, songs, start_index=0):
        if not songs:
            return
        if start_index < 0 or start_index >= len(songs):
            return
        self.queue = list(songs)
        self.queue_index = start_index
        
        self.play_current_song()
            
    def play_current_song(self):
        if not self.queue:
            return
        
        self.current_song = self.queue[self.queue_index]
        url = QUrl.fromLocalFile(self.current_song.path)
        
        self.player.setSource(url)
        self.player.play()
        
        self.song_changed.emit(self.current_song.title)
        self.current_song_changed.emit(self.current_song)
        
    def play_next(self):
        if self.queue_index < len(self.queue) -1:
            self.queue_index += 1
            self.play_current_song()
    
    def play_previous(self):
        if self.player.position() > 3000:
            self.player.setPosition(0)
            return
        
        if self.queue_index > 0:
            self.queue_index -= 1
            self.play_current_song()
    
    def toggle_play(self):
        if self.player.isPlaying():
            self.player.pause()
        else:
            self.player.play()
    
    def on_playback_state_changed(self, state):
        is_playing = (state == QMediaPlayer.PlaybackState.PlayingState)
        
        self.playback_state_changed.emit(is_playing)
        
    def on_media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.play_next()
    
    def set_volume(self, value):
        self.audio_output.setVolume(value / 100)
        
    def seek(self, position):
        self.player.setPosition(position)
