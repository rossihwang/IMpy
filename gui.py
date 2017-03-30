import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import matching

VER = 0.2

class IMpyPage(Gtk.Box):

    def __init__(self, label):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.__label = label
        self.set_border_width(10)
        
        ### Setting the boxes
        self.leftVBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.rightVBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.pack_start(self.leftVBox, True, True, 0)
        self.pack_start(self.rightVBox, True, True, 0)

        ### Setting the frames
        self.topLeftFrame = Gtk.Frame()
        self.topLeftFrame.set_label("Input")
        self.topLeftFrame.set_label_align(0.5, 0.5)

        self.bottomLeftFrame = Gtk.Frame()
        self.bottomLeftFrame.set_label("Output")
        self.bottomLeftFrame.set_label_align(0.5, 0.5)

        self.rightFrame = Gtk.Frame()
        self.rightFrame.set_label("Image")
        self.rightFrame.set_label_align(0.5, 0.5)
        self.leftVBox.pack_start(self.topLeftFrame, True, True, 0)
        self.leftVBox.pack_start(self.bottomLeftFrame, True, True, 0)
        self.rightVBox.pack_start(self.rightFrame, True, True, 0)

        ### Setting input box
        self.topLeftBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.inputListBox = Gtk.ListBox()
        self.confirmButton = Gtk.Button("Confirm")
        self.confirmButton.connect("clicked", self.on_confirm_button)
        self.topLeftFrame.add(self.topLeftBox)
        self.topLeftBox.pack_start(self.inputListBox, True, True, 0)
        self.topLeftBox.pack_start(self.confirmButton, False, True, 0)
        ## Setting the output box
        self.outputListBox = Gtk.ListBox()
        self.bottomLeftFrame.add(self.outputListBox)
        ## Setting the image box
        self.imgBox = Gtk.Alignment(xalign=0.5, yalign=0.1, xscale=0, yscale=0) 
        self.rightFrame.add(self.imgBox)

    def add_entry(self, label, isInput):
        '''
        Add entries to left box for parameters input. 
        '''
        entry = IMpyParaBox(label)
        row = Gtk.ListBoxRow()
        row.add(entry)

        if isInput == True:
            self.inputListBox.add(row)
        else:
            self.outputListBox.add(row)
    
    def disp_result(self, ):
        pass

    def disp_img(self, img):
        '''
        Display the image on the right box.
        '''
        self.imgBox.add(Gtk.Image(file=img))
    
    def sim_result(self):
        pass

    def on_confirm_button(self, button):
        '''
        When the confirm button pressed, do the calculation.
        '''
        print(self.__label)
        '''
        if self.__label == "L circuit":
            pass
        elif self.__label == "Pi circuit":
            pass
        elif self.__label == "T circuit":
            pass
        elif self.__label == "Tapped Cap":
            pass
        else:
            raise()
        '''
class IMpyParaBox(Gtk.Box):
    
    def __init__(self, label):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True, spacing=10)
        l = Gtk.Label(label)
        l.set_alignment(0.5, 0) # misc method
        self.pack_start(l, True, True, 0)
        e = Gtk.Entry()
        self.pack_start(e, True, True, 0)

class IMpyMainWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="IMpy(ver." + str(VER)+')')
        self.set_default_size(800, 600)
        self.set_border_width(5)
        
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.page1 = IMpyPage("L circuit")
        self.page1.disp_img("../lena.jpg")
        self.page1.add_entry("Rs", True)
        self.page1.add_entry("Rl", True)
        self.page1.add_entry("f0(MHz)", True)
        self.page1.add_entry("Circuit type", True)
        self.notebook.append_page(self.page1, Gtk.Label("L"))

        self.page2 = IMpyPage("Pi circuit")
        self.page2.add_entry("Rs", True)
        self.page2.add_entry("Rl", True)
        self.page2.add_entry("f0(MHz)", True)
        self.page2.add_entry("Desired Q", True)
        self.page2.add_entry("Circuit type", True)
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
