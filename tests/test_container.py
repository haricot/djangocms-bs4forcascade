# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import QueryDict
from cms.api import add_plugin, create_page
from cms.utils.plugins import build_plugin_tree
from cmsplugin_cascade.models import CascadeElement
from cms_bootstrap4.bootstrap.container import (Bootstrap4ContainerPlugin, Bootstrap4RowPlugin,
         BootstrapRowForm, Bootstrap4ColumnPlugin, BS4_BREAKPOINT_KEYS)
from .test_base import CascadeTestCase


class ContainerPluginTest(CascadeTestCase):

    def test_container_context(self):
        # add a Bootstrap Container Plugin
        container_model = add_plugin(self.placeholder, Bootstrap4ContainerPlugin, 'en',
            glossary={'breakpoints': BS4_BREAKPOINT_KEYS})
        self.assertIsInstance(container_model, CascadeElement)
        container_plugin = container_model.get_plugin_class_instance(self.admin_site)
        self.assertIsInstance(container_plugin, Bootstrap4ContainerPlugin)
        ModelForm = container_plugin.get_form(self.request, container_model)
        post_data = QueryDict('', mutable=True)
        post_data.setlist('breakpoints', ['sm', 'md'])
        form = ModelForm(post_data, None, instance=container_model)
        html = form.as_p()
        self.assertInHTML('<input id="id_glossary_breakpoints_0" name="breakpoints" type="checkbox" value="xs" />', html)
        self.assertInHTML('<input checked="checked" id="id_glossary_breakpoints_2" name="breakpoints" type="checkbox" value="md" />', html)
        self.assertInHTML('<input id="id_glossary_fluid" name="fluid" type="checkbox" />', html)
        container_plugin.save_model(self.request, container_model, form, False)
        self.assertListEqual(container_model.glossary['breakpoints'], ['sm', 'md'])
        self.assertTrue('fluid' in container_model.glossary)
        self.assertEqual(str(container_model), 'for phablets, tablets')

        # add a RowPlugin with 3 Columns
        row_model = add_plugin(self.placeholder, Bootstrap4RowPlugin, 'en', target=container_model)
        row_plugin = row_model.get_plugin_class_instance()
        row_change_form = BootstrapRowForm({'num_children': 3})
        row_change_form.full_clean()
        row_plugin.save_model(self.request, row_model, row_change_form, False)
        self.assertDictEqual(row_model.glossary, {})
        self.assertIsInstance(row_model, CascadeElement)
        self.assertEqual(str(row_model), 'with 3 columns')
        plugin_list = [container_model, row_model]
        columns_qs = CascadeElement.objects.filter(parent_id=row_model.id)
        self.assertEqual(columns_qs.count(), 3)
        for column_model in columns_qs:
            self.assertIsInstance(column_model, CascadeElement)
            column_plugin = column_model.get_plugin_class_instance()
            self.assertIsInstance(column_plugin, Bootstrap4ColumnPlugin)
            self.assertEqual(column_model.parent.id, row_model.id)
            self.assertEqual(str(column_model), 'default width: 4 units')
            plugin_list.append(column_model)

        # Render the Container Plugin with all of its children
        build_plugin_tree(plugin_list)
        html = self.get_html(container_model, self.get_request_context())
        self.assertHTMLEqual(html, '<div class="container"><div class="row">' +
            '<div class="col-sm-4"></div><div class="col-sm-4"></div><div class="col-sm-4"></div>' +
            '</div></div>')

        # change data inside the first column
        column_model = columns_qs[0]
        delattr(column_model, '_inst')
        column_plugin = column_model.get_plugin_class_instance(self.admin_site)
        column_plugin.cms_plugin_instance = column_model
        post_data = QueryDict('', mutable=True)
        post_data.update({'sm-column-offset': 'col-sm-offset-1', 'sm-column-width': 'col-sm-3'})
        ModelForm = column_plugin.get_form(self.request, column_model)
        form = ModelForm(post_data, None, instance=column_model)
        self.assertTrue(form.is_valid())
        column_plugin.save_model(self.request, column_model, form, True)

        # change data inside the second column
        column_model = columns_qs[1]
        delattr(column_model, '_inst')
        column_plugin = column_model.get_plugin_class_instance(self.admin_site)
        column_plugin.cms_plugin_instance = column_model
        post_data = QueryDict('', mutable=True)
        post_data.update({'sm-responsive-utils': 'hidden-sm', 'sm-column-width': 'col-sm-4'})
        ModelForm = column_plugin.get_form(self.request, column_model)
        form = ModelForm(post_data, None, instance=column_model)
        self.assertTrue(form.is_valid())
        column_plugin.save_model(self.request, column_model, form, False)
        html = self.get_html(container_model, self.get_request_context())
        self.assertHTMLEqual(html, '<div class="container"><div class="row">' +
            '<div class="col-sm-3 col-sm-offset-1"></div><div class="col-sm-4 hidden-sm"></div><div class="col-sm-4"></div>' +
            '</div></div>')
