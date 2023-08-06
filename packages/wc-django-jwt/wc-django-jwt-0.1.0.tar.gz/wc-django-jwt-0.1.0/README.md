# WebCase django JWT authentication

Based on [djangorestframework-simplejwt](https://pypi.org/project/djangorestframework-simplejwt/) with a little bit of additional goodies.

Us it's documentation as a source of truth. All changes and additional info about configuration are described here, in this documentation.

## Installation

```sh
pip install wc-django-jwt
```

In `settings.py`:

```python
INSTALLED_APPS += [
  'rest_framework_simplejwt',

  'wcd_jwt',
]
```
