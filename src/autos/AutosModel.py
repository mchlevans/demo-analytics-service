
import mpld3
import pandas as pd
import numpy as np

from scipy.stats import gaussian_kde
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from matplotlib.figure import Figure


class AutosModel:
    pixelToInch = .0104166667
    aspectRatio = .75 # matplotlib default

    def __init__(self, df: pd.DataFrame, independentVariables: list, dependentVariable: list, polynomial: int, width: int = None):
        xTrainData = df[independentVariables]
        yTrainData = df[dependentVariable]

        # transform polynomials
        pr = PolynomialFeatures(degree = polynomial)
        xTrainTransformed = pr.fit_transform(xTrainData)

        # generate model from training data
        lm = LinearRegression()
        lm.fit(xTrainTransformed, yTrainData)

        self.lm = lm
        self.xTrainTransformed = xTrainTransformed
        self.xTrainData = xTrainData
        self.yTrainData = yTrainData
        self.polynomial = polynomial
        self.independentVariables = independentVariables
        self.width = width if width != None else 550
        
    
    def getFigure(self):
        if len(self.independentVariables) == 1:
            return self.getSingleVarChart()
        return self.getMultiVarChart()
    
    
    # plot predicted autos property on Y axis
    def getSingleVarChart(self):
        # x values for graphing
        xPlotData = np.linspace(
            start = self.xTrainData.min(), 
            stop = self.xTrainData.max(), 
            num = 100
        )
        
        # generate predictions using x data generated for graphing purposes
        pr = PolynomialFeatures(degree = self.polynomial)
        xPlotDataTransformed = pr.fit_transform(xPlotData)
        yHat = self.lm.predict(xPlotDataTransformed)
        
        # build figure
        figure = Figure(figsize=[self.getFigureWidth(), self.getFigureHeight()])
        ax = figure.subplots()
        ax.plot(self.xTrainData, self.yTrainData, '.', xPlotData, yHat, '-')
        ax.set_xlabel(self.independentVariables[0])
        ax.set_ylabel("Price") # temp harcode
        ax.set_title("Predicted Value vs Observed Data Points")

        # return html version of graph
        return mpld3.fig_to_html(figure, template_type = 'simple')
    

    # plot distribution on Y axis
    def getMultiVarChart(self):
        # get predicted values for training set
        yHatTrainingData = self.lm.predict(self.xTrainTransformed)

        # use training values and predicted values to generate kde corresponding models
        actualKde = gaussian_kde(self.yTrainData)
        predictedKde = gaussian_kde(yHatTrainingData)
        
        # x values for graphing smooth curve
        xPlotData = np.linspace(
            start = self.yTrainData.min(), 
            stop = self.yTrainData.max(), 
            num = 200
        )

        # build figure
        figure = Figure(figsize=[self.getFigureWidth(), self.getFigureHeight()])
        ax = figure.subplots()
        ax.plot(xPlotData, actualKde(xPlotData), '-', label = 'Observed Distribution')
        ax.plot(xPlotData, predictedKde(xPlotData), '-', label = 'Predicted Distribution')
        ax.legend()
        ax.set_xlabel('Price')
        ax.set_ylabel('Proportion of Cars', labelpad = 30)
        ax.set_title("Distribution Plot of Predicted Value Using Training Data vs Training Data Distribution")
    
        # return html version of graph
        return mpld3.fig_to_html(figure, template_type = 'simple')


    def getRsquared(self):
        return self.lm.score(self.xTrainTransformed, self.yTrainData)


    def getMse(self):
        return mean_squared_error(self.yTrainData, self.lm.predict(self.xTrainTransformed))

    def getFigureWidth(self):
        return self.width * self.pixelToInch
    
    def getFigureHeight(self):
        return self.width * self.pixelToInch * self.aspectRatio