import requests
from os import environ
from flask import current_app as app
import pandas as pd
from ..common.cache import cache
from ..common.ApiErrorResponse import ApiErrorResponse

@cache.cached(timeout=60 * 60 * 24 * 21, key_prefix='db_data')
def fetchAutosData():
    try:
        host = environ['INTERFACE_API_HOST']
        port = environ['INTERFACE_API_PORT']
        route = "http://" + host + ":" + port + "/vehicle?limit=1000&offset=0"
        
        app.logger.info('attempt to fetch api data')
        response = requests.get(route)
        # throw error if bad response
        response.raise_for_status()

        return response.json()['data']
    except requests.exceptions.RequestException as err:
        raise ApiErrorResponse(500, ['unable to retrieve data'])


def getAutosDf():
    data = fetchAutosData()
    app.logger.info('attempt to build df from data')
    df = pd.json_normalize(data)
    return df
