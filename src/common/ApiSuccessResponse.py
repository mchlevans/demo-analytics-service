class ApiSuccessResponse:
    def __init__(self, status: int, data):
        self.status = status
        self.data = data

    def getBody(self):
        return {
            'status': self.status,
            'data': self.data
        }
    def getStatus(self):
        return self.status


