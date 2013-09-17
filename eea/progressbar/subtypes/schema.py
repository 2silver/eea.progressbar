""" Schema extender for Disable Autolinks for context/page
"""
from zope.interface import implements
from zope.component import queryAdapter
from zope.component.hooks import getSite
from Products.Archetypes.public import BooleanField, BooleanWidget
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.field import ExtensionField
from eea.progressbar.config import EEAMessageFactory as _
from eea.progressbar.interfaces import IProgressBarLayer
from eea.progressbar.controlpanel.interfaces import ISettings

class EEABooleanField(ExtensionField, BooleanField):
    """ BooleanField for schema extender
    """

class EEASchemaExtender(object):
    """ Schema extender for content types with data provenance
    """
    implements(ISchemaExtender, IBrowserLayerAwareExtender)
    layer = IProgressBarLayer

    fields = (
        EEABooleanField(
            name='disableProgressBarViewlet',
            schemata='settings',
            default=False,
            searchable=False,
            widget=BooleanWidget(
                label=_('Hide Progress Bar Viewlet'),
                description=_('Hide Progress Bar viewlet for '
                              'this context/page'),
            )
        ),
    )

    def __init__(self, context):
        self.context = context

    def getFields(self):
        """ Returns provenance list field
        """
        settings = queryAdapter(getSite(), ISettings)
        ctype = getattr(self.context, 'portal_type', '')
        allowed = settings.viewletVisibleFor or []
        if ctype in allowed:
            return self.fields
        return ()
