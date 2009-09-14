from zope.interface.interfaces import IInterface
from zope.component import queryUtility


from atreal.richfile.streaming.interfaces import IStreamable


def is_richfilestreaming_installed():
    """
    """
    return queryUtility(IInterface, name=u'atreal.richfile.streaming.IRichFileStreamingSite', default=False)


def buildAndStoreStreaming(obj, event):
    """
    """
    if not is_richfilestreaming_installed():
        return
    print "atreal.richfile.streaming: build and store streaming for %s" % ('/'.join(obj.getPhysicalPath()))
    IStreamable(obj).process()


def cleanStreamingData(obj, event):
    """
    """
    if not is_richfilestreaming_installed():
        return
    print "atreal.richfile.streaming: clean data for %s" % ('/'.join(obj.getPhysicalPath()))
    IStreamable(obj).cleanUp()
