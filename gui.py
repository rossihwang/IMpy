import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

VER = 0.1

class Plane(Gtk.Box):

    def __init__(self, label):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.__label = label
        self.set_border_width(5)

        self.leftBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.leftBox.add(Gtk.Label(self.__label))
        self.pack_start(self.leftBox, True, True, 0)

        self.rightBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        self.imgBox = Gtk.Box()
        self.imgBox.set_border_width(10)

        self.rightBox.add(self.imgBox)
         
        self.pack_start(self.rightBox, True, True, 0)

        self.confirmButton = Gtk.Button("Confirm")
        # self.confirmButton.connect("")

        self.leftBox.pack_end(self.confirmButton, False, False, 0)
    
    def add_entry(self):
        '''
        Add entries to left box for parameters input. 
        '''
        pass

    def disp_img(self, img):
        '''
        Display the image on the right box.
        '''
        self.imgBox.pack_start(Gtk.Image(file=img), True, True, 0)
    
    def emu_result(self):
        pass

    def on_confirm_button(self):
        '''
        When the confirm button pressed, do the calculation.
        '''
        pass


class IMpyWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="IMpy Ver." + str(VER))
        self.set_default_size(800, 600)
        self.set_border_width(5)
        
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.page1 = Plane("L circuit")
        self.page1.disp_img("../lena.jpg")
        self.notebook.append_page(self.page1, Gtk.Label("L circuit"))
        self.page2 = Plane("Pi circuit")
        self.notebook.append_page(self.page2, Gtk.Label("Pi circuit"))
        self.page3 = Plane("T circuit")
        self.notebook.append_page(self.page3, Gtk.Label("T circuit"))
        self.page4 = Plane("Tapped Cap")
        self.notebook.append_page(self.page4, Gtk.Label("Tapped Cap"))
        # self.page5 = Plane("Help")
        # self.notebook.append_page(self.page5, Gtk.Label("Help"))

if __name__ == "__main__":
    win = IMpyWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
