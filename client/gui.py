import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


import lib
import json


class Gui(Gtk.Window):
    def __init__(self) -> None:
        super().__init__(title="Discord Soundboard")
        # Set window size
        self.set_default_size(1620, 700)

        self.audios_scrolled_window = Gtk.ScrolledWindow()
        # scroll only vertically
        self.audios_scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.audios_scrolled_window.set_hexpand(True)
        self.audios_scrolled_window.set_vexpand(True)
        self.audios_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.audios_box.set_vexpand(False)
        self.audios_box.set_valign(Gtk.Align.START)
        self.search_audio(Gtk.Entry())

        search_bar = Gtk.Entry()
        search_bar.set_placeholder_text("Search")
        # call search_audio when the user presses enter
        search_bar.connect("activate", self.search_audio)

        # Button with stop icon
        stop_button = Gtk.Button()
        stop_button.set_image(Gtk.Image.new_from_icon_name("media-playback-stop-symbolic", Gtk.IconSize.BUTTON))
        stop_button.set_always_show_image(True)
        stop_button.connect("clicked", self.stop)

        # Button with pause icon
        self.pause_button = Gtk.Button()
        self.pause_button.set_image(Gtk.Image.new_from_icon_name("media-playback-pause-symbolic", Gtk.IconSize.BUTTON))
        self.pause_button.set_always_show_image(True)
        self.paused = False
        self.pause_button.connect("clicked", self.play_pause)

        # Button with refresh icon
        refresh_button = Gtk.Button()
        refresh_button.set_image(Gtk.Image.new_from_icon_name("view-refresh-symbolic", Gtk.IconSize.BUTTON))
        refresh_button.set_always_show_image(True)
        refresh_button.connect("clicked", self.refresh)

        self.grid = Gtk.Grid()
        self.grid.attach(self.audios_scrolled_window, 0, 0, 2, 1)
        self.grid.attach(search_bar, 0, 1, 2, 1)
        self.grid.attach(stop_button, 0, 2, 1, 1)
        self.grid.attach(self.pause_button, 1, 2, 1, 1)
        self.grid.attach(refresh_button, 0, 3, 2, 1)
        self.add(self.grid)
    
    def refresh(self, button):
        self.search_audio(Gtk.Entry())
    
    def stop(self, button):
        lib.stop()
    
    def play_pause(self, button):
        if self.paused:
            lib.resume()
            self.paused = False
            button.set_image(Gtk.Image.new_from_icon_name("media-playback-pause-symbolic", Gtk.IconSize.BUTTON))
        else:
            lib.pause()
            self.paused = True
            button.set_image(Gtk.Image.new_from_icon_name("media-playback-start-symbolic", Gtk.IconSize.BUTTON))
    
    def play_audio(self, button, audio_name, vol):
        lib.stop()
        self.paused = False
        self.pause_button.set_image(Gtk.Image.new_from_icon_name("media-playback-pause-symbolic", Gtk.IconSize.BUTTON))
        lib.vol(vol.get_value()*100)
        lib.play(audio_name)
    
    def vol_changed(self, button, value, audio_name):
        vols = json.load(open('vols.json'))
        if value != 1:
            vols[audio_name] = value*100
        else:
            del vols[audio_name]
        json.dump(vols, open('vols.json', "w"))
    
    def search_audio(self, entry):
        self.audios_box.foreach(self.audios_box.remove)
        vols = json.load(open('vols.json'))
        for element in lib.ls():
            if entry.get_text().lower() in element.lower():
                box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
                title = ".".join(element.split('.')[:-1])
                b = Gtk.Button(label=title)
                box.pack_start(b, True, True, 0)
                vol = Gtk.VolumeButton()
                if element in vols.keys():
                    vol.set_value(vols[element]/100)
                else:
                    vol.set_value(1)
                box.pack_start(vol, False, True, 0)
                self.audios_box.pack_end(box, True, True, 0)
                b.connect("clicked", self.play_audio, element, vol)
                vol.connect("value-changed", self.vol_changed, element)
        self.audios_scrolled_window.foreach(self.audios_scrolled_window.remove)
        self.audios_scrolled_window.add(self.audios_box)
        self.show_all()



win = Gui()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()