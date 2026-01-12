class Service1Error(Exception):
    pass

class ServiceRequestError(Service1Error):
    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(f"Service returned status {status_code}")