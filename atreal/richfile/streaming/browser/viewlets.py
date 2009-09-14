from zope.component import queryUtility
from Products.CMFPlone.interfaces import IPloneSiteRoot

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from atreal.richfile.qualifier.browser.viewlets import RichfileViewlet

from atreal.richfile.streaming.browser.controlpanel import IRichFileStreamingSchema
from atreal.richfile.streaming.interfaces import IStreamingVideo, IStreamingAudio, IStreaming, IStreamable
from atreal.richfile.streaming import RichFileStreamingMessageFactory as _

base_videoplayer = (
    "flowplayer('player',"
        "'flowplayer-3.1.1.swf',"
        "{"
            "clip: {"
                "autoPlay: %(AUTOPLAY)s,"
                "url: '%(URL)s'"
            "}"
        "})"
)

base_audioplayer = (
    "flowplayer('player',"
        "'flowplayer-3.1.1.swf',"
        "{"
            "plugins: {"
                "controls: {"
                    "fullscreen: %(FULLSCREEN)s,"
                    "height: %(HEIGHT)s"
                "}"
            "},"
            "clip: "
                "{"
                    "autoPlay: %(AUTOPLAY)s,"
                    "url: '%(URL)s'"
                "}"
        "})"
)

class FlowPlayerViewlet(RichfileViewlet):
    """
    """
    index = ViewPageTemplateFile("flowplayer.pt")
    marker_interface = IStreaming
    plugin_interface = IStreamable
    plugin_id = 'streaming'
    plugin_title = 'Streaming'
    controlpanel_interface = IRichFileStreamingSchema

    
    def update(self):
        super(FlowPlayerViewlet, self).update()
        self.video = IStreamingVideo.providedBy(self.context)
        self.audio = IStreamingAudio.providedBy(self.context)
        self.state = IStreamable(self.context).state
    
    
    def autoplay(self):
        """ """
        return getattr (self._getConfig(), 'rfs_autoplay', False)
    
    
    def videoPlayer(self):
        """ """
        parameters = dict(AUTOPLAY = self.autoplay() and 'true' or 'false',
                           URL = '%s/rfstreaming/streaming.flv' % self.context.absolute_url(),
                           )
        return base_videoplayer % parameters


    def audioPlayer(self):
        """ """
        parameters = dict(AUTOPLAY = self.autoplay() and 'true' or 'false',
                           URL = '%s/rfstreaming/streaming.mp3' % self.context.absolute_url(),
                           FULLSCREEN = 'false',
                           HEIGHT = '25',
                           )
        return base_audioplayer % parameters



