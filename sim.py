from ahkab import new_ac, run
from ahkab.circuit import Circuit
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import numpy as np

class Simulator():

    def __init__(self, simType):
        self.simType = simType
        if self.simType not in ["L", "pi", "T", "tapped_cap"]:
            raise RuntimeError("Not support for this simulation type!")
        self.simFig = plt.Figure()
        self.simAx = self.simFig.add_subplot(111) 
        self.simAx.set_xscale("log", nonposx="clip")
 
    @property
    def figure(self):
        return self.simFig 
        
    def update_figure(self):
        self.simFig.canvas.draw()
    
    def simulate(self, *input):
        if self.simType == "L":
            self.L_sim(input)
        elif self.simType == "pi":
            self.pi_sim(input)
        elif self.simType == "T":
            self.T_sim(input)
        elif self.simType == "tappped_cap":
            self.tapped_cap_sim(input)

    def L_sim(self, Rs, Rl, f0, L, C, tp):
        # Descript the circuit
        cir = Circuit("L matching")
        cir.add_isource("I1", cir.gnd, "n1", dc_value=0, ac_value=1)
        cir.add_resistor("Rs", "n1", cir.gnd, Rs)
        cir.add_capacitor("C", "n1", "n2", C)
        cir.add_inductor("L", "n2", cir.gnd, L)
        cir.add_resistor("Rl", "n2", cir.gnd, Rl)

        # AC analysis
        ac = new_ac(f0-100, f0+100, 100, x0=None)
        res = run(cir, ac)

        self.simAx.clear()
        idx = self.index_of_freq0(res["ac"]["f"], f0)
        xy = res["ac"]["f"][idx], res["ac"]["Vn1"][idx].real
        self.simAx.annotate("(%s, %s)" % xy, xy=xy, textcoords="data")
        self.simAx.plot(res["ac"]["f"], res["ac"]["Vn1"].real)
        self.simAx.plot(xy[0], xy[1], "bo")
        self.simFig.tight_layout()
        # self.__run_sim(cir, f0)

    def pi_sim(self, Rs, Rl, f0, L1, L2, C1, C2, tp):
        # Descript the circuit
        cir = Circuit("pi matching")
        cir.add_isource("I1", cir.gnd, "n1", dc_value=0, ac_value=1)
        cir.add_resistor("Rs", "n1", cir.gnd, Rs)
        # cir.add_vsource("V1", "n0", cir.gnd, dc_value=0, ac_value=Rs)
        # cir.add_resistor("Rs", "n0", "n1", Rs)
        if tp == "low-pass":
            cir.add_inductor("L1", "n1", "n2", L1)
            cir.add_capacitor("C1", "n1", cir.gnd, C1)
            cir.add_capacitor("C2", "n2", cir.gnd, C2)
        elif tp == "high-pass":
            cir.add_capacitor("C1", "n1", "n2", C1)
            cir.add_inductor("L1", "n1", cir.gnd, L1)
            cir.add_inductor("L2", "n2", cir.gnd, L2)
        cir.add_resistor("Rl", "n2", cir.gnd, Rl)
        
        self.__run_sim(cir, f0)
        
    def T_sim(self, Rs, Rl, f0, L1, L2, C1, C2, tp):
        # Descript the circuit
        cir = Circuit("pi matching")
        cir.add_isource("I1", cir.gnd, "n1", dc_value=0, ac_value=1)
        cir.add_resistor("Rs", "n1", cir.gnd, Rs)
        if tp == "low-pass":
            cir.add_inductor("L1", "n1", "n2", L1)
            cir.add_inductor("L2", "n2", "n3", L2)
            cir.add_capacitor("C1", "n2", cir.gnd, C1)
        elif tp == "high-pass":
            cir.add_capacitor("C1", "n1", "n2", C1)
            cir.add_capacitor("C2", "n2", "n3", C2)
            cir.add_inductor("L1", "n2", cir.gnd, L1)
        cir.add_resistor("Rl", "n3", cir.gnd, Rl)
        
        self.__run_sim(cir, f0)

    def tapped_cap_sim(self, Rs, Rl, f0, L, C1, C2):
        cir = Circuit("Tapped cap matching")
        cir.add_isource("I1", cir.gnd, "n1", dc_value=0, ac_value=1)
        cir.add_resistor("Rs", "n1", cir.gnd, Rs)
        # cir.add_vsource("V1", "n0", cir.gnd, dc_value=0, ac_value=Rs)
        # cir.add_resistor("Rs", "n0", "n1", Rs)
        cir.add_inductor("L", "n1", cir.gnd, L)
        cir.add_capacitor("C1", "n1", "n2", C1)
        cir.add_capacitor("C2", "n2", cir.gnd, C2)
        cir.add_resistor("Rl", "n2", cir.gnd, Rl)

        self.__run_sim(cir, f0)
        
    def index_of_freq0(self, fRange, f0):
        for idx, f in enumerate(fRange):
            if np.abs(f - f0) < 1.0:
                # print(idx, f) # debugging
                return idx
    
    def __run_sim(self, circuit, f0):

        minF = 1 if f0-100 <= 0 else f0-100
        maxF = f0+100
        ac = new_ac(minF, maxF, 100, x0=None)
        res = run(circuit, ac)

        self.simAx.clear()
        idx = self.index_of_freq0(res["ac"]["f"], f0)
        xy = res["ac"]['f'][idx], res["ac"]["Vn1"][idx].real
        self.simAx.annotate("(%s, %s)" % xy, xy=xy, textcoords="data")
        self.simAx.plot(res["ac"]['f'], res["ac"]["Vn1"].real)
        
        self.simAx.plot(xy[0], xy[1], "bo")
        self.simFig.tight_layout()