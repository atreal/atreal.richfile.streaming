from zope.interface import Interface

class IRichFileStreamingLayer(Interface):
    """ Marker interface that defines a Zope 3 browser layer.
    """

class IRichFileStreamingSite(Interface):
    """ Marker interface for sites with this product installed.
    """ 

class IStreaming(Interface):
    """
    """
    
class IStreamingAudio(IStreaming):
    """
    """

class IStreamingVideo(IStreaming):
    """
    """
    
class IStreamable(Interface):
    """
    """

class ICallBackView(Interface):
    """
    """
    def conv_done_xmlrpc(status):
        """
        """
