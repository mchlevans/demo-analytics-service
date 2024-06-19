import numpy as np
import matplotlib
import scipy
from matplotlib.figure import Figure
import pandas as pd
import requests
import mpld3
from flask import current_app as app
from os import environ

import scipy.stats
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

from ..cache import cache
from ..AnalyticsAPIError import AnalyticsAPIError


#################################################################
# "It is not necessary to avoid using the pyplot interface in 
# order to create figures without a graphical front-end - 
# simply setting the backend to "Agg" would be sufficient."
#################################################################
# potentially remove
matplotlib.use('agg')

def singelVarChart(xTrainData, yTrainData, xPlotData, yHat, xAxisLabel, yAxisLabel):
    figure = Figure()
    ax = figure.subplots()
    ax.plot(xTrainData, yTrainData, '.', xPlotData, yHat, '-')
    ax.set_xlabel(xAxisLabel)
    ax.set_ylabel(yAxisLabel)
    ax.set_title("Predicted Value vs Observed Data Points")
    return figure


def multiVarChart(xTrainData, yTrainData, yHat, xAxisLabel, yAxisLabel):
    figure = Figure()
    ax = figure.subplots()
    ax.plot(xTrainData, yTrainData, '-', label = 'Observed Distribution')
    ax.plot(xTrainData, yHat, '-', label = 'Predicted Distribution')
    ax.legend()
    ax.set_xlabel(xAxisLabel)
    ax.set_ylabel(yAxisLabel, labelpad = 30)
    ax.set_title("Distribution Plot of Predicted Value Using Training Data vs Training Data Distribution")
    return figure


@cache.cached(timeout=50, key_prefix='db_data')
def fetchData():
    try:
        host = environ['INTERFACE_API_HOST']
        port = environ['INTERFACE_API_PORT']
        route = "http://" + host + ":" + port + "/vehicle?limit=1000&offset=0"
        
        app.logger.info('attempt to fetch api data')
        data = requests.get(route)

        # throw error if bad response
        data.raise_for_status()

        return data
    except requests.exceptions.RequestException as err:
        raise AnalyticsAPIError(500, ["unable to retrieve data"])


def buildDf():
    data = fetchData()
    app.logger.info('attempt to build df from data')
    df = pd.json_normalize(data.json())
    return df


def polyExample(xVarNames: list, yVarName: str, polynomial: int):
    # prep data
    df = buildDf()

    # get queried data
    xTrainData = df[xVarNames]
    yTrainData = df[yVarName]

    # transform polynomials
    pr = PolynomialFeatures(degree = polynomial)
    xPr = pr.fit_transform(xTrainData)

    # generate model from training data
    lm = LinearRegression()
    lm.fit(xPr, yTrainData)

    fig = '' # generated figure
    if len(xVarNames) == 1:
        ###########################################################
        # single variable model - plot vehicle variable on Y axis #
        ###########################################################
        
        # x values for graphing
        xPlotData = np.linspace(
            start = xTrainData.min(), 
            stop = xTrainData.max(), 
            num = 100
        )
        
        # generate predictions using x data generated for graphing purposes
        xPlotDataPr = pr.fit_transform(xPlotData)
        yHat = lm.predict(xPlotDataPr)
        
        # get graph
        fig = singelVarChart(
            xTrainData, 
            yTrainData,
            xPlotData,
            yHat = yHat,
            xAxisLabel = xVarNames[0],
            yAxisLabel = 'Price'
        )
    else:
        ####################################################
        # multivariate model - plot distribution on Y axis #
        ####################################################

        # get predicted values for training set
        yHatTrainingData = lm.predict(xPr)

        # use training values and predicted values to generate kde models
        actualKde = scipy.stats.gaussian_kde(yTrainData)
        predictedKde = scipy.stats.gaussian_kde(yHatTrainingData)
        
        # x values for graphing
        xPlotData = np.linspace(
            start = yTrainData.min(), 
            stop = yTrainData.max(), 
            num = 200
        )

        # get graph
        fig = multiVarChart(
            xPlotData,
            actualKde(xPlotData),
            predictedKde(xPlotData),
            xAxisLabel = 'Price',
            yAxisLabel = 'Proportion of Cars'
        )
    
    # return html version of graph
    return mpld3.fig_to_html(fig, template_type = 'simple')
