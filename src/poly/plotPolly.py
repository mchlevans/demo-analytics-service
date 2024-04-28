import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
import mpld3

def plotPolly(model, independent_variable, dependent_variabble, Name):
    x_new = np.linspace(15, 55, 100)
    y_new = model(x_new)

    plt.plot(independent_variable, dependent_variabble, '.', x_new, y_new, '-')
    plt.title('Polynomial Fit with Matplotlib for Price ~ Length')

    ax = plt.gca()
    ax.set_facecolor((0.898, 0.898, 0.898))

    plt.xlabel(Name)
    plt.ylabel('Price of Cars')

    figure = plt.gcf()

    # To-do figure sizing: To transform from pixels to inches, divide by Figure.dpi.

    return figure

def buildDf():
    data = requests.get("http://app:8080/vehicle-stream")
    df = pd.json_normalize(data.json())
    return df

def polyExample(xVarName, yVarName):
    # prep data
    df = buildDf()
    
    # create model
    x = df[xVarName]
    y = df[yVarName]
    f = np.polyfit(x, y, 3)
    p = np.poly1d(f)

    # generate graph
    fig = plotPolly(p, x, y, 'highwayMpg')
    
    # return json version of graph
    return mpld3.fig_to_html(fig, template_type='simple')
