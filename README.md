
# School Log (Django) #

This is the code base for my School Log application on Django.

## Installation #

With minor modifications, it could be included in an existing Django site.

### Bootstrap 4 Templates #

The templates assume the existence of a file called `site_bs4_base.html`,
which includes Bootstrap 4 CSS, JQuery, and `body` block.

The referenced base template in use is in 
[this repository](https://github.com/jfmario/blog-dj),
another part of my Django site.

### Forms #

The forms in `forms.py` extend `BootstrapModelForm`, which extends Django's
`ModelForm` and simply alters their properties to be Bootstrap 4 compliant.

### Urls #

The urls are all exported as `URLS` in `urls.py`. The sites main `urls.py`
should establish the base url as `/school-log` and then use the URLS
defined here.

## Visit #

The app is live [here](http://www.johnfmarion.com/school-log).