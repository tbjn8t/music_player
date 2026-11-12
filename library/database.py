import sqlite3
import os

from library.song import Song

class MusicDatabase:
    def __init__(self, db_path="data/music.db"):
        self.db_path = db_path
        
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.connection = sqlite3.connect(self.db_path)
        
        self.create_tables()
        
    def create_tables(self):
        cursor = self.connection.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE,
            title TEXT,
            artist TEXT,
            album TEXT,
            duration REAL,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS library_locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        self.connection.commit()
        
    def add_song(self, song):
        cursor = self.connection.cursor()
        
        cursor.execute("""
        INSERT INTO songs
        (
                path,
                title,
                artist,
                album,
                duration
        )
        
        VALUES (?, ?, ?, ?, ?)
        
        ON CONFLICT(path) DO UPDATE SET
            title = excluded.title,
            artist = excluded.artist,
            album = excluded.album,
            duration = excluded.duration
        """,
        (
            song.path,
            song.title,
            song.artist,
            song.album,
            song.duration
        ))
        
        self.connection.commit()
        
    def remove_song(self, path):
        cursor = self.connection.cursor()
        
        cursor.execute("""
        DELETE FROM songs
        WHERE path = ?
        """,
        (path,))
        
        self.connection.commit()
        
    def get_all_songs(self):
        cursor = self.connection.cursor()
        
        cursor.execute("""
        SELECT  
            title, 
            artist, 
            album,
            duration,
            path
        FROM songs
        ORDER BY artist, album, title
        """)
        
        rows = cursor.fetchall()
        
        songs = []
        
        for row in rows:
            songs.append(
                Song(
                    path=row[4],
                    title=row[0],
                    artist=row[1],
                    album=row[2],
                    duration=row[3]
                )
            )
        
        return songs
    
    def add_library_location(self, folder):
        cursor = self.connection.cursor()
        
        cursor.execute("""
        INSERT OR IGNORE INTO library_locations
        (path)
        
        VALUES (?)
        """,
        (folder,))
        
        self.connection.commit()
        
    def get_library_locations(self):
        cursor = self.connection.cursor()
        
        cursor.execute("""
        SELECT path
        FROM library_locations
        """)
        
        return [
            row[0] for row in cursor.fetchall()
        ]