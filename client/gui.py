#! /usr/bin/python3
from PySide2 import QtCore, QtGui, QtWidgets
from lib import Client
import json


config = json.load(open('config.json'))

host = config['serverAddress'].split(':')[0]
port = int(config['serverAddress'].split(':')[1])

client = Client(host, port)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello World")
        self.audio_scroll_area = QtWidgets.QScrollArea()
        self.audio_frame = QtWidgets.QFrame()
        self.audio_scroll_area.setWidget(self.audio_frame)
        self.audio_scroll_area.setWidgetResizable(True)
        self.audio_frame.setLayout(QtWidgets.QVBoxLayout())
        self.audio_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.audio_frame.layout().setSpacing(0)
        self.audio_frame.layout().setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.audio_scroll_area)
        self.audio_widget_list = []
        self.control_frame = QtWidgets.QFrame()
        self.control_frame.setLayout(QtWidgets.QHBoxLayout())
        self.control_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.control_frame.layout().setSpacing(0)
        self.layout().addWidget(self.control_frame)
        self.search_box = QtWidgets.QLineEdit()
        self.search_box.textChanged.connect(self.search)
        self.control_frame.layout().addWidget(self.search_box)
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.stop_button.clicked.connect(client.stop)
        self.control_frame.layout().addWidget(self.stop_button)
        self.pause_play_button = QtWidgets.QPushButton("Pause")
        self.pause_play_button.clicked.connect(self.pause_play)
        self.control_frame.layout().addWidget(self.pause_play_button)
        self.refresh_button = QtWidgets.QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh)
        self.control_frame.layout().addWidget(self.refresh_button)
        self.refresh()
    
    def refresh(self):
        self.ls_result = client.ls()
        self.search()
    
    def pause_play(self):
        if self.pause_play_button.text() == "Pause":
            self.pause_play_button.setText("Resume")
            client.pause()
        else:
            self.pause_play_button.setText("Pause")
            client.resume()
    
    def stop(self):
        client.stop()
        self.pause_play_button.setText("Pause")
    
    def search(self):
        volumes = json.load(open('vols.json'))
        for widget in self.audio_widget_list:
            self.audio_frame.layout().removeWidget(widget)
            widget.deleteLater()
        self.audio_widget_list = []
        query = self.search_box.text()
        for i in self.ls_result:
            if query.lower() in i.lower():
                vol = volumes[i] if i in volumes else 100
                self.audio_widget_list.append(AudioWidget(i, vol))
                self.audio_frame.layout().addWidget(self.audio_widget_list[-1])
                

class AudioWidget(QtWidgets.QFrame):
    def __init__(self, audio_name, volume):
        super().__init__()
        self.button = QtWidgets.QPushButton(".".join(audio_name.split('.')[:-1]))
        self.button.clicked.connect(self.play)
        self.volume = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.volume.setMinimum(0)
        self.volume.setMaximum(200)
        self.volume.setValue(volume)
        self.volume.setFixedWidth(100)
        self.volume.valueChanged.connect(self.volChange)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.volume)
        self.setLayout(self.layout)
        self.audio_name = audio_name
    
    def play(self):
        client.stop()
        client.vol(self.volume.value())
        client.play(self.audio_name)
    
    def volChange(self):
        vols = json.load(open('vols.json'))
        vols[self.audio_name] = self.volume.value()
        json.dump(vols, open('vols.json', 'w'))



app = QtWidgets.QApplication([])
window = Window()
window.showMaximized()
app.exec_()