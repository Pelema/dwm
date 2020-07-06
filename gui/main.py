import mysql.connector
import csv
from tkinter.filedialog import askopenfilename
from functools import partial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from apyori import apriori
import numpy as np
import sklearn
from sklearn import cluster
import statsmodels.api as sm
from statsmodels.formula.api import ols
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use("TkAgg")


df = pd.read_csv("../barbershop.csv")


class OtherFrame(tk.Toplevel):
    def __init__(self, original):
        self.original_frame = original
        tk.Toplevel.__init__(self)
        # self.geometry("500x400")
        self.title("Mining")
        self.fig = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.calc_set = ["default"]
        self.buttonDict = {}
        self.x_variable = None
        self.y_variable = None

        self.create_widgets()
        sns.set(style="whitegrid")

        btn = tk.Button(self, text="Back", command=self.onClose)
        btn.grid(row=0)

    def onClose(self):
        self.destroy()
        self.original_frame.show()

    def create_widgets(self):
        tk.Button(self, text="Clean", command=self.m_clean).grid(
            row=1, columnspan=1)
        tk.Button(self, text="Bar chart", command=self.m_bar).grid(
            row=2, columnspan=1)
        tk.Button(self, text="Pie Chart", command=self.m_pie).grid(
            row=3, columnspan=1)
        tk.Button(self, text="Histogram", command=self.m_hist).grid(
            row=4, columnspan=1)
        tk.Button(self, text="Cluster", command=self.m_cluster).grid(
            row=5, columnspan=1)
        tk.Button(self, text="Box Plot",  command=self.m_box).grid(
            row=6, columnspan=1)
        tk.Button(self, text="Scatter Plot",
                  command=self.m_scatter).grid(row=7, columnspan=1)
        tk.Button(self, text="Association").grid(row=8, columnspan=1)

        tk.Label(self, text="x").grid(row=10, column=2)
        tk.Label(self, text="y").grid(row=10, column=4)

        self.select_default_x = tk.StringVar()
        self.select_default_x.set(self.calc_set[0])

        self.select_default_y = tk.StringVar()
        self.select_default_y.set(self.calc_set[0])

        self.options_x = tk.OptionMenu(
            self, self.select_default_x, *self.calc_set, command=self.func_x)
        self.options_x.grid(row=10, column=3)

        self.options_y = tk.OptionMenu(
            self, self.select_default_y, *self.calc_set, command=self.func_y)
        self.options_y.grid(row=10, column=5)

        colc = 8
        rowc = 0
        for column in df.columns.values:
            self.buttonDict[column] = tk.Button(
                self, text=column, command=partial(self.add_to_set, column))
            self.buttonDict[column].grid(row=rowc, column=colc, columnspan=1)
            if(colc == 9):
                colc -= 1
                rowc += 1
            else:
                colc += 1

    def add_to_set(self, column):
        if(self.buttonDict[column].cget('bg') == 'green'):
            self.calc_set.remove(column)
            self.buttonDict[column].config(background='#383838')

        else:
            if ("default" in self.calc_set):
                self.calc_set.remove("default")

            self.calc_set.append(column)
            self.buttonDict[column].config(background='green')

        menu_x = self.options_x.children['menu']
        menu_y = self.options_y.children['menu']

        menu_x.delete(0, "end")
        menu_y.delete(0, "end")

        for string in self.calc_set:
            menu_x.add_command(label=string,
                             command=lambda value=string: self.func_x(value))
            menu_y.add_command(label=string,
                             command=lambda value=string: self.func_y(value))

        return None

    def func_x(self, value):
        self.x_variable = value

        return self.select_default_x.set(value)

    def func_y(self, value):
        self.y_variable = value
        return self.select_default_y.set(value)

    def m_scatter(self):
        self.fig.clf()
        plt.scatter(df[self.x_variable], df[self.y_variable])
        plt.title('Barbershop Scatterplot')
        plt.xlabel(self.x_variable)
        plt.ylabel(self.y_variable)
        self.draw_canvas()

    def m_cluster(self):
        self.fig.clf()
        kmeans = KMeans(n_clusters=2).fit(df[self.calc_set])
        centroids = kmeans.cluster_centers_
        plt.scatter(df[self.x_variable], df[self.y_variable],
                    c=kmeans.labels_, cmap='rainbow')
        plt.xlabel(self.x_variable)
        plt.ylabel(self.y_variable)
        self.draw_canvas()

    def m_hist(self):
        self.fig.clf()

        plt = self.fig.add_subplot(111)
        plt.hist(df[self.x_variable], bins=10)
        plt.set_xlabel(self.x_variable)
        plt.set_title(self.x_variable + " histogram")
        self.draw_canvas()

    def m_box(self):
        self.fig.clf()
        sns.boxplot(x=self.x_variable, y=self.y_variable, data=df, orient="v")
        self.draw_canvas()

    def m_pie(self):
        self.fig.clf()
        plt = self.fig.add_subplot(111)
        plt.set_title(self.x_variable + " pie chart")
        type_counts_1 = df[self.x_variable].value_counts()

        df1 = pd.DataFrame({'prtype': type_counts_1},
                        index=type_counts_1.keys())

        plt.pie(df1['prtype'], labels=type_counts_1.keys(), autopct='%1.1f%%')

        self.draw_canvas()

    def m_bar(self):
        self.fig.clf()
        plt = self.fig.add_subplot(111)
        plt.set_title(self.x_variable + " bar chart")
        sns.countplot(x=self.x_variable, data=df[self.calc_set])
        self.draw_canvas()

    def m_clean(self):
        df['hairstyle'].str.lower()
        median = df['transport_cost'].median()
        df.fillna({'monthly_rent':0, 'clients_per_trip': 0, 'transport_cost':median}, inplace=True)
        

    def draw_canvas(self):
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(row=0, column=1, rowspan=6)
        self.canvas._tkcanvas.grid(row=0, column=1, columnspan=6)

class MyApp(object):
    def __init__(self, parent):
        self.root = parent
        self.root.title("main frame")
        self.frame = tk.Frame(parent)
        self.frame.grid()

        tk.Button(self.frame, text="mine", command=self.openFrame).grid(row=0, column=3)
        tk.Button(self.frame ,text="Submit").grid(row=11,column=3)
        tk.Button(self.frame, text="Upload", command=self.upload).grid(row=1, column=3, pady=10)
        self.selectField = tk.Entry(self.frame, text="mine")
        self.selectField.grid(row=1, column=0, columnspan=3, pady=10)
        self.selectField.bind("<Double-Button-1>", self.someFile)        

        self.create_widgets()

    def upload(self):
        mydb = mysql.connector.connect(host='localhost',
            user='root',
            passwd='',
            db='mydb')
        cursor = mydb.cursor()

        csv_data = csv.reader(self.filename)
        for row in csv_data:

            cursor.execute('INSERT INTO testcsv(names, \
                classes, mark )' \
                'VALUES("%s", "%s", "%s")', 
                row)
        # close the connection to the database.
        cursor.close()
        return 0

    def someFile(self, event):
        self.filename = askopenfilename(filetypes = (("CSV files","*.csv"), ("all files", "*.*")))
        self.selectField.delete(1,"end")
        self.selectField.insert(1, self.filename)
        return None

    def hide(self):
        self.root.withdraw()

    def openFrame(self):
        self.hide()
        subFrame = OtherFrame(self)


    def show(self):
        self.root.update()
        self.root.deiconify()
    
    def create_widgets(self):


        tk.Label(self.frame, text="Barbershop Form").grid(row=3, columnspan=3, pady=15)
        tk.Label(self.frame, text="Cellphone").grid(row=4)
        tk.Label(self.frame, text="Style").grid(row=4, column=2)
        tk.Label(self.frame, text="Price").grid(row=5)
        tk.Label(self.frame, text="Rent").grid(row=5, column=2)
        tk.Label(self.frame, text="Transport").grid(row=6)
        tk.Label(self.frame, text="Clients").grid(row=6, column=2)
        tk.Label(self.frame, text="Income").grid(row=7)
        tk.Label(self.frame, text="Transport Type").grid(row=7, column=2)
        tk.Label(self.frame, text="Hours").grid(row=8)
        tk.Label(self.frame, text="Trip").grid(row=8, column=2)
        tk.Label(self.frame, text="Shop").grid(row=9)
        tk.Label(self.frame, text="Plat1").grid(row=9, column=2)
        tk.Label(self.frame, text="Plat2").grid(row=10)

        self.cell = tk.Entry(self.frame, background="white", fg="black")
        self.style = tk.Entry(self.frame, background="white", fg="black")
        self.cost = tk.Entry(self.frame, background="white", fg="black")
        self.rent = tk.Entry(self.frame, background="white", fg="black")
        self.transport = tk.Entry(self.frame, background="white", fg="black")
        self.clients = tk.Entry(self.frame, background="white", fg="black")
        self.income = tk.Entry(self.frame, background="white", fg="black")
        self.tform = tk.Entry(self.frame, background="white", fg="black")
        self.hours = tk.Entry(self.frame, background="white", fg="black")
        self.trip = tk.Entry(self.frame, background="white", fg="black")
        self.shop = tk.Entry(self.frame, background="white", fg="black")
        self.plat1 = tk.Entry(self.frame, background="white", fg="black")
        self.plat2 = tk.Entry(self.frame, background="white", fg="black")

        self.cell.grid(row=4, column=1)
        self.style.grid(row=4, column=3)
        self.cost.grid(row=5, column=1) 
        self.rent.grid(row=5, column=3) 
        self.transport.grid(row=6, column=1) 
        self.clients.grid(row=6, column=3) 
        self.income.grid(row=7, column=1)
        self.tform.grid(row=7, column=3)
        self.hours.grid(row=8, column=1)
        self.trip.grid(row=8, column=3) 
        self.shop.grid(row=9, column=1) 
        self.plat1.grid(row=9, column=3)
        self.plat2.grid(row=10, column=1)

        

root = tk.Tk()
root.geometry("500x400")
app = MyApp(root)
root.mainloop()
