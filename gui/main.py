import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from apyori import apriori
import numpy as np
import sklearn
from sklearn import cluster
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

df = pd.read_csv("../barbershop.csv")

class OtherFrame(tk.Toplevel):
    def __init__(self, original):
        self.original_frame = original
        tk.Toplevel.__init__(self)
        # self.geometry("500x400")
        self.title("Mining")

        self.create_widgets()
        
        btn = tk.Button(self, text="Back", command=self.onClose)
        btn.grid(row=7)

    def onClose(self):
        self.destroy()
        self.original_frame.show()

    def create_widgets(self):
        tk.Button(self, text="clean").grid(row=0, columnspan=1)
        tk.Button(self, text="bar chart", command=self.calculate_bar).grid(row=1, columnspan=1)
        tk.Button(self, text="pie chart").grid(row=2, columnspan=1)
        tk.Button(self, text="histogram").grid(row=3, columnspan=1)
        tk.Button(self, text="Cluster").grid(row=4, columnspan=1)
        tk.Button(self, text="Box Plot").grid(row=5, columnspan=1)
        tk.Button(self, text="Association").grid(row=6, columnspan=1)
        self.text = tk.Text(self)
        self.text.grid(row=0, column=2, rowspan=6)
        self.text.insert(tk.END, "this is a text area")

    def calculate_bar(self):
        self.text.delete(1.0, tk.END)
        # self.text.insert(tk.END, df.head())

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        #sss = sns.jointplot(x="clients_per_month", y="monthly_income", data=df, kind = 'reg', fit_reg=True, height=7)

        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().grid(row=0, column=1, columnspan=6)

        canvas._tkcanvas.grid(row=0, column=1, columnspan=6)

        # sns.jointplot(x="clients_per_month", y="monthly_income", data=df, kind = 'reg', fit_reg=True, height=7)
        # plt.show()

        


class MyApp(object):
    def __init__(self, parent):
        self.root = parent
        self.root.title("main frame")
        self.frame = tk.Frame(parent)
        self.frame.grid()

        btn = tk.Button(self.frame, text="mine", command=self.openFrame)
        btn.grid(row=7, column=2)

        self.create_widgets()

    def hide(self):
        self.root.withdraw()

    def openFrame(self):
        self.hide()
        subFrame = OtherFrame(self)


    def show(self):
        self.root.update()
        self.root.deiconify()
    
    def create_widgets(self):

        tk.Label(self.frame, text="Cellphone").grid(row=0)
        tk.Label(self.frame, text="Style").grid(row=0, column=2)
        tk.Label(self.frame, text="Price").grid(row=1)
        tk.Label(self.frame, text="Rent").grid(row=1, column=2)
        tk.Label(self.frame, text="Transport").grid(row=2)
        tk.Label(self.frame, text="Clients").grid(row=2, column=2)
        tk.Label(self.frame, text="Income").grid(row=3)
        tk.Label(self.frame, text="Transport Type").grid(row=3, column=2)
        tk.Label(self.frame, text="Hours").grid(row=4)
        tk.Label(self.frame, text="Trip").grid(row=4, column=2)
        tk.Label(self.frame, text="Shop").grid(row=5)
        tk.Label(self.frame, text="Plat1").grid(row=5, column=2)
        tk.Label(self.frame, text="Plat2").grid(row=6)

        self.cell = tk.Entry(self.frame)
        self.style = tk.Entry(self.frame)
        self.cost = tk.Entry(self.frame)
        self.rent = tk.Entry(self.frame)
        self.transport = tk.Entry(self.frame)
        self.clients = tk.Entry(self.frame)
        self.income = tk.Entry(self.frame)
        self.tform = tk.Entry(self.frame)
        self.hours = tk.Entry(self.frame)
        self.trip = tk.Entry(self.frame)
        self.shop = tk.Entry(self.frame)
        self.plat1 = tk.Entry(self.frame)
        self.plat2 = tk.Entry(self.frame)

        self.cell.grid(row=0, column=1)
        self.style.grid(row=0, column=3)
        self.cost.grid(row=1, column=1) 
        self.rent.grid(row=1, column=3) 
        self.transport.grid(row=2, column=1) 
        self.clients.grid(row=2, column=3) 
        self.income.grid(row=3, column=1)
        self.tform.grid(row=3, column=3)
        self.hours.grid(row=4, column=1)
        self.trip.grid(row=4, column=3) 
        self.shop.grid(row=5, column=1) 
        self.plat1.grid(row=5, column=3)
        self.plat2.grid(row=6, column=1)

        

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x400")
    app = MyApp(root)
    root.mainloop()