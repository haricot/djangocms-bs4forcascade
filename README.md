djangocms-bs4forcascade     
================================================================================================================================
djangocms-bs4forcascade is very similar to [jrief/djangocms-cascade](https://github.com/jrief/djangocms-cascade/), the code has been adapted for bootstrap 4,

Currently with bootstrap v4.1.1

Some templates and templatetags to be used with djangoCMS and Bootstrap4 with plugins for [jrief/djangocms-cascade](https://github.com/jrief/djangocms-cascade/).



### How use djangocms-bs4forcascade :
As in the examples/bs3demo of [jrief/djangocms-cascade](https://github.com/jrief/djangocms-cascade/) of , bs4demo is very similar:


```
$ git clone --depth=1 https://github.com/haricot/djangocms-bs4forcascade
$ cd djangocms-bs4forcascade
$ virtualenv cascadenv
$ source cascadenv/bin/activate
(cascadenv)$ pip install -r requirements/django111.txt
```

```
$ cd examples
$ npm install
$ ./manage.py migrate
$ ./manage.py createsuperuser
$ ./manage.py runserver
```


## CHANGELOG

- 0.16_bs4 Update release.
