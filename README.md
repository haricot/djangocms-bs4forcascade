# djangocms-bs4forcascade     

Currently with bootstrap v4.0.0-alpha.6

Some templates and templatetags to be used with djangoCMS and Bootstrap4 with plugins for djangocms-casacde.

### how use this :
As in the bs3demo/example of djangocms-cascade, you have to modify the settings.py file like this:
```
INSTALLED_APPS = (
...
    'cms_bootstrap4',
...
)
```

```
CMSPLUGIN_CASCADE_PLUGINS = (
..
'cms_bootstrap4.bootstrap',
..
)
```

```
CACSCADE_WORKAREA_GLOSSARY = {
    'breakpoints': ['xs', 'sm', 'md', 'lg','xl'],
            'container_max_widths': {
                'xs': 0,
                'sm': 576,
                'md': 768,
                'lg': 992,
                'xl': 1200,
            },
    'fluid': False,
    'media_queries': {
                'xs': ['(max-width: 542px)'],
                'sm': ['(min-width: 544px)', '(max-width: 767px)'],
                'md': ['(min-width: 768px)', '(max-width: 991px)'],
                'lg': ['(min-width: 992px)', '(max-width: 1199px)'],
                'xl': ['(min-width: 1200px)'],
    },
}
```

```
CMS_PLACEHOLDER_CONF = {
    # this placeholder is used in templates/main.html, it shows how to
    # scaffold a djangoCMS page starting with an empty placeholder
    'Main Content': {
        'plugins': ['Bootstrap4ContainerPlugin', 'BootstrapJumbotronPlugin' ],'text_only_plugins': ['TextLinkPlugin'],
        'parent_classes': {'Bootstrap4ContainerPlugin': None, 'BootstrapJumbotronPlugin': None},
        'glossary': CACSCADE_WORKAREA_GLOSSARY,
    },
    # this placeholder is used in templates/wrapped.html, it shows how to
    # add content to an existing Bootstrap column
    'Bootstrap Column': {
        'plugins': ['Bootstrap4RowPlugin', 'TextPlugin', 'TextLinkPlugin' ],
        'parent_classes': {'Bootstrap4RowPlugin': None},
        'require_parent': False,
        'glossary': CACSCADE_WORKAREA_GLOSSARY,
    },
}
```

```
CMSPLUGIN_CASCADE = {
    'alien_plugins': ('TextPlugin', 'TextLinkPlugin',),
    'plugins_with_sharables': {
        'BootstrapImagePlugin': ('image_shapes', 'image_width_responsive', 'image_width_fixed',
                                 'image_height', 'resize_options',),
        'BootstrapPicturePlugin': ('image_shapes', 'responsive_heights', 'image_size', 'resize_options',),
        'BootstrapButtonPlugin': ('button_type', 'button_size', 'button_options', 'icon_font',),
        'TextLinkPlugin': ('link', 'target',),
    },
    # 'plugins_with_extra_fields': {
    #     'Bootstrap4RowPlugin': PluginExtraFieldsConfig(
    #         inline_styles={
    #             'extra_fields:Margins': ['margin-top', 'margin-bottom'],
    #             'extra_units:Margins': 'px,em',
    #         }
    #     ),
    #     'Bootstrap4ColumnPlugin': PluginExtraFieldsConfig(
    #         css_classes={'multiple': True, 'class_names': 'white'},
    #         inline_styles={
    #             'extra_fields:Height': ['height'],
    #             'extra_units:Height': 'px',
    #             'extra_fields:Paddings': ['padding-top', 'padding-right', 'padding-bottom', 'padding-left'],
    #             'extra_units:Paddings': 'px,em',
    #         }
    #     ),
    # },
    'exclude_hiding_plugin': ('SegmentPlugin', 'Badge'),
    'bootstrap4': {},
    'allow_plugin_hiding': True,
}


```

And replace all :
```
CMSPLUGIN_CASCADE['bootstrap3'] to CMSPLUGIN_CASCADE['bootstrap4']
```

## CHANGELOG

- 0.0.2 Initial release.
