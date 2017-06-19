# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http import QueryDict

from cms.api import add_plugin
from cms.toolbar.toolbar import CMSToolbar
from cms.utils.plugins import build_plugin_tree

from cmsplugin_cascade.models import CascadeElement, CascadeClipboard
from cms_bootstrap4.bootstrap.container import (Bootstrap4ContainerPlugin, Bootstrap4RowPlugin,
         BootstrapRowForm, Bootstrap4ColumnPlugin, BS4_BREAKPOINT_KEYS)
from .test_base import CascadeTestCase


class ClipboardPluginTest(CascadeTestCase):
    maxDiff = None
    identifier = "Test saved clipboard"
    placeholder_data = {'plugins': [['Bootstrap4ContainerPlugin', {
        'glossary': {'media_queries': {'md': ['(min-width: 768px)'] ,'sm': ['(max-width: 768px)']},
                     'container_max_widths': {'md': 768,'sm': 544}, 'fluid': '',
                     'breakpoints': ['sm', 'md']}},
                                     [['Bootstrap4RowPlugin', {'glossary': {}}, [
                                         ['Bootstrap4ColumnPlugin',
                                          {'glossary': {'sm-responsive-utils': '',
                                                        'md-column-offset': '',
                                                        'sm-column-width': 'col-sm-3',
                                                        'md-responsive-utils': '',
                                                        'md-column-ordering': '',
                                                        'sm-column-ordering': '',
                                                        'sm-column-offset': 'offset-sm-1',
                                                        'container_max_widths': {'md': 162.0,
                                                                                 'sm': 106.0},
                                                        'md-column-width': ''}}, []],
                                         ['Bootstrap4ColumnPlugin', {
                                             'glossary': {'sm-responsive-utils': 'hidden-sm',
                                                          'md-column-offset': '',
                                                          'sm-column-width': 'col-sm-4',
                                                          'md-responsive-utils': '',
                                                          'md-column-ordering': '',
                                                          'sm-column-ordering': '',
                                                          'sm-column-offset': '',
                                                          'container_max_widths': {'md': 226.0,
                                                                                   'sm': 151.33},
                                                          'md-column-width': ''}}, []],
                                         ['Bootstrap4ColumnPlugin', {
                                            'glossary': {
                                                'container_max_widths': {
                                                    'sm': 151.33,
                                                    'md': 226.0},
                                                    'sm-column-width': 'col-sm-4'
                                                   }},
                                                   []]]]]]]}

    def setUp(self):
        super(ClipboardPluginTest, self).setUp()
        UserModel = get_user_model()
        self.admin_user = UserModel.objects.get(username='admin')

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
        self.assertInHTML(
            '<input id="id_glossary_breakpoints_0" name="breakpoints" type="checkbox" value="xs" />',
            html)
        self.assertInHTML(
            '<input checked="checked" id="id_glossary_breakpoints_2" name="breakpoints" type="checkbox" value="md" />',
            html)
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
        row_data = []
        for column_model in columns_qs:
            self.assertIsInstance(column_model, CascadeElement)
            column_plugin = column_model.get_plugin_class_instance()
            self.assertIsInstance(column_plugin, Bootstrap4ColumnPlugin)
            self.assertEqual(column_model.parent.id, row_model.id)
            self.assertEqual(str(column_model), 'default width: 4 units')
            plugin_list.append(column_model)
            row_data.append(['Bootstrap4ColumnPlugin', {'glossary': column_model.glossary}, []])
        # container_data = ['Bootstrap4RowPlugin', {'glossary': row_model.glossary}, row_data]

        # Render the Container Plugin with all of its children
        build_plugin_tree(plugin_list)
        html = self.get_html(container_model, self.get_request_context())
        self.assertHTMLEqual(html, '<div class="container"><div class="row">' +
                             '<div class="col-sm-4"></div><div class="col-sm-4"></div>' +
                             '<div class="col-sm-4"></div>' +
                             '</div></div>')

        # change data inside the first column
        column_model = columns_qs[0]
        delattr(column_model, '_inst')
        column_plugin = column_model.get_plugin_class_instance(self.admin_site)
        column_plugin.cms_plugin_instance = column_model
        post_data = QueryDict('', mutable=True)
        post_data.update({'sm-column-offset': 'offset-sm-1', 'sm-column-width': 'col-sm-3'})
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
                             '<div class="col-sm-3 offset-sm-1"></div>' +
                             '<div class="col-sm-4 hidden-sm"></div><div class="col-sm-4"></div>' +
                             '</div></div>')

    def test_save_clipboard(self):
        with self.login_user_context(self.admin_user):
            request = self.get_request('/')
            request.toolbar = CMSToolbar(request)
            self.assertIsNotNone(request.toolbar.clipboard)
            data = {'source_placeholder_id': self.placeholder.pk, 'source_plugin_id': '',
                'source_language': 'en', 'target_plugin_id': '',
                'target_placeholder_id': request.toolbar.clipboard.pk, 'target_language': 'en'}

            # check that clipboard is empty
            self.assertEqual(request.toolbar.clipboard.cmsplugin_set.count(), 0)

            # copy plugins from placeholder to clipboard
            copy_plugins_url = reverse('admin:cms_page_copy_plugins')  # + '?cms_path=%2Fen%2F'
            response = self.client.post(copy_plugins_url, data)
            self.assertEqual(response.status_code, 200)

            # serialize and persist clipboard content
            add_clipboard_url = reverse('admin:cmsplugin_cascade_cascadeclipboard_add')
            data = {'identifier': self.identifier, 'save_clipboard': 'Save', 'data': {}}
            response = self.client.post(add_clipboard_url, data)
            self.assertEqual(response.status_code, 302)
            change_clipboard_url = response['location']
            response = self.client.get(change_clipboard_url, data)
            soup = BeautifulSoup(response.content)
            ul = soup.find('ul', class_='messagelist')
            self.assertEqual(ul.li.text, 'The Persited Clipboard Content "Test saved clipboard" was added successfully. You may edit it again below.')
            self.assertEqual(CascadeClipboard.objects.all().count(), 1)

            # now examine the serialized data in the clipboard
            cascade_clipboard = CascadeClipboard.objects.get(identifier=self.identifier)
            print(cascade_clipboard.data)
            self.assertDictEqual(cascade_clipboard.data, self.placeholder_data)

    def test_restore_clipboard(self):
        with self.login_user_context(self.admin_user):
            cascade_clipboard = CascadeClipboard.objects.create(identifier=self.identifier, data=self.placeholder_data)
            cascade_clipboard.save()
            request = self.get_request('/')
            request.toolbar = CMSToolbar(request)
            self.assertIsNotNone(request.toolbar.clipboard)

            # check that clipboard is empty
            self.assertEqual(request.toolbar.clipboard.cmsplugin_set.count(), 0)

            # copy plugins from CascadeClipboard to CMS clipboard
            change_clipboard_url = reverse('admin:cmsplugin_cascade_cascadeclipboard_change', args=(cascade_clipboard.pk,))
            data = {'identifier': self.identifier, 'restore_clipboard': 'Restore', 'data': json.dumps(self.placeholder_data)}
            response = self.client.post(change_clipboard_url, data)
            self.assertEqual(response.status_code, 302)
            change_clipboard_url = response['location']
            response = self.client.get(change_clipboard_url, data)
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.content, 'html.parser')
            ul = soup.find('ul', class_='messagelist')
            self.assertEqual(ul.li.text, 'The Persited Clipboard Content "Test saved clipboard" was changed successfully. You may edit it again below.')

            # check if clipboard has been populated with plugins from serialized data
            ref_plugin = request.toolbar.clipboard.get_plugins().first()
            self.assertEqual(ref_plugin.plugin_type, 'PlaceholderPlugin')
            inst = ref_plugin.get_plugin_instance()[0]
            plugins = inst.placeholder_ref.get_plugins()
            self.assertEqual(plugins.count(), 5)
            self.assertEqual(plugins[0].plugin_type, 'Bootstrap4ContainerPlugin')
            self.assertEqual(plugins[1].plugin_type, 'Bootstrap4RowPlugin')
            self.assertEqual(plugins[2].plugin_type, 'Bootstrap4ColumnPlugin')
