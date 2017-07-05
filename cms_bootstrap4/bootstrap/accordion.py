# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from html.parser import HTMLParser  # py3
except ImportError:
    from HTMLParser import HTMLParser  # py2
from django.forms import widgets
from django.utils.translation import ungettext_lazy, ugettext_lazy as _
from django.utils.text import Truncator
from django.utils.html import format_html
from django.forms.models import ModelForm
from django.forms.fields import IntegerField

from cms.plugin_pool import plugin_pool
from cmsplugin_cascade.forms import ManageChildrenFormMixin
from cmsplugin_cascade.fields import GlossaryField
from cmsplugin_cascade.plugin_base import TransparentWrapper, TransparentContainer
from cmsplugin_cascade.widgets import NumberInputWidget

from .plugin_base import Bootstrap4PluginBase
from .card import card_heading_sizes, CardTypeRenderer


class AccordionForm(ManageChildrenFormMixin, ModelForm):
    num_children = IntegerField(min_value=1, initial=1,
        widget=NumberInputWidget(attrs={'size': '3', 'style': 'width: 5em !important;'}),
        label=_("Cards"),
        help_text=_("Number of cards for this card group."))


class BootstrapAccordionPlugin(TransparentWrapper, Bootstrap4PluginBase):
    name = _("Accordion")
    form = AccordionForm
    default_css_class = 'panel-group'
    require_parent = True
    parent_classes = ('Bootstrap4ColumnPlugin',)
    direct_child_classes = ('BootstrapAccordionCardPlugin',)
    allow_children = True
    render_template = 'cascade/bootstrap4/{}/accordion.html'
    fields = ('num_children', 'glossary',)

    close_others = GlossaryField(
         widgets.CheckboxInput(),
         label=_("Close others"),
         initial=True,
         help_text=_("Open only one card at a time.")
    )

    first_is_open = GlossaryField(
         widgets.CheckboxInput(),
         label=_("First card open"),
         initial=True,
         help_text=_("Start with the first card open.")
    )

    @classmethod
    def get_identifier(cls, obj):
        identifier = super(BootstrapAccordionPlugin, cls).get_identifier(obj)
        num_cols = obj.get_children().count()
        content = ungettext_lazy('with {0} card', 'with {0} cards', num_cols).format(num_cols)
        return format_html('{0}{1}', identifier, content)

    def save_model(self, request, obj, form, change):
        wanted_children = int(form.cleaned_data.get('num_children'))
        super(BootstrapAccordionPlugin, self).save_model(request, obj, form, change)
        self.extend_children(obj, wanted_children, BootstrapAccordionCardPlugin)

plugin_pool.register_plugin(BootstrapAccordionPlugin)


class BootstrapAccordionCardPlugin(TransparentContainer, Bootstrap4PluginBase):
    name = _("Accordion Card")
    default_css_class = 'card'
    direct_parent_classes = parent_classes = ('BootstrapAccordionPlugin',)
    require_parent = True
    alien_child_classes = True
    render_template = 'cascade/bootstrap4/{}/accordion-card.html'
    glossary_field_order = ('card_type', 'heading_size', 'card_title')

    card_type = GlossaryField(
        CardTypeRenderer.get_widget(),
        label=_("Card type"),
        help_text=_("Display Card using this style.")
    )

    heading_size = GlossaryField(
        widgets.Select(choices=card_heading_sizes),
        initial='',
        label=_("Heading Size")
    )

    card_title = GlossaryField(
        widgets.TextInput(attrs={'size': 80}),
        label=_("Card Title")
    )

    class Media:
        css = {'all': ('cascade/css/admin/bootstrap.min.css', 'cascade/css/admin/bootstrap-theme.min.css',)}

    @classmethod
    def get_identifier(cls, obj):
        identifier = super(BootstrapAccordionCardPlugin, cls).get_identifier(obj)
        card_title = HTMLParser().unescape(obj.glossary.get('card_title', ''))
        card_title = Truncator(card_title).words(3, truncate=' ...')
        return format_html('{0}{1}', identifier, card_title)

plugin_pool.register_plugin(BootstrapAccordionCardPlugin)
