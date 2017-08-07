# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict
try:
    from html.parser import HTMLParser  # py3
except ImportError:
    from HTMLParser import HTMLParser  # py2
from django.forms import widgets
from django.forms.widgets import RadioFieldRenderer
from django.utils.html import format_html, format_html_join
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from cmsplugin_cascade.fields import GlossaryField
from cmsplugin_cascade.plugin_base import TransparentContainer
from .plugin_base import Bootstrap4PluginBase

modal_heading_sizes = (('', _("normal")),) + tuple(('h{}'.format(k), _("Heading {}").format(k)) for k in range(1, 7))


class BootstrapModalPlugin(TransparentContainer, Bootstrap4PluginBase):
    """
    Use this plugin to display a modal with optional modal-header and modal-footer.
    """
    name = _("Modal")
    default_css_class = 'fade'
    require_parent = False
    parent_classes = ('Bootstrap4ColumnPlugin',)
    allow_children = True
    child_classes = None
    render_template = 'cascade/bootstrap4/modal.html'
    glossary_field_order = ('modal_type', 'modal_sizes', 'heading_size', 'heading', 'footer')

    modal_sizes = GlossaryField(
        widgets.RadioSelect(choices=(('', _("Do not define")), ('modal-sm', _("Small modal")),
                                     ('modal-lg', _("Large modal")),)),
        label=_("Modal Sizes"),
        initial='',
        help_text=_("Select Modal Sizes")
    )

    heading_size = GlossaryField(
        widgets.Select(choices=modal_heading_sizes),
        initial='',
        label=_("Heading Size")
    )

    heading = GlossaryField(
        widgets.TextInput(attrs={'size': 80}),
        label=_("Modal Heading")
    )

    footer = GlossaryField(
        widgets.TextInput(attrs={'size': 80}),
        label=_("Modal Footer")
    )

    html_parser = HTMLParser()

    class Media:
        css = {'all': ('cascade-bs4/css/admin/bootstrap.min.css', 'cascade-bs4/css/admin/bootstrap-theme.min.css',)}

    def render(self, context, instance, placeholder):
        heading = self.html_parser.unescape(instance.glossary.get('heading', ''))
        footer = self.html_parser.unescape(instance.glossary.get('footer', ''))
        context.update({
            'instance': instance,
            'modal_type': instance.glossary.get('modal_type', 'modal-default'),
            'modal_size':instance.glossary.get('modal_sizes'),
            'modal_heading': heading,
            'heading_size': instance.glossary.get('heading_size', ''),
            'modal_footer': footer,
            'placeholder': placeholder,
        })
        return super(BootstrapModalPlugin, self).render(context, instance, placeholder)

plugin_pool.register_plugin(BootstrapModalPlugin)
