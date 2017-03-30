import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

VER = 0.1

class IMpyPage(Gtk.Box):

    def __init__(self, label):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.__label = label
        self.set_border_width(5)
        
        ### Setting the frames
        self.leftFrame = Gtk.Frame()
        self.leftFrame.set_label("Input")
        self.leftFrame.set_label_align(0.5, 0.5)
        self.rightFrame = Gtk.Frame()
        self.rightFrame.set_label("Output")
        self.rightFrame.set_label_align(0.5, 0.5)
        self.pack_start(self.leftFrame, True, True, 0)
        self.pack_start(self.rightFrame, True, True, 0)

        ### Setting parameter box and image box
        # self.paraBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        # self.leftFrame.add(self.paraBox)
        self.paraBox = Gtk.ListBox()
        self.paraBox.set_selection_mode(Gtk.SelectionMode.NONE) # ???
        self.leftFrame.add(self.paraBox)
        self.imgBox = Gtk.Alignment(xalign=0.5, yalign=0.1, xscale=0, yscale=0) 
        self.rightFrame.add(self.imgBox)

        self.confirmButton = Gtk.Button("Confirm")
        # self.confirmButton.connect("")
        # self.paraBox.pack_end(self.confirmButton, False, False, 0)
    
    def add_entry(self, label):
        '''
        Add entries to left box for parameters input. 
        '''
        entry = IMpyParaBox(label)
        row = Gtk.ListBoxRow()
        row.add(entry)
        self.paraBox.add(row)

    def disp_img(self, img):
        '''
        Display the image on the right box.
        '''
        self.imgBox.add(Gtk.Image(file=img))
    
    def sim_result(self):
        pass

    def on_confirm_button(self):
        '''
        When the confirm button pressed, do the calculation.
        '''
        pass

class IMpyParaBox(Gtk.Box):
    
    def __init__(self, label):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        self.pack_start(Gtk.Label(label), True, True, 0)
        self.pack_start(Gtk.Entry(), True, True, 0)

class IMpyMainWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="IMpy(ver." + str(VER)+')')
        self.set_default_size(800, 600)
        self.set_border_width(5)
        
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.page1 = IMpyPage("L circuit")
        self.page1.disp_img("../lena.jpg")
        self.page1.add_entry("hello")
        self.page1.add_entry("world")
        self.page1.add_entry("dddddddddddddddddddddddd")
        self.notebook.append_page(self.page1, Gtk.Label("L"))

        self.page2 = IMpyPage("Pi circuit")
        self.page2.add_entry("hhhhllll")
        self.notebook.append_page(self.page2, Gtk.Label("Pi"))

        self.page3 = IMpyPage("T circuit")
        self.notebook.append_page(self.page3, Gtk.Label("T"))

        self.page4 = IMpyPage("Tapped Cap")
        self.notebook.append_page(self.page4, Gtk.Label("Tapped Cap"))

if __name__ == "__main__":
    win = IMpyMainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
