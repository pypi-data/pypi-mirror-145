# coding: utf-8


class MaxipagoException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ValidationError(MaxipagoException):
    def __repr__(self):
        return 'ValidationError(%s)' % self.message


# customer
class CustomerException(MaxipagoException):
    def __repr__(self):
        return 'CustomerError(%s)' % self.message


class CustomerAlreadyExists(CustomerException):
    def __repr__(self):
        return 'CustomerValidation(%s)' % self.message


class CardException(MaxipagoException):
    def __repr__(self):
        return 'CardError(%s)' % self.message


class PaymentException(MaxipagoException):
    def __repr__(self):
        return 'PaymentError(%s)' % self.message


#http
class HttpErrorException(MaxipagoException):
    def __repr__(self):
        return 'HttpError(%s)' % self.message
