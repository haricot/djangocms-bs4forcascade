djangocms-bs4forcascade     
================================================================================================================================

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



And replace :
```
CMSPLUGIN_CASCADE['bootstrap3'] to CMSPLUGIN_CASCADE['bootstrap4']
```

And replace :

```
'BootstrapContainerPlugin' to 'Bootstrap4ContainerPlugin'
'BootstrapRowPlugin' to 'Bootstrap4RowPlugin'
'BootstrapColumnPlugin' to 'Bootstrap4ColumnPlugin'
'BootstrapButtonPlugin' to 'Bootstrap4ButtonPlugin'

```

## CHANGELOG

- 0.15.4v2bs4 Update release. 
- 0.15.3v2bs4 Initial release.

