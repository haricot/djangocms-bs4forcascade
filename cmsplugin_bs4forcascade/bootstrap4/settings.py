# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _


CASCADE_PLUGINS = getattr(settings, 'BS4_CASCADE_PLUGINS',
    ['buttons', 'carousel', 'accordion', 'container', 'image', 'picture','card',
     'tabs', 'gallery', 'jumbotron'],)

if 'cmsplugin_bs4forcascade' in settings.INSTALLED_APPS:
    CASCADE_PLUGINS.append('secondary_menu')


def set_defaults(config):
    config.setdefault('bootstrap4', {})
    config['bootstrap4'].setdefault(
        'breakpoints', (
            ('xs', (0, 'mobile', _("mobile phones"), 0, 542)),
            ('sm', (576, 'phablet', _("phablets"), 544, 767)),
            ('md', (768, 'tablet', _("tablets"), 768, 991)),
            ('lg', (992, 'laptop', _("laptops"), 992, 1199)),
            ('xl', (1200, 'desktop', _("large desktops"), 1200, 1980)),))
    for tpl in config['bootstrap4']['breakpoints']:
        if len(tpl[1]) != 5:
            msg = "The configuration directive CMSPLUGIN_CASCADE['bootstrap4']['bootstrap4']['{}'] requires 5 parameters"
            raise ImproperlyConfigured(msg.format(tpl[0]))

    config['bootstrap4'].setdefault('gutter', 30)

    config['plugins_with_extra_render_templates'].setdefault('BootstrapSecondaryMenuPlugin', (
        ('cascade/bootstrap4/secmenu-list-group.html', _("List Group")),
        ('cascade/bootstrap4/secmenu-unstyled-list.html', _("Unstyled List")),))

    if os.getenv('DJANGO_CLIENT_FRAMEWORK', '').startswith('angular'):
        config['bootstrap4']['template_basedir'] = 'angular-ui'
