import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sys


class PhasePlot:
    """Main class that shows phase plots for a given star"""

    def __init__(self, root) -> None:
        """Initialization of a phase plot class"""
        self.root = root
        self.root.title = 'Phase Plot'
        self.root.geometry()

        self.file_name = sys.argv[1]
        self.file_V = self.file_name+"_V.dat_data"
        self.file_I = self.file_name+"_I.dat_data"
        self.freq_file_V = self.file_name+"_V.dat_data_fit"
        self.freq_file_I = self.file_name+"_I.dat_data_fit"

        self.periods_V, self.epochs_V = self.read_freq_list(self.freq_file_V)
        self.periods_I, self.epochs_I = self.read_freq_list(self.freq_file_I)

        self.data_V = np.loadtxt(self.file_V, usecols=(0, 1), unpack=True)
        self.data_I = np.loadtxt(self.file_I, usecols=(0, 1), unpack=True)

        # self.V_frame = ttk.Frame(self.root, padding=10).grid(column=0, row=0)
        # self.I_frame = ttk.Frame(self.root, padding=10).grid(column=1, row=0)

        self.V_frame = (tk.Frame(self.root, padx=10))
        self.V_frame.pack(side="right", fill="both", expand=True)
        self.I_frame = tk.Frame(self.root, padx=10)
        self.I_frame.pack(side="left", fill="both", expand=True)

        self.show_periods_main_window()

    def read_freq_list(self, file: str):
        """Reads frequencies and epochs from file with a fit"""
        f = open(file, 'r')
        f.readline()
        f.readline()
        f.readline()
        temp1 = []
        temp2 = []
        for line in f.readlines():
            temp1.append(float(line.split()[0]))
            temp2.append(float(line.split()[4]))
        return temp1, temp2


    def show_periods_main_window(self):
        for which_per, entry in enumerate(self.periods_I):
            tk.Button(self.I_frame, text='Phase').grid(column=0, row=which_per, padx=10)
            tk.Label(self.I_frame, text=str(1./entry)).grid(column=1, row=which_per)

        for which_per, entry in enumerate(self.periods_V):
            tk.Button(self.V_frame, text='Phase 2').grid(column=0, row=which_per, padx=10)
            tk.Label(self.V_frame, text=str(1./entry)).grid(column=1, row=which_per)



def main():
    root = tk.Tk()
    phaseplot = PhasePlot(root)
    root.geometry('600x800')
    root.mainloop()

if __name__ == '__main__':
    main()

