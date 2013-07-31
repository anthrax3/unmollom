# -*- coding: utf-8 -*-

"""
unmollom.exceptions


"""

class UnMollomException(RuntimeError):
    """Base class for all exceptions"""

class RecognitionException(UnMollomException):
    """Something in the recognition process went wrong"""

class AudioFormatException(UnMollomException):
    """This format cannot be converted to FLAC by your ffmpeg installation"""

class CommunicationException(UnMollomException):
    """Could not communicate with server"""

class NoMollomTagsFoundException(UnMollomException):
    """Is your target site really using mollom?"""