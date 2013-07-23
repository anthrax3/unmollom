# -*- coding: utf-8 -*-

"""
unmollom.exceptions


"""

class UnMollomException(RuntimeError):
    """Base class for all exceptions"""

class RecognitionException(UnMollomException):
    """Something in the recognition process went wrong"""

class CommunicationException(UnMollomException):
    """Could not communicate with server"""