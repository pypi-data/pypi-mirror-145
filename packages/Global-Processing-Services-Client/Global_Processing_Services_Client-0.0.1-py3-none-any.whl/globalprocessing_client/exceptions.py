"""GPS Exceptions.

:copyright: (c) DiviPay 2022
"""


class GPSClientException(BaseException):
    pass


class GPSClientConnectionException(GPSClientException):
    pass
