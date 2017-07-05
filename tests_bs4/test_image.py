# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from bs4 import BeautifulSoup
from django.core.files import File as DjangoFile
from django.http import QueryDict

from filer.models.foldermodels import Folder
from filer.models.imagemodels import Image

from cms.api import add_plugin
from cms.utils.plugins import build_plugin_tree

from cmsplugin_cascade import app_settings
from cmsplugin_cascade.models import SharableCascadeElement
from cms_bootstrap4.bootstrap.container import (
    Bootstrap4ContainerPlugin, Bootstrap4RowPlugin, Bootstrap4ColumnPlugin)
from cms_bootstrap4.bootstrap.image import BootstrapImagePlugin
from .test_base import CascadeTestCase

BS4_BREAKPOINT_KEYS = list(tp[0] for tp in app_settings.CMSPLUGIN_CASCADE['bootstrap4']['breakpoints'])


class ImagePluginTest(CascadeTestCase):
    maxDiff = None

    def upload_demo_image(self):
        demo_image = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets/demo_image.png'))
        folder, dummy = Folder.objects.get_or_create(name='Samples', parent=None)
        file_obj = DjangoFile(open(demo_image, 'rb'), name='demo_image.png')
        image = Image.objects.create(owner=self.user, original_filename='Demo Image',
                                     file=file_obj, folder=folder)
        return image

    def test_plugin_context(self):
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

        # add an image
        image_model = add_plugin(self.placeholder, BootstrapImagePlugin, 'en', target=column_model)
        self.assertIsInstance(image_model, SharableCascadeElement)
        image_plugin = image_model.get_plugin_class_instance()
        self.assertIsInstance(image_plugin, BootstrapImagePlugin)
        image_plugin.cms_plugin_instance = image_model.cmsplugin_ptr

        # upload an image and change the form
        ModelForm = image_plugin.get_form(self.request, image_model)
        image = self.upload_demo_image()
        post_data = QueryDict('', mutable=True)
        post_data.update({'image_file': image.pk, 'link_type': 'none', 'image_width_fixed': '300px'})
        image_model._image_model = image
        form = ModelForm(post_data, None, instance=image_model)
        self.assertTrue(form.is_valid())
        image_plugin.save_model(self.request, image_model, form, False)

        # render the plugins
        plugin_list = [container_model, row_model, column_model, image_model]
        build_plugin_tree(plugin_list)
        soup = BeautifulSoup(self.get_html(container_model, self.get_request_context()))
        self.assertEqual(soup.img['height'], '100')
        self.assertEqual(soup.img['width'], '300')
        self.assertTrue('demo_image.png__300x100_q85_subsampling-2' in str(soup.img))

        # use a responsive image
        post_data.setlist('image_shapes', ['img-fluid'])
        form = ModelForm(post_data, None, instance=image_model)
        self.assertTrue(form.is_valid())
        image_plugin.save_model(self.request, image_model, form, False)
        soup = BeautifulSoup(self.get_html(container_model, self.get_request_context()))
        self.assertTrue('img-fluid' in soup.img['class'])
        sizes = [s.strip() for s in soup.img['sizes'].split(',')]
        self.assertTrue('(max-width: 576px) -30px' in sizes)
        self.assertTrue('(min-width: 576px) and (max-width: 768px) 242px' in sizes)
        self.assertTrue('(min-width: 768px) and (max-width: 992px) 226px' in sizes)
        self.assertTrue('(min-width: 992px) and (max-width: 1200px) 218px' in sizes)
        self.assertTrue('(min-width: 1200px) 270px' in sizes)
        srcsets = [s.strip() for s in soup.img['srcset'].split(',')]
        self.assertEqual(len([s for s in srcsets if s.endswith('demo_image.png__242x81_q85_subsampling-2.jpg 242w')]), 1)
        self.assertEqual(len([s for s in srcsets if s.endswith('demo_image.png__226x75_q85_subsampling-2.jpg 226w')]), 1)
        self.assertEqual(len([s for s in srcsets if s.endswith('demo_image.png__218x73_q85_subsampling-2.jpg 218w')]), 1)
        self.assertEqual(len([s for s in srcsets if s.endswith('demo_image.png__270x90_q85_subsampling-2.jpg 270w')]), 1)
        self.assertTrue(soup.img['src'].endswith('demo_image.png__270x90_q85_subsampling-2.jpg'))
