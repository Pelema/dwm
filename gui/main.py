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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from functools import partial
from tkinter.filedialog import askopenfilename
import csv
import mysql.connector





df = pd.read_csv("../barbershop.csv")

class OtherFrame(tk.Toplevel):
    def __init__(self, original):
        self.original_frame = original
        tk.Toplevel.__init__(self)
        # self.geometry("500x400")
        self.title("Mining")
        self.fig = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.calc_set = set()
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
        tk.Button(self, text="Clean").grid(row=1, columnspan=1)
        tk.Button(self, text="Bar chart", command=self.m_bar).grid(row=2, columnspan=1)
        tk.Button(self, text="Pie Chart", command=self.m_pie).grid(row=3, columnspan=1)
        tk.Button(self, text="Histogram", command=self.m_hist).grid(row=4, columnspan=1)
        tk.Button(self, text="Cluster", command=self.m_cluster).grid(row=5, columnspan=1)
        tk.Button(self, text="Box Plot",  command=self.m_box).grid(row=6, columnspan=1)
        tk.Button(self, text="Scatter Plot",  command=self.m_scatter).grid(row=7, columnspan=1)
        tk.Button(self, text="Association").grid(row=8, columnspan=1)

        tk.Label(self, text="x").grid(row=10, column=2)
        tk.Label(self, text="y").grid(row=10, column=4)

        tk.OptionMenu(self, "select", self.calc_set).grid(row=10, column=3)
        tk.Entry(self, background="white", fg="black").grid(row=10, column=5)


        colc = 8
        rowc = 0
        for column in df.columns.values:
            self.buttonDict[column]=tk.Button(self, text=column, command=partial(self.add_to_set, column))
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
            self.calc_set.add(column)
            self.buttonDict[column].config(background='green')
        return None


    def m_scatter(self):
        self.fig.clf()
        plt.scatter(df[self.y_variable], df[self.x_variable])
        plt.title('Barbershop Scatterplot')
        plt.xlabel(self.x_variable)
        plt.ylabel(self.y_variable)
        self.draw_canvas()

    def m_cluster(self):
        self.fig.clf()
        kmeans = KMeans(n_clusters=2).fit(df[['clients_per_month', 'monthly_income']])
        centroids = kmeans.cluster_centers_
        plt.scatter(df['clients_per_month'], df['monthly_income'], c=kmeans.labels_, cmap='rainbow')
        self.draw_canvas()

    def m_hist(self):
        self.fig.clf()

        for (i, itm) in enumerate(self.calc_set):
            clients = self.fig.add_subplot(12+i+1)
            clients.hist(df[itm], bins=10)
            clients.set_xlabel('Count')
            clients.set_title(itm + " histogram")
            
        self.draw_canvas()

        


    def m_box(self):
        self.fig.clf()
        sns.boxplot(x=self.x_variable, y=self.y_variable, data=df, orient="v")
        self.draw_canvas()

    def m_pie(self):
        type_counts = df['promotion_platform_1'].value_counts()
        df2 = pd.DataFrame({'prtype': type_counts}, 
                        index = ['b', 'o', 'r', 'u'])
        df2.plot.pie(y='prtype', figsize=(10, 10), autopct='%1.1f%%')
        self.draw_canvas()

    def m_bar(self):
        self.fig.clf()
        sns.countplot(x=self.x_variable, data=df[self.calc_set])
        self.draw_canvas()

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
        #close the connection to the database.
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