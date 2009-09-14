from zope.i18nmessageid import MessageFactory
RichFileStreamingMessageFactory = MessageFactory('atreal.richfile.streaming')

from atreal.richfile.streaming.interfaces import IStreamingAudio, IStreamingVideo, IStreaming

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    try:
        from atreal.richfile.qualifier.registry import registerRFPlugin
    except:
        return
    
    supported_audio_mimetypes = [
        'audio/x-mp3',
        'audio/mpeg',
        'audio/x-mpeg',
        'audio/x-wav',
        'audio/wav',
        'audio/vnd.wave',
        'audio/ogg',
        'audio/x-ogg',
        'application/ogg',
        ]

    supported_video_mimetypes = [
        'video/x-msvideo',
        'video/x-flv',
        'video/mpeg',
        'video/3gpp',
        'video/x-ms-wmv',
        'video/x-ms-asf',
        'video/quicktime',
        'video/ogg',
        'video/x-ogg',
        'video/x-ogm+ogg'
        ]
    
    registerRFPlugin(IStreamingAudio, supported_audio_mimetypes)
    registerRFPlugin(IStreamingVideo, supported_video_mimetypes)
    registerRFPlugin(IStreaming, supported_audio_mimetypes+supported_video_mimetypes)
    
