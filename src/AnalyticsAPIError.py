class AnalyticsAPIError(Exception):
    def __init__(self, status: int, errors: list):
        self.status = status
        self.errors = errors

    def getBody(self):
        return {
            'status': self.status,
            'errors': self.errors
        }
    def getStatus(self):
        return self.status
