from s4f.errors import ServiceError as BaseServiceError


class ServiceError(BaseServiceError):
    def __init__(self, error_code, error_message, service_traceback=None):
        error_message = "stock_client: {}".format(error_message)
        super(ServiceError, self).__init__(
            error_code,
            error_message,
            service_name="stock_client",
            service_traceback=service_traceback,
        )


class InvalidStockAdjustmentError(Exception):
    """
    raised when an invalidate reason code is used for stock adjustment
    """
