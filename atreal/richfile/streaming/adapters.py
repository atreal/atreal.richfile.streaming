
import transaction

import sys
import urllib
import xmlrpclib

from zope.interface import implements

from atreal.richfile.qualifier.common import RFPlugin

from atreal.richfile.streaming.interfaces import IStreamable, IStreamingAudio, IStreamingVideo

# options control panel
from zope.component import queryUtility
from Products.CMFPlone.interfaces import IPloneSiteRoot
from atreal.richfile.streaming.browser.controlpanel import IRichFileStreamingSchema

from atreal.filestorage.common.interfaces import IOmniFile

def launchConversion(status, server, input, output, options, cb_url):
    """
    """
    if not status:
        return
    print "CALLBACK", cb_url
    try:
        jobId = server.convert(input, output, options, cb_url)
        print "atreal.richfile.streaming: ConvertDaemon call "+jobId
    #except xmlrpclib.Fault, e:
    except Exception, e:
        print "atreal.richfile.streaming: ConvertDaemon call FAILED", e
        server=xmlrpclib.Server(cb_url)
        server.conv_done_xmlrpc(e)
    #print "INPUT ", input_path
    #print "OUTPUT", output_path
    #return jobId


class ToStreamableObject(RFPlugin):
    """
    """
    implements(IStreamable)
    
    @property
    def convert_id(self):
        return 'streaming_convert' + "/".join(self.context.getPhysicalPath())

    @property
    def _options(self):
        return IRichFileStreamingSchema(queryUtility(IPloneSiteRoot))

    @property
    def convertdaemon_url(self):
        host = getattr (self._options, 'rfs_host', None)
        if host is None:
            return
        port = getattr (self._options, 'rfs_port', None)
        if port is None:
            return
        return ("http://%s:%s" % (host, port)).encode("ascii")

    @property
    def callback_netloc(self):
        return getattr (self._options, 'rfs_callback_netloc', None)
    
    @property
    def callback_user(self):
        return getattr (self._options, 'rfs_user', None)
    
    @property
    def callback_pwd(self):
        return getattr (self._options, 'rfs_pass', None)
    
    @property
    def isAudio(self):
        return IStreamingAudio.providedBy(self.context)

    @property
    def isVideo(self):
        return IStreamingVideo.providedBy(self.context)

    @property
    def outputFilename(self):
        if self.isVideo:
            return "streaming.flv"
        elif self.isAudio:
            return "streaming.mp3"

    @property
    def outputMimetype(self):
        if self.isVideo:
            return "video/x-flv"
        elif self.isAudio:
            return "audio/mpeg"
    
    def state(self):
        if not self.info.has_key('state'):
            self.info['state'] = "empty"
        return self.info['state']
    
    def process(self):
        """
        """
        print "\nPROCESS", self.convert_id
        #print "REQUEST", hash(self.context.REQUEST), self.context.REQUEST.form
        #print "REQUEST", getattr(self.context.REQUEST, "plop", None)
        if (self.convert_id in self.request_info) or ('tmp_omni_input' in self.info):
            print "WARNING: Already processing!!!"
            return
        print "atreal.richfile.streaming: processing..."
        
        #
        if self.context.getContentType() == "video/x-flv":
            self.setSubObject(self.outputFilename, self.context.getFile().data)
            print "atreal.richfile.streaming: built and stored!"
            self.info ['state'] = "ok"
            return
        
        # fichier origine en tmp
        in_mime_type = self.context.getContentType()
        if self.context.getField('file').getStorageName() == 'FileSystemStorage':
            self.info['tmp_omni_input'] = input_path = self.context.getFile().path
        else:
            infile = IOmniFile(self.context.getFile())
            self.info['tmp_omni_input'] = infile
            input_path = infile.displaceOnFS()
        
        # fichier converti en storage
        output = self.storage.getOrMakeFile(self.outputFilename)
        output_path = output.displaceOnFS()
        
        #
        server=xmlrpclib.Server(self.convertdaemon_url)
        
        #
        input=dict(path=input_path,type=in_mime_type)
        output=dict(path=output_path,type=self.outputMimetype)
        
        #
        options = dict()
        
        url_format = "http://%s:%s@%s%s/@@streaming_RPC"

        path = '/'.join(self.context.getPhysicalPath())
        
        cb_url = url_format % (self.callback_user,
                               self.callback_pwd,
                               self.callback_netloc,
                               urllib.quote(path))
        
        trans = transaction.get()
        trans.addAfterCommitHook(launchConversion, (server, input, output,
                                                    options, cb_url))

        self.info ['state'] = "processing"
        
        #print cb_url
        #try:
        #    jobId = server.convert(input, output, options, cb_url)
        #    self.info ['state'] = "processing"
        #except xmlrpclib.Fault:
        #    self.info ['state'] = "error"
        #    raise
        #self.request_info['streaming_convert'] = True
        #print "atreal.richfile.streaming: ConvertDaemon call "+jobId
        #print "INPUT ", input_path
        #print "OUTPUT", output_path
        #return jobId
        print "atreal.richfile.streaming: ConvertDaemon call pending"
        return True
    
    def _storeStreaming(self, ret):
        print "atreal.richfile.streaming: ConvertDaemon answer"
        if not 'tmp_omni_input' in self.info:
            #self.info ['state'] = "skeutuveux"
            print "NO conversion asked!!!"
            return
        try:
            if not isinstance(self.info['tmp_omni_input'], str):
                self.info['tmp_omni_input'].discardFromFS()
            del self.info['tmp_omni_input']
        except Exception, e:
            #exc = sys.exc_info()
            print "WARNING", e
            self.info ['state'] = "error"
            #raise e
        if ret:
            print "ERROR", ret
            self.info ['state'] = "error"
            self.storage.getOrMakeFile(self.outputFilename).discardFromFS()
            return
        #del self.request_info[self.convert_id]
        try:
            self.storage.getOrMakeFile(self.outputFilename).replaceFromFS()
            self.info ['state'] = "ok"
            print "atreal.richfile.streaming: built and stored!"
        except Exception, e:
            #exc = sys.exc_info()
            print "WARNING", e
            self.info ['state'] = "error"
            #raise e
    

