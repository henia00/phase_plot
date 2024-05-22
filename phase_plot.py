import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sys
from scipy.interpolate import CubicSpline, UnivariateSpline


class PhasePlot:
    """Main class that shows phase plots for a given star"""

    def __init__(self, root) -> None:
        """Initialization of a phase plot class"""
        self.root = root
        self.root.title('Phase Plot')
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


    def show_periods_main_window(self) -> None:
        tk.Label(self.I_frame, text='I-band').grid(column=0, row=0)
        for which_per, entry in enumerate(self.periods_I):
            tk.Button(self.I_frame, text='Phase',
                      command=lambda period=1./entry: self.show_phase_plot(period)).grid(column=0,
                                                                                             row=which_per+1,
                                                                                             padx=10)
            tk.Label(self.I_frame, text=str(1./entry)).grid(column=1, row=which_per+1)

        tk.Label(self.V_frame, text='V-band').grid(column=0, row=0)
        for which_per, entry in enumerate(self.periods_V):
            tk.Button(self.V_frame, text='Phase',
                      command=lambda period=1./entry: self.show_phase_plot(period)).grid(column=0,
                                                                                              row=which_per+1,
                                                                                              padx=10)
            tk.Label(self.V_frame, text=str(1./entry)).grid(column=1, row=which_per+1)

    def show_phase_plot(self, period: float) -> None:
        popup = tk.Toplevel()

        self.fig1, self.ax1 = plt.subplots(figsize=(6, 4), tight_layout=True)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=popup)
        self.canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, pady=10)

        self.fig2, self.ax2 = plt.subplots(figsize=(6, 4), tight_layout=True)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=popup)
        self.canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, pady=10)

        print(period)

        # phases, y = PhasePlot.get_epoch(self.data_I[0], self.data_I[1], period)
        phases = (self.data_V[0] / period) % 1.0
        y = self.data_V[1]

        self.ax1.set_title(f"Phased V, period {period} d")
        self.ax1.invert_yaxis()
        self.ax1.scatter(phases, y, color='green')
        self.ax1.scatter(phases + 1, y, color='green')
        self.canvas1.draw()

        # phases, y = PhasePlot.get_epoch(self.data_V[0], self.data_V[1], period)
        phases = (self.data_I[0] / period) % 1.0
        y = self.data_I[1]

        self.ax2.set_title("Phased I")
        self.ax2.invert_yaxis()
        self.ax2.scatter(phases, y, color='red')
        self.ax2.scatter(phases + 1, y, color='red')
        self.canvas2.draw()



    @staticmethod
    def get_epoch(x, y, period):
        # Compute phases
        phases = (np.array(x) / period) % 1.0

        # Sort phases and corresponding y values
        sorted_indices = np.argsort(phases)
        sorted_phases = phases[sorted_indices]
        sorted_y = np.array(y)[sorted_indices]

        # Fit a spline to the sorted data
        spline = UnivariateSpline(sorted_phases, sorted_y, s=1)

        # Generate a dense phase array for the spline
        dense_phase = np.linspace(0, 1, 1000)
        smooth_y = spline(dense_phase)


        # Find the phase corresponding to the minimum of the spline fit
        min_index_smooth = np.argmin(smooth_y)
        min_phase_smooth = dense_phase[min_index_smooth]

        # Shift the original phases
        shifted_phase = sorted_phases - min_phase_smooth

        # Handle periodicity by wrapping the shifted phases within [0, 1)
        wrapped_shifted_phase = np.mod(shifted_phase, 1.0)

        return wrapped_shifted_phase, sorted_y



def main():
    root = tk.Tk()
    phaseplot = PhasePlot(root)
    # root.geometry('600x800')
    root.mainloop()

if __name__ == '__main__':
    main()

