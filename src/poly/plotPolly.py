import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import requests
import mpld3
from flask import current_app as app
from ..AnalyticsAPIError import AnalyticsAPIError

# need to update this to use matplotlib.figure as pyplot will
# cause memmory leaks


def plotPolly(model, xData, yData, Name):
    # generate data for predicted trend line
    xDataPredicted = np.linspace(
        start = xData.min(), 
        stop = xData.max(), 
        num = 100
    )
    
    yDataPredicted = np.polynomial.polynomial.polyval(xDataPredicted, model)

    fig = Figure()
    
    # add previous data as scatterplot, predicted as line
    ax = fig.subplots()
    ax.plot(xDataPredicted, yDataPredicted)
    ax.plot(xData, yData, "o")

    return fig

def fetchData():
    try:
        app.logger.info('attempt to fetch api data')
        data = requests.get("http://app:8080/vehicle?limit=1000&offset=0")
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
    f = np.polynomial.polynomial.polyfit(x, y, 3)

    # p = np.polynomial.Polynomial(f)

    # generate graph
    fig = plotPolly(
        model = f, 
        xData = x, 
        yData = y,
        Name = xVarName
    )
    
    # return html version of graph
    return mpld3.fig_to_html(fig, template_type='simple')
