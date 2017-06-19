# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import warnings
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from cmsplugin_cascade.settings import CMSPLUGIN_CASCADE, orig_config

CASCADE_PLUGINS = ('buttons', 'carousel', 'accordion', 'container', 'image', 'picture', 'card',
                   'tabs', 'gallery', 'jumbotron')
if 'cms_bootstrap4' in settings.INSTALLED_APPS:
    CASCADE_PLUGINS += ('secondary_menu',)

if 'fluid-lg-width' in orig_config.get('bootstrap4', {}):
    msg = "The configuration directive CMSPLUGIN_CASCADE['bootstrap4']['fluid-lg-width'] in gone"
    warnings.warn(msg)

CMSPLUGIN_CASCADE['bootstrap4'] = {
    'breakpoints': (
        ('xs', (0, 'mobile', _("mobile phones"), 0, 542)),
        ('sm', (576, 'phablet', _("phablets"), 544, 767)),
        ('md', (768, 'tablet', _("tablets"), 768, 991)),
        ('lg', (992, 'laptop', _("laptops"), 992, 1199)),
        ('xl', (1200, 'desktop', _("large desktops"), 1200, 1980)),
    ),
    'gutter': 30,
}

CMSPLUGIN_CASCADE['bootstrap4'].update(orig_config.get('bootstrap4', {}))
for tpl in CMSPLUGIN_CASCADE['bootstrap4']['breakpoints']:
    if len(tpl[1]) != 5:
        msg = "The configuration directive CMSPLUGIN_CASCADE['bootstrap4']['bootstrap4']['{}'] requires 5 parameters"
        raise ImproperlyConfigured(msg.format(tpl[0]))

CMSPLUGIN_CASCADE['plugins_with_extra_render_templates'].setdefault('BootstrapSecondaryMenuPlugin', (
    ('cascade/bootstrap4/secmenu-list-group.html', _("default")),
    ('cascade/bootstrap4/secmenu-unstyled-list.html', _("unstyled")),
))
