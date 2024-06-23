import logging
from flask import Flask, request
from marshmallow import ValidationError
from .common.cache import cache
from .common.PolySchema import PolySchema
from .common.ApiErrorResponse import ApiErrorResponse
from .common.ApiSuccessResponse import ApiSuccessResponse

from .autos.AutosModel import AutosModel
from .autos.autosService import getAutosDf

def app():    
    app = Flask(__name__)
    cache.init_app(app)


    # setup logging using gunicorn configs
    if __name__ != '__main__':
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)


    @app.route("/ping")
    def hello_world():
        app.logger.info('hit ping route')
        return {
            'status': 200,
            'data': "pong"
        }


    @app.route("/autos-model", methods = ['POST'])
    def autosModelController():
        body = request.json
        
        # validate request body
        try:
            PolySchema().load(body)
        except ValidationError as err:
            app.logger.info('caught validation exception in analytcis api')
            raise ApiErrorResponse(status=400, errors=err.messages)
        
        # fetch data and build model
        dataframe = getAutosDf()
        model = AutosModel(
            df = dataframe,
            independentVariables = body['xVarNames'],
            dependentVariable = body['yVarName'],
            polynomial = body['polynomial']
        )
        
        autosData = {
            'figure': model.getFigure(),
            'rsquared': model.getRsquared(),
            'mse': model.getMse()
        }
        
        response = ApiSuccessResponse(status = 200, data = autosData)
        return response.getBody(), response.getStatus()


    @app.errorhandler(ApiErrorResponse)
    def error_response(e):
        return e.getBody(), e.getStatus()

    return app
