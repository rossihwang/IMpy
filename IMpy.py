import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gui import IMpyMainWindow

if __name__ == "__main__":
    win = IMpyMainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()