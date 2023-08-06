from zope.component import adapter
from plone.registry.interfaces import IRecordModifiedEvent
from Products.CMFPlone.interfaces import ISiteSchema
from plone.formwidget.namedfile.converter import b64decode_file
import mimetypes
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.registry.recordsproxy import RecordsProxy


@adapter(ISiteSchema, IRecordModifiedEvent)
def updateMimetype(settings: RecordsProxy, event: IRecordModifiedEvent=None):

    if event.record.fieldName != 'site_favicon' or not event.record.value:
        return

    filename = b64decode_file(event.newValue)[0]
    mimetype = mimetypes.guess_type(filename)[0] if filename else None
    if mimetype in ('image/x-icon', None):
        # Override incorrect MIME type registered in both PIL and the
        # Products.MimetypesRegistry product.
        mimetype = 'image/vnd.microsoft.icon'
    settings.__registry__['plone.site_favicon_mimetype'] = mimetype
