from atreal.richfile.streaming.interfaces import IStreamable
from atreal.richfile.qualifier.common import RFView
from atreal.richfile.streaming import RichFileStreamingMessageFactory as _

class RFStreamingView(RFView):
    """
    """
    plugin_interface = IStreamable
    kss_id = 'streaming'
    viewlet_name = 'atreal.richfile.streaming.flowplayer'
    update_message = _('The streaming has been updated.')
    active_message = _('Streaming activated.')
    unactive_message = _('Streaming un-activated.')   
