# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
from django.test import override_settings
from cms.api import add_plugin
from cms.utils.plugins import build_plugin_tree
from cms_bootstrap4.bootstrap.container import (Bootstrap4ContainerPlugin, Bootstrap4RowPlugin,
        Bootstrap4ColumnPlugin)
from cms_bootstrap4.bootstrap.accordion import (BootstrapAccordionPlugin,
    BootstrapAccordionCardPlugin)
from cms_bootstrap4.bootstrap import settings
from .test_base import CascadeTestCase


BS4_BREAKPOINT_KEYS = list(tp[0] for tp in settings.CMSPLUGIN_CASCADE['bootstrap4']['breakpoints'])


class AccordionPluginTest(CascadeTestCase):

    def build_accordion_plugins(self):
        # create container
        container_model = add_plugin(self.placeholder, Bootstrap4ContainerPlugin, 'en',
            glossary={'breakpoints': BS4_BREAKPOINT_KEYS})
        container_plugin = container_model.get_plugin_class_instance()
        self.assertIsInstance(container_plugin, Bootstrap4ContainerPlugin)

        # add one row
        row_model = add_plugin(self.placeholder, Bootstrap4RowPlugin, 'en', target=container_model,
                               glossary={})
        row_plugin = row_model.get_plugin_class_instance()
        self.assertIsInstance(row_plugin, Bootstrap4RowPlugin)

        # add one column
        column_model = add_plugin(self.placeholder, Bootstrap4ColumnPlugin, 'en', target=row_model,
            glossary={'xs-column-width': 'col-12', 'sm-column-width': 'col-sm-6',
                      'md-column-width': 'col-md-4', 'lg-column-width': 'col-lg-3'})
        column_plugin = column_model.get_plugin_class_instance()
        self.assertIsInstance(column_plugin, Bootstrap4ColumnPlugin)

        # add accordion plugin
        accordion_model = add_plugin(self.placeholder, BootstrapAccordionPlugin, 'en', target=column_model)
        accordion_plugin = accordion_model.get_plugin_class_instance()
        self.assertIsInstance(accordion_plugin, BootstrapAccordionPlugin)
        accordion_plugin.cms_plugin_instance = accordion_model.cmsplugin_ptr

        # add accordion panel
        card_model = add_plugin(self.placeholder, BootstrapAccordionCardPlugin, 'en',
            target=accordion_model, glossary={'card_type': "card-danger", 'card_title': "Foo"})
        card_plugin = card_model.get_plugin_class_instance()
        self.assertIsInstance(card_plugin, BootstrapAccordionCardPlugin)
        card_plugin.cms_plugin_instance = card_model.cmsplugin_ptr

        # render the plugins
        plugin_list = [container_model, row_model, column_model, accordion_model, card_model]
        build_plugin_tree(plugin_list)

        self.assertEqual(accordion_plugin.get_identifier(accordion_model), 'with 1 card')
        self.assertEqual(card_plugin.get_identifier(card_model), 'Foo')

        return self.get_html(container_model, self.get_request_context())

    @override_settings()
    def test_bootstrap_accordion(self):
        try:
            del settings.CMSPLUGIN_CASCADE['bootstrap4']['template_basedir']
        except KeyError:
            pass
        html = self.build_accordion_plugins()
        soup = BeautifulSoup(html)
        panel_group = soup.find('div', class_='card-header')
        self.assertIsNotNone(panel_group)

#    @override_settings()
#    def test_angular_bootstrap_accordion(self):
#        settings.CMSPLUGIN_CASCADE['bootstrap4'].update({'template_basedir': 'angular-ui'})
#        html = self.build_accordion_plugins()
#        soup = BeautifulSoup(html)
#        accordion = soup.find('uib-accordion')
#        self.assertIsNotNone(accordion)
