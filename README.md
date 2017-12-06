# djangocms-bs4forcascade     

Currently with bootstrap v4.0.0-beta2

Some templates and templatetags to be used with djangoCMS and Bootstrap4 with plugins for djangocms-casacde.

### how use djangocms-bs4forcascade :
As in the bs3demo/example of djangocms-cascade, you have to modify the settings.py file like this:

```
INSTALLED_APPS = (
...
    'cmsplugin_bs4forcascade',
...
)
```

```
CMSPLUGIN_CASCADE_PLUGINS = (
..
'cmsplugin_bs4forcascade.bootstrap4',
..
)
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
    'exclude_hiding_plugin': ('SegmentPlugin', 'Badge'),
    'bootstrap4': {},
    'allow_plugin_hiding': True,
}

```


```

And replace :
```
CMSPLUGIN_CASCADE['bootstrap3'] to CMSPLUGIN_CASCADE['bootstrap4']
```

## CHANGELOG

- 0.15.3v2bs4 Initial release.
