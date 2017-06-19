# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, re
from bs4 import BeautifulSoup
from django.core.files import File as DjangoFile
from django.http import QueryDict

from filer.models.foldermodels import Folder
from filer.models.imagemodels import Image

from cms.api import add_plugin
from cms.utils.plugins import build_plugin_tree
from cms_bootstrap4.bootstrap import settings
from cmsplugin_cascade.models import SharableCascadeElement
from cms_bootstrap4.bootstrap.container import (Bootstrap4ContainerPlugin, Bootstrap4RowPlugin,
        Bootstrap4ColumnPlugin)
from cms_bootstrap4.bootstrap.picture import BootstrapPicturePlugin
from .test_base import CascadeTestCase

BS4_BREAKPOINT_KEYS = list(tp[0] for tp in settings.CMSPLUGIN_CASCADE['bootstrap4']['breakpoints'])


class PicturePluginTest(CascadeTestCase):
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

        # add a picture
        picture_model = add_plugin(self.placeholder, BootstrapPicturePlugin, 'en', target=column_model)
        self.assertIsInstance(picture_model, SharableCascadeElement)
        picture_plugin = picture_model.get_plugin_class_instance()
        self.assertIsInstance(picture_plugin, BootstrapPicturePlugin)
        picture_plugin.cms_plugin_instance = picture_model.cmsplugin_ptr

        # upload an image and change the form
        ModelForm = picture_plugin.get_form(self.request, picture_model)
        image = self.upload_demo_image()
        post_data = QueryDict('', mutable=True)
        post_data.update({'image_file': image.pk, 'link_type': 'none',
            'responsive_heights-xs': '50%', 'responsive_heights-sm': '66%',
            'responsive_heights-md': '75%', 'responsive_heights-lg': '100%',
            'responsive_zoom-lg': '40%', 'responsive_zoom-lg': '25%',
            'responsive_zoom-lg': '15%', 'responsive_zoom-lg': '0%'})
        post_data.setlist('resize_options', ['crop'])
        picture_model._image_model = image
        form = ModelForm(post_data, None, instance=picture_model)
        self.assertTrue(form.is_valid())
        picture_plugin.save_model(self.request, picture_model, form, False)

        # render the plugins
        plugin_list = [container_model, row_model, column_model, picture_model]
        build_plugin_tree(plugin_list)
        soup = BeautifulSoup(self.get_html(container_model, self.get_request_context()))
        self.assertEqual(soup.img['height'], '90')
        self.assertEqual(soup.img['width'], '270')
        self.assertTrue('demo_image.png__270x90_q85_crop_subsampling-2.jpg' in str(soup.img))
        sources = dict((s['media'], s['srcset']) for s in soup.picture.find_all('source'))
        self.assertTrue('demo_image.png__242x53_q85_crop_subsampling-2.jpg' in sources['(min-width: 576px) and (max-width: 768px)'])
        self.assertTrue('demo_image.png__226x56_q85_crop_subsampling-2.jpg' in sources['(min-width: 768px) and (max-width: 992px)'])
        self.assertTrue('demo_image.png__218x73_q85_crop_subsampling-2.jpg' in sources['(min-width: 992px) and (max-width: 1200px)'])
        # Due to an different round implimentation in python3 height can vary by 1 to 2 pixels
        # self.assertTrue(bool(re.search(r'demo_image.png__262x8\d_q85_crop_subsampling-2.jpg$', sources['(min-width: 1200px)'])))
        self.assertTrue(bool(re.search(r'/demo_image.png__270x9\d_q85_crop_subsampling-2.jpg$', sources['(min-width: 1200px)'])))

        # with Retina images
        post_data.setlist('resize_options', ['crop', 'high_resolution'])
        form = ModelForm(post_data, None, instance=picture_model)
        self.assertTrue(form.is_valid())
        picture_plugin.save_model(self.request, picture_model, form, False)
        soup = BeautifulSoup(self.get_html(container_model, self.get_request_context()))
        self.assertEqual(soup.img['height'], '90')
        self.assertEqual(soup.img['width'], '270')
        self.assertTrue('demo_image.png__270x90_q85_crop_subsampling-2.jpg' in soup.img['src'])
        sources = dict((s['media'], s['srcset']) for s in soup.picture.find_all('source'))
        print(sources)
        self.assertTrue('demo_image.png__242x53_q85_crop_subsampling-2.jpg 1x' in sources['(min-width: 576px) and (max-width: 768px)'])
        self.assertTrue('demo_image.png__484x106_q85_crop_subsampling-2.jpg 2x' in sources['(min-width: 576px) and (max-width: 768px)'])
        self.assertTrue('demo_image.png__226x56_q85_crop_subsampling-2.jpg 1x' in sources['(min-width: 768px) and (max-width: 992px)'])
        self.assertTrue('demo_image.png__452x112_q85_crop_subsampling-2.jpg 2x' in sources['(min-width: 768px) and (max-width: 992px)'])
        self.assertTrue('demo_image.png__218x73_q85_crop_subsampling-2.jpg 1x' in sources['(min-width: 992px) and (max-width: 1200px)'])
        self.assertTrue('demo_image.png__436x146_q85_crop_subsampling-2.jpg 2x' in sources['(min-width: 992px) and (max-width: 1200px)'])

        # Due to an different round implimentation in python3 height can vary by 1 to 2 pixels
        self.assertTrue(bool(re.search(r'demo_image.png__270x9\d_q85_crop_subsampling-2.jpg\s1x', sources['(min-width: 1200px)'])))
        self.assertTrue(bool(re.search(r'demo_image.png__540x18\d_q85_crop_subsampling-2.jpg\s2x', sources['(min-width: 1200px)'])))
