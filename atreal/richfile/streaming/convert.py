from zope.interface import implements

from Products.Five  import BrowserView
from atreal.richfile.streaming.interfaces import ICallBackView, IStreamable

class CallBackView(BrowserView):
    """
    """
    implements(ICallBackView)
    
    def conv_done_xmlrpc(self, status):
        """
        """
        IStreamable(self.context)._storeStreaming(status)
