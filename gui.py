import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import matching

VER = 0.5

class IMpyPage(Gtk.Box):

    def __init__(self, label, window):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.__label = label
        self.set_border_width(10)
        self.inputList = [] # Store the input entry objects
        self.outputList = [] # Store the output entry objects
        self.lastCircuitType = None
        self.circuitImg = Gtk.Image()
        self.win = window
        
        ### Setting the vertical boxes on the right and left
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
        self.rightFrame.set_label("Circuit")
        self.rightFrame.set_label_align(0.5, 0.5)

        self.leftVBox.pack_start(self.topLeftFrame, True, True, 0)
        self.leftVBox.pack_start(self.bottomLeftFrame, True, True, 0)
        self.rightVBox.pack_start(self.rightFrame, True, True, 0)

        ### Setting input box
        self.topLeftBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.inputListBox = Gtk.ListBox()
        self.clearButton = Gtk.Button("Clear")
        self.clearButton.connect("clicked", self.on_clear_button)
        self.confirmButton = Gtk.Button("Confirm")
        self.confirmButton.connect("clicked", self.on_confirm_button)
        self.topLeftFrame.add(self.topLeftBox)
        self.topLeftBox.pack_start(self.inputListBox, True, True, 0)
        self.topLeftBox.pack_start(self.clearButton, False, True, 0)
        self.topLeftBox.pack_start(self.confirmButton, False, True, 0)

        ## Setting the output box
        self.outputListBox = Gtk.ListBox()
        self.bottomLeftFrame.add(self.outputListBox)

        ## Setting the image box
        self.imgBox = Gtk.Alignment(xalign=0.5, yalign=0.1, xscale=0, yscale=0) 
        self.imgBox.add(self.circuitImg)
        self.rightFrame.add(self.imgBox)
        
    def add_param_entry(self, label, isInput):
        '''
        Add entries to left box for parameters input. 
        '''
        pe = IMpyParamEntry(label, isInput) # when its input, its editable
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
    
    def disp_result(self, *result, tp):
        '''
        Fill the result into the output entries
        '''
        ### Output numerical result
        if len(result[0]) > 0 and len(result[0]) == len(self.outputList):
            for i in range(len(result[0])):
                self.outputList[i].set_entry_text("{0:.2e}".format(result[0][i]))
        else:
            print(result)
            print("length of result is " + str(len(result)))
            print("length of outputList is " + str(len(self.outputList)))
        ### Update Circuit image
        tp = '_'+tp if tp != None else ''
        self.disp_circuit_img("./img/{0}{1}.png".format(self.__label, tp))

    def disp_circuit_img(self, img):
        '''
        Display the image on the right box.
        '''
        self.circuitImg.set_from_file(img)
            
    def sim_result(self, *result, tp):
        pass

    def on_confirm_button(self, button):
        '''
        When the confirm button pressed, do the calculation.
        This is not a good OO design!!!
        '''
        inputVal = []
        for pe in self.inputList:
            v = pe.get_entry_text() if isinstance(pe, IMpyParamEntry) else pe.get_combo_text()
            inputVal.append(v)
        try:
            if self.__label == "L":
                Rs, Rl, f0, tp = inputVal
                result = matching.L_matching(float(Rs), float(Rl), float(f0), tp)
                self.disp_result(result, tp=tp)
            elif self.__label == "pi":
                Rs, Rl, f0, dsrQ, tp = inputVal
                result = matching.pi_matching(float(Rs), float(Rl), float(f0), float(dsrQ), tp)
                self.disp_result(result, tp=tp)
            elif self.__label == "T":
                Rs, Rl, f0, dsrQ, tp = inputVal
                result = matching.T_matching(float(Rs), float(Rl), float(f0), float(dsrQ), tp)
                self.disp_result(result, tp=tp)
            elif self.__label == "TappedCap":
                Rs, Rl, f0, dsrQ = inputVal
                result = matching.tapped_cap_matching(float(Rs), float(Rl), float(f0), float(dsrQ))
                self.disp_result(result, tp=None)
            else:
                pass
        except ValueError: # there may be two kinds of exception here, empty input or string input
            self.throw_warning("Invalid Input", "The input should be numbers!")
    
    def on_clear_button(self, button):
        for i in self.inputList:
            i.reset()

    def throw_warning(self, mesg, secMesg):
        if self.win != None:
            dialog = Gtk.MessageDialog(self.win, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, mesg)
            dialog.format_secondary_text(secMesg)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                pass
            elif response == Gtk.ResponseType.CANCEL:
                pass
            dialog.destroy()
    
class IMpyParamBox(Gtk.Box):
    
    def __init__(self, labelStr):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True, spacing=10)
        self.label = Gtk.Label()
        self.label.set_alignment(0.5, 0) # misc method
        self.set_label(labelStr)
        self.pack_start(self.label, True, True, 0)

    def set_label(self, string):
        self.label.set_label(string)

class IMpyParamEntry(IMpyParamBox):

    def __init__(self, labelStr, isEditable):
        super().__init__(labelStr)
        self.entry = Gtk.Entry()
        self.entry.set_editable(isEditable)
        self.pack_start(self.entry, True, True, 0)

    def set_entry_text(self, string):
        self.entry.set_text(string)

    def get_entry_text(self):
        return self.entry.get_text()

    def reset(self):
        self.entry.set_text('')

class IMpyParamComboBox(IMpyParamBox):

    def __init__(self, labelStr, comboList):
        super().__init__(labelStr)
        self.listStore = Gtk.ListStore(str)
        for s in comboList:
            self.listStore.append([s])
        self.combo = Gtk.ComboBox.new_with_model(self.listStore)
        renderer_text = Gtk.CellRendererText()
        self.combo.pack_start(renderer_text, True)
        self.combo.add_attribute(renderer_text, "text", 0)
        self.combo.set_active(0) # default value
        self.pack_start(self.combo, False, True, True)

    def get_combo_text(self):
        idx = self.combo.get_active()
        if idx != None:
            model = self.combo.get_model()
            return model[idx][0]
    
    def reset(self):
        self.combo.set_active(0)

class IMpyMainWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="IMpy ver." + str(VER)+ " by rossihwang")
        self.set_default_size(800, 600)
        self.set_border_width(5)
        
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        window = self
        ### Add page for L
        self.page1 = IMpyPage("L", window)
        ### Add default image
        self.page1.disp_circuit_img("./img/L_low-pass.png")
        ### Input Entries
        self.page1.add_param_entry("Rs", True)
        self.page1.add_param_entry("Rl", True)
        self.page1.add_param_entry("f0(MHz)", True)
        self.page1.add_combo_box("Circuit type", ["low-pass", "high-pass"])
        # ### Output Entries
        self.page1.add_param_entry("Q", False)
        self.page1.add_param_entry("L(H)", False)
        self.page1.add_param_entry("C(F)", False)
        self.notebook.append_page(self.page1, Gtk.Label("L"))
        ###

        ### Add page for Pi
        self.page2 = IMpyPage("pi", window)
        ### Add default image
        self.page2.disp_circuit_img("./img/pi_low-pass.png")
        ### Input Entries
        self.page2.add_param_entry("Rs", True)
        self.page2.add_param_entry("Rl", True)
        self.page2.add_param_entry("f0(MHz)", True)
        self.page2.add_param_entry("Desired Q", True)
        self.page2.add_combo_box("Circuit type", ["low-pass", "high-pass"])
        ### Output Entries
        self.page2.add_param_entry("Q", False)
        self.page2.add_param_entry("L1(H)", False)
        self.page2.add_param_entry("L2(F)", False)
        self.page2.add_param_entry("C1(H)", False)
        self.page2.add_param_entry("C2(F)", False)
        self.notebook.append_page(self.page2, Gtk.Label("Pi"))
        ###

        ### Add page for T
        self.page3 = IMpyPage("T", window)
        ### Add default image
        self.page3.disp_circuit_img("./img/T_low-pass.png")
        ### Input Entries
        self.page3.add_param_entry("Rs", True)
        self.page3.add_param_entry("Rl", True)
        self.page3.add_param_entry("f0(MHz)", True)
        self.page3.add_param_entry("Desired Q", True)
        self.page3.add_combo_box("Circuit type", ["low-pass", "high-pass"])
        ### Output Entries
        self.page3.add_param_entry("Q", False)
        self.page3.add_param_entry("L1(H)", False)
        self.page3.add_param_entry("L2(F)", False)
        self.page3.add_param_entry("C1(H)", False)
        self.page3.add_param_entry("C2(F)", False)
        self.notebook.append_page(self.page3, Gtk.Label("T"))
        ###

        ### Add page for TappedCap
        self.page4 = IMpyPage("TappedCap", window)
        ### Add default image
        self.page4.disp_circuit_img("./img/TappedCap.png")
        ### Input Entries
        self.page4.add_param_entry("Rs", True)
        self.page4.add_param_entry("Rl", True)
        self.page4.add_param_entry("f0(MHz)", True)
        self.page4.add_param_entry("Desired Q", True)
        ### Output Entries
        self.page4.add_param_entry("Q", False)
        self.page4.add_param_entry("L(H)", False)
        self.page4.add_param_entry("C1(F)", False)
        self.page4.add_param_entry("C2(F)", False)
        self.notebook.append_page(self.page4, Gtk.Label("Tapped Cap"))
        ###

        ### Add about page
        self.page5 = Gtk.Box()
        lb = Gtk.Label()
        lb.set_markup("<a href=\"https://github.com/rossihwang/IMpy\"title=\"Click to find out more\">The Project Page</a>")
        lb.set_line_wrap(True)
        lb.set_alignment(xalign=0.0, yalign=0.0)
        self.page5.pack_start(lb, False, False, 0)
        self.notebook.append_page(self.page5, Gtk.Label("About"))

if __name__ == "__main__":
    pass
