import logging
from flask import Flask, request
from marshmallow import ValidationError
from .poly.plotPolly import polyExample
from .poly.PolySchema import PolySchema
from .AnalyticsAPIError import AnalyticsAPIError

def app():    
    app = Flask(__name__)

    # setup logging using gunicorn configs
    if __name__ != '__main__':
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    @app.route("/")
    def hello_world():
        app.logger.info('hit ping route')
        return {
            'status': 200,
            'data': "Hello, World!"
        }

    @app.route("/poly", methods = ['POST'])
    def ployController():
        body = request.json
        
        # validate request body
        try:
            PolySchema().load(body)
        except ValidationError as err:
            app.logger.info('caught validation exception in analytcis api')
            raise AnalyticsAPIError(status=400, errors=err.messages)

        
        figure = polyExample(xVarName = body['xVarName'], 
                             yVarName = body['yVarName'])         
        
        # to do: encapsulate success response body
        return {
            'status': 200,
            'data': {
                'figure': figure
            }
        }
    
    @app.errorhandler(AnalyticsAPIError)
    def error_response(e):
        return e.getBody(), e.getStatus()

    return app
