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

df = pd.read_csv("../barbershop.csv")

class OtherFrame(tk.Toplevel):
    def __init__(self, original):
        self.original_frame = original
        tk.Toplevel.__init__(self)
        # self.geometry("500x400")
        self.title("Mining")
        self.fig = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.calc_set = []


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
        tk.Button(self, text="Regression", command=self.m_regression).grid(row=9, columnspan=1)


        count = 0
        row = 10
        for column in df.columns.values:
            if(count > 7):
                row = 11


            tk.Button(self, text=column, command=partial(self.add_to_set, column)).grid(row=row, column=count+2, columnspan=1)
            count += 1

    def add_to_set(self, column):
        
        self.calc_set.append(column)
        print(self.calc_set)

        return None


    def m_regression(self):
        self.fig.clf()
        sns.lmplot(x="clients_per_month", y="monthly_income", hue="shop_type", data=df, markers=["o", "x"])
        self.draw_canvas()

    # def m_apryori(self):
    #     self.fig.clf()
    #     records = []
    #     for i in range(0, 50):
    #         records.append([str(df.values[i,j]) for j in range(5, 6)])
    #         association_rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)
    #         association_results = list(association_rules)
    #         print(len(association_rules))
    #         print(association_rules[0])
        
    #     for item in association_rules:

    #         # first index of the inner list
    #         # Contains base item and add item
    #         pair = item[0] 
    #         items = [x for x in pair]
    #         print("Rule: " + items[0] + " -> " + items[1])

    #         #second index of the inner list
    #         print("Support: " + str(item[1]))

    #         #third index of the list located at 0th
    #         #of the third index of the inner list

    #         print("Confidence: " + str(item[2][0][2]))
    #         print("Lift: " + str(item[2][0][3]))
    #         print("=====================================")

    def m_scatter(self):
        self.fig.clf()
        plt.scatter(df.clients_per_month, df.monthly_income)
        plt.title('Barbershop Scatterplot')
        plt.xlabel('Monthly Income')
        plt.ylabel('Clients per Month')
        self.draw_canvas()

    def m_cluster(self):
        self.fig.clf()
        kmeans = KMeans(n_clusters=2).fit(df[['clients_per_month', 'monthly_income']])
        centroids = kmeans.cluster_centers_
        plt.scatter(df['clients_per_month'], df['monthly_income'], c=kmeans.labels_, cmap='rainbow')
        self.draw_canvas()

    def m_hist(self):
        self.fig.clf()
        clients = self.fig.add_subplot(121)
        income = self.fig.add_subplot(122)

        clients.hist(df.clients_per_month, bins=10)
        clients.set_xlabel('Count')
        clients.set_title("Clients per Month")

        income.hist(df.monthly_income, bins=10)
        income.set_xlabel('N$')
        income.set_title("Monthly Barber Income")
        self.draw_canvas()


    def m_box(self):
        self.fig.clf()
        sns.boxplot(x='shop_type', y='cost', data=df, orient="v")
        self.draw_canvas()

    def m_pie(self):
        type_counts = df['promotion_platform_1'].value_counts()
        df2 = pd.DataFrame({'prtype': type_counts}, 
                        index = ['b', 'o', 'r', 'u'])
        df2.plot.pie(y='prtype', figsize=(10, 10), autopct='%1.1f%%')
        self.draw_canvas()

    def m_bar(self):
        self.fig.clf()
        sns.countplot(x='hairstyle', data=df[self.calc_set])
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