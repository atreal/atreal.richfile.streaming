from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.schema import TextLine, Choice, List, Bool, Password
from zope.formlib import form

from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_hasattr
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from atreal.richfile.streaming import RichFileStreamingMessageFactory as _
from atreal.richfile.streaming.interfaces import IStreamable

from atreal.richfile.qualifier.common import RFControlPanel
from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm


class IRFStreamingMainSchema(Interface):

    rf_streaming_collapsed = Bool(
        title=_(u"label_rf_streaming_collapsed",
                default=u"Display collapsed ?"),
        description=_(u"help_rf_streaming_collapsed",
                      default=u"Do you want the plugin's display to be collapsed ?"
                     ),
        default=False)    

    rfs_autoplay = Bool(
        title=_(u"label_rfs_autoplay",
                default=u"Auto Play ?"),
        description=_(u"help_rfs_autoplay",
                      default=u"Do you want the player start automatically "
                              u"when the page is loaded or do you want a user "
                              u"action to start it ?"),
        default=False)



class IRFStreamingConvertDaemonSchema(Interface):
    
    rfs_host = TextLine(title=_(u'label_rfs_host',
                                 default=u'ConvertDaemon host'),
                         description=_(u"help_rfs_host",
                                       default=u"The address of your "
                                       "ConvertDaemon server. Usually 'localhost', "
                                       "unless you use an external server."),
                         default=u'localhost',
                         required=True)

    rfs_port= TextLine(title=_(u'label_rfs_port',
                                 default=u'ConvertDaemon port'),
                         description=_(u"help_rfs_port",
                                       default=u"The port of your "
                                       "ConvertDaemon server. Usually '8888', "
                                       "unless you use another port."),
                         default=u'8888',
                         required=True)
    
    rfs_callback_netloc = TextLine(title=_(u'label_rfs_callback_netloc',
                                 default=u'ConvertDaemon callback netloc'),
                         description=_(u"help_rfs_callback_netloc",
                                       default=u"The address of your "
                                       "zope server."),
                         default=u'localhost:8650',
                         required=True)
    
    rfs_user = TextLine(title=_(u'label_rfs_user',
                                   default=u'ConvertDaemon username'),
                           description=_(u"help_rfs_user",
                                         default=u"Username for authentication "
                                         "of ConvertDaemon on Plone Site. "),
                           default=None,
                           required=True)
 
    rfs_pass = TextLine(title=_(u'label_rfs_pass',
                                 default=u'ConvertDaemon password'),
                         description=_(u"help_rfs_pass",
                                       default=u"The password for the ConvertDaemon "
                                       "user account."),
                         default=None,
                         required=True)
    
    

class IRichFileStreamingSchema(IRFStreamingMainSchema, IRFStreamingConvertDaemonSchema):
    """Combined schema for the adapter lookup.
    """
    

class RichFileStreamingControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IRichFileStreamingSchema)

    rf_streaming_collapsed = ProxyFieldProperty(IRichFileStreamingSchema['rf_streaming_collapsed'])
    rfs_autoplay = ProxyFieldProperty(IRichFileStreamingSchema['rfs_autoplay'])
    rfs_host = ProxyFieldProperty(IRichFileStreamingSchema['rfs_host'])
    rfs_port = ProxyFieldProperty(IRichFileStreamingSchema['rfs_port'])
    rfs_callback_netloc = ProxyFieldProperty(IRichFileStreamingSchema['rfs_callback_netloc'])
    rfs_user = ProxyFieldProperty(IRichFileStreamingSchema['rfs_user'])
    rfs_pass = ProxyFieldProperty(IRichFileStreamingSchema['rfs_pass'])

rfs_mainset = FormFieldsets(IRFStreamingMainSchema)
rfs_mainset.id = 'main'
rfs_mainset.label = _(u'label_rfs_main', default=u'Main')

rfs_convertdaemonset = FormFieldsets(IRFStreamingConvertDaemonSchema)
rfs_convertdaemonset.id = 'convertdaemon'
rfs_convertdaemonset.label = _(u'label_rfs_convertdaemon', default=u'ConvertDaemon')


class RichFileStreamingControlPanel(RFControlPanel):
    """
    """
    template = ZopeTwoPageTemplateFile('controlpanel.pt')
    form_fields = FormFieldsets(rfs_mainset, rfs_convertdaemonset)
    label = _("RichFileStreaming settings")
    description = _("RichFileStreaming settings for this site.")
    form_name = _("RichFileStreaming settings")
    plugin_iface = IStreamable
    supported_ifaces = ('atreal.richfile.streaming.interfaces.IStreaming',)
    
