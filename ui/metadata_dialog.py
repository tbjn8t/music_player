from PyQt6.QtWidgets import (
    QDialog,
    QLineEdit,
    QLabel,
    QPushButton,
    QVBoxLayout
)

class MetadataDialog(QDialog):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Album Information")
        
        layout = QVBoxLayout()
        
        self.artist_input = QLineEdit()
        self.artist_input.setPlaceholderText("Artist Name")
        
        self.album_input = QLineEdit()
        self.album_input.setPlaceholderText("Album Name")
        
        button = QPushButton("OK")
        button.clicked.connect(self.accept)
        
        layout.addWidget(
            QLabel("Information Not Found\nEnter Album Information")
        )
        
        layout.addWidget(self.artist_input)
        layout.addWidget(self.album_input)
        layout.addWidget(button)
        self.setLayout(layout)
    
    def get_value(self):
        return (
            self.artist_input.text(),
            self.album_input.text()
        )
                