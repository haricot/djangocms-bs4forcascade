# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict
from django.forms import widgets
from django.forms.fields import CharField
from django.forms.widgets import RadioFieldRenderer
from django.utils.html import format_html, format_html_join
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from cms.plugin_pool import plugin_pool
from cmsplugin_cascade.fields import GlossaryField
from cmsplugin_cascade.link.config import LinkPluginBase, LinkElementMixin, LinkForm
from cmsplugin_cascade.link.forms import TextLinkFormMixin
from cmsplugin_cascade.icon.mixins import IconPluginMixin


class ButtonTypeWidget(widgets.RadioSelect):
    """
    Render sample buttons in different colors in the button's backend editor.
    """
    BUTTON_TYPES = OrderedDict((('btn-primary', _("Primary")), ('btn-secondary', _("Secondary")),
        ('btn-success', _("Success")), ('btn-info', _("Info")), ('btn-warning', _("Warning")),
        ('btn-danger', _("Danger")), ('btn-link', _("Link")),))

    @classmethod
    def get_instance(cls):
        choices = tuple((k, v) for k, v in cls.BUTTON_TYPES.items())
        return cls(choices=choices)

    def render(self, name, value, attrs=None, renderer=None):
        renderer = self.get_renderer(name, value, attrs)
        return format_html('<div class="form-row">{}</div>',
            format_html_join('\n',
                '<div class="field-box"><span class="btn {1}">{2}</span><div class="label">{0}</div></div>',
                ((force_text(w), w.choice_value, force_text(self.BUTTON_TYPES[w.choice_value])) for w in renderer)))


class ButtonSizeWidget(widgets.RadioSelect):
    """
    Render sample buttons in different sizes in the button's backend editor.
    """
    BUTTON_SIZES = OrderedDict((('btn-lg', _("Large")), ('', _("Default")), ('btn-sm', _("Small")),))

    @classmethod
    def get_instance(cls):
        choices = tuple((k, v) for k, v in cls.BUTTON_SIZES.items())
        return cls(choices=choices)

    def render(self, name, value, attrs=None, renderer=None):
        renderer = self.get_renderer(name, value, attrs)
        return format_html('<div class="form-row">{}</div>',
            format_html_join('\n',
                '<div class="field-box"><div class="button-samples">'
                    '<span class="btn btn-primary {1}">{2}</span>'
                    '<span class="btn btn-default {1}">{2}</span></div>'
                    '<div class="label">{0}</div>'
                '</div>',
                ((force_text(w), w.choice_value, force_text(self.BUTTON_SIZES[w.choice_value])) for w in renderer)))


class BootstrapButtonMixin(IconPluginMixin):
    require_parent = True
    parent_classes = ('Bootstrap4ColumnPlugin', 'SimpleWrapperPlugin',)
    render_template = 'cascade/bootstrap4/button.html'
    allow_children = False
    default_css_class = 'btn'
    default_css_attributes = ('button_type', 'button_size', 'button_options', 'quick_float',)
    ring_plugin = 'ButtonMixin'

    button_type = GlossaryField(
        ButtonTypeWidget.get_instance(),
        label=_("Button Type"),
        initial='btn-primary',
        help_text=_("Display Link using this Button Style")
    )

    button_size = GlossaryField(
        ButtonSizeWidget.get_instance(),
        label=_("Button Size"),
        initial='',
        help_text=_("Display Link using this Button Size")
    )

    button_options = GlossaryField(
        widgets.CheckboxSelectMultiple(choices=(('btn-block', _('Block level')), ('disabled', _('Disabled')),)),
        label=_("Button Options"),
    )

#Added .float-{sm,md,lg,xl}-{left,right,none} classes for responsive floats and removed .pull-left and .pull-right since they’re redundant to .float-left and .float-right.
    quick_float = GlossaryField(
        widgets.RadioSelect(choices=(('', _("Do not float")), ('float-left', _("Float left")),
                                     ('float-right', _("Float right")),)),
        label=_("Quick Float"),
        initial='',
        help_text=_("Float the button to the left or right.")
    )

    icon_align = GlossaryField(
        widgets.RadioSelect(choices=(('', _("No Icon")), ('icon-left', _("Icon placed left")),
                                     ('icon-right', _("Icon placed right")),)),
        label=_("Icon alignment"),
        initial='',
        help_text=_("Add an Icon before or after the button content.")
    )

    icon_font = GlossaryField(
        widgets.Select(),
        label=_("Font"),
    )

    symbol = GlossaryField(
        widgets.HiddenInput(),
        label=_("Select Symbol"),
    )

    class Media:
        js = ['cascade/js/admin/buttonmixin.js']

    def render(self, context, instance, placeholder):
        context = super(BootstrapButtonMixin, self).render(context, instance, placeholder)
        icon_font = self.get_icon_font(instance)
        symbol = instance.glossary.get('symbol')
        if icon_font and symbol:
            context['stylesheet_url'] = icon_font.get_stylesheet_url()
            mini_template = '{0}<i class="icon-{1} {2}" aria-hidden="true"></i>{3}'
            icon_align = instance.glossary.get('icon_align')
            if icon_align == 'icon-left':
                context['icon_left'] = format_html(mini_template, '', symbol, 'cascade-icon-left', ' ')
            elif icon_align == 'icon-right':
                context['icon_right'] = format_html(mini_template, ' ', symbol, 'cascade-icon-right', '')
        return context


class Bootstrap4ButtonPlugin(BootstrapButtonMixin, LinkPluginBase):
    module = 'Bootstrap'
    name = _("Button")
    model_mixins = (LinkElementMixin,)
    fields = ('link_content',) + LinkPluginBase.fields
    glossary_field_order = ('button_type', 'button_size', 'button_options', 'quick_float',
                            'icon_align', 'icon_font', 'symbol')
    ring_plugin = 'ButtonPlugin'

    class Media:
        css = {'all': ['cascade-bs4/css/admin/bootstrap.min.css',
                       'cascade-bs4/css/admin/bootstrap-theme.min.css',
                       'cascade/css/admin/iconplugin.css']}
        js = ['cascade/js/admin/buttonplugin.js']

    @classmethod
    def get_identifier(cls, obj):
        identifier = super(Bootstrap4ButtonPlugin, cls).get_identifier(obj)
        content = obj.glossary.get('link_content')
        if not content:
            try:
                content = force_text(ButtonTypeRenderer.BUTTON_TYPES[obj.glossary['button_type']])
            except KeyError:
                content = _("Empty")
        return format_html('{}{}', identifier, content)

    def get_form(self, request, obj=None, **kwargs):
        link_content = CharField(required=False, label=_("Button Content"), widget=widgets.TextInput())
        Form = type(str('ButtonForm'), (TextLinkFormMixin, getattr(LinkForm, 'get_form_class')(),),
                    {'link_content': link_content})
        kwargs.update(form=Form)
        return super(Bootstrap4ButtonPlugin, self).get_form(request, obj, **kwargs)

plugin_pool.register_plugin(Bootstrap4ButtonPlugin)
