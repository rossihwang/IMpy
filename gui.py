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
        self.inputList = [] # Store the input entry objects
        self.outputList = [] # Store the output entry objects
        
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

    def add_param_entry(self, label, isInput):
        '''
        Add entries to left box for parameters input. 
        '''
        pe = IMpyParamEntry(label, isInput) # when input, it's editable
        row = Gtk.ListBoxRow()

        if isInput == True:
            self.inputList.append(pe)
            row.add(pe)
            self.inputListBox.add(row)
        else:
            self.outputList.append(pe)
            row.add(pe)
            self.outputListBox.add(row)

    def add_combo_box(self, label, comboList):
        pc = IMpyParamComboBox(label, comboList)
        row = Gtk.ListBoxRow()
        self.inputList.append(pc)
        row.add(pc)
        self.inputListBox.add(row)
        print("hello")
    
    def disp_result(self):
        labelStr = {'L': ['Q', 'L', 'C'], 
                    'pi_hp': ['Q', 'L1', 'L2', 'C1'], 
                    'pi_lp': ['Q', 'L1', 'C1', 'C2'], 
                    'T_hp': ['Q', 'L1', 'C1', 'C2'], 
                    'T_lp': ['Q', 'L1', 'L2', 'C1'], 
                    'TappedCap': ['Q', 'L1', 'C1', 'C2']}
        if len(self.outputEntryList) > 0:
            self.outputEntryList[0].set_text("hello")

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
        inputVal = []
        for pe in self.inputList:
            inputVal.append(float(pe.get_text()))
        print(inputVal)
        if self.__label == "L circuit":
            pass
        elif self.__label == "Pi circuit":
            pass
        elif self.__label == "T circuit":
            pass
        elif self.__label == "Tapped Cap":
            pass
        else:
            pass
        
class IMpyParamEntry(Gtk.Box):
    
    def __init__(self, label, isEditable):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True, spacing=10)
        self.lb = Gtk.Label(label)
        self.lb.set_alignment(0.5, 0) # misc method
        self.pack_start(self.lb, True, True, 0)
        self.et = Gtk.Entry()
        self.et.set_editable(isEditable)
        self.pack_start(self.et, True, True, 0)
    
    def set_text(self, string):
        self.et.set_text(string)

    def get_text(self):
        return self.et.get_text()

class IMpyParamComboBox(Gtk.Box):

    def __init__(self, label, comboList):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True, spacing=10)
        self.lb = Gtk.Label(label)
        self.lb.set_alignment(0.5, 0)
        self.pack_start(self.lb, True, True, 0)
        self.listStore = Gtk.ListStore(str)
        for i in comboList:
            self.listStore.append([i])
        self.combo = Gtk.ComboBox.new_with_model(self.listStore)
        renderer_text = Gtk.CellRendererText()
        self.combo.pack_start(renderer_text, True)
        self.combo.add_attribute(renderer_text, "text", 0)
        self.pack_start(self.combo, False, True, True)

    def get_text(self):
        iter = self.combo.get_active_iter()
        if iter != None:
            return self.listStore[iter]

class IMpyMainWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="IMpy(ver." + str(VER)+')')
        self.set_default_size(800, 600)
        self.set_border_width(5)
        
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        ### Add page for L
        self.page1 = IMpyPage("L circuit")
        ### Add default image
        self.page1.disp_img("../lena.jpg")
        ### Input Entries
        self.page1.add_param_entry("Rs", True)
        self.page1.add_param_entry("Rl", True)
        self.page1.add_param_entry("f0(MHz)", True)
        # self.page1.add_param_entry("Circuit type", True)
        self.page1.add_combo_box("Circuit type", ["high-pass", "low-pass"])
        ### Output Entries
        self.page1.add_param_entry("Q", False)
        self.page1.add_param_entry("L", False)
        self.page1.add_param_entry("C", False)
        self.notebook.append_page(self.page1, Gtk.Label("L"))
        ###
        ### Add page for Pi
        self.page2 = IMpyPage("Pi circuit")
        ### Add default image
        ### Input Entries
        self.page2.add_param_entry("Rs", True)
        self.page2.add_param_entry("Rl", True)
        self.page2.add_param_entry("f0(MHz)", True)
        self.page2.add_param_entry("Desired Q", True)
        self.page2.add_param_entry("Circuit type", True)
        ### Output Entries
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
