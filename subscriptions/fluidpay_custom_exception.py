from rest_framework import status
from rest_framework.exceptions import APIException


class FluidPayCustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, *args, response_body=None):
        self.response_body = response_body
        super().__init__(*args)

