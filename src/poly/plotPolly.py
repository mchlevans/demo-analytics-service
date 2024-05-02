import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests
import mpld3
from flask import current_app as app
from ..AnalyticsAPIError import AnalyticsAPIError

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

def fetchData():
    try:
        app.logger.info('attempt to fetch api data')
        data = requests.get("http://app:8080/vehicle-stream")
        data.raise_for_status()
        return data
    except requests.exceptions.RequestException as err:
        raise AnalyticsAPIError(500, ["unable to retrieve data"])
    
def buildDf():
    data = fetchData()
    app.logger.info('attempt to build df from data')
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
    
    # return html version of graph
    return mpld3.fig_to_html(fig, template_type='simple')
