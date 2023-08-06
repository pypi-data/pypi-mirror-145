# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['salesman_paypal']

package_data = \
{'': ['*'], 'salesman_paypal': ['templates/salesman_paypal/*']}

install_requires = \
['django-salesman>=1.1.3',
 'django>=3.1,<4.1',
 'paypal-checkout-serversdk>=1.0.1,<1.1.0']

setup_kwargs = {
    'name': 'django-salesman-paypal',
    'version': '0.1.3',
    'description': 'PayPal payment integration for Salesman.',
    'long_description': "# Salesman PayPal\n\n[![PyPI](https://img.shields.io/pypi/v/django-salesman-paypal)](https://pypi.org/project/django-salesman-paypal/)\n[![Test](https://img.shields.io/github/workflow/status/dinoperovic/django-salesman-paypal/Test/master)](https://github.com/dinoperovic/django-salesman-paypal/actions?query=workflow:Test)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-salesman-paypal)](https://pypi.org/project/django-salesman-paypal/)\n[![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-salesman-paypal)](https://pypi.org/project/django-salesman-paypal/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n[PayPal](https://www.paypal.com/) payment integration for [Salesman](https://github.com/dinoperovic/django-salesman).\n\n## Installation\n\nInstall the package using pip:\n\n```bash\npip install django-salesman-paypal\n```\n\nAdd to your setting file:\n\n```python\nINSTALLED_APPS = ['salesman_paypal']\nSALESMAN_PAYMENT_METHODS = ['salesman_paypal.payment.PayPalPayment']\nSALESMAN_PAYPAL_CLIENT_ID = '<paypal-client-id>'\nSALESMAN_PAYPAL_CLIENT_SECRET = '<paypal-client-secret>'\nSALESMAN_PAYPAL_SANDBOX_MODE = True  # Disable in production\n```\n\n### Usage guide\n\nTo use this payment on your website, checkout the official PayPal server [integration guide](https://developer.paypal.com/demo/checkout/#/pattern/server).\n\nSee `example` directory in this repository for integration example using JavaScript.\n\n### Additional settings\n\nOptional additional settings that you can override:\n\n```python\n# Payment method label used when displayed in the basket.\nSALESMAN_PAYPAL_PAYMENT_LABEL = 'Pay with PayPal'\n\n# Default PayPal currency used for payments (https://developer.paypal.com/docs/reports/reference/paypal-supported-currencies/)\nSALESMAN_PAYPAL_DEFAULT_CURRENCY = 'USD'\n\n# URL to redirect to when PayPal payment is approved.\nSALESMAN_PAYPAL_RETURN_URL = '/paypal/return/'\n\n# URL to redirect to when PayPal payment is cancelled.\nSALESMAN_PAYPAL_CANCEL_URL = '/paypal/cancel/'\n\n# Default paid status for fullfiled orders.\nSALESMAN_PAYPAL_PAID_STATUS = 'PROCESSING'\n```\n\n## Advanced usage\n\nTo gain more control feel free to extend the `PayPalPayment` class with your custom functionality:\n\n```python\n# shop/payment.py\nfrom salesman_paypal.payment import PayPalPayment\nfrom salesman_paypal.conf import app_settings\n\nclass MyPayPalPayment(StripePayment):\n    def get_paypal_payer_data(self, obj, request):\n        # https://developer.paypal.com/api/orders/v2/#definition-payer\n        data = super().get_paypal_payer_data(obj, request)\n        if obj.user and obj.user.birth_date:\n            data['birth_date'] = obj.user.birth_date.strftime('%Y-%m-%d')\n        return data\n\n    def get_currency(self, request):\n        currency = request.GET.get('currency', None)\n        # Check currency is valid for PayPal...\n        return currency or app_settings.SALESMAN_PAYPAL_DEFAULT_CURRENCY\n```\n\nMake sure to use your payment method in `settings.py`:\n\n```python\nSALESMAN_PAYMENT_METHODS = ['shop.payment.MyPayPalPayment']\n```\n\nThe `PayPalPayment` class is setup with extending in mind, feel free to explore other methods.",
    'author': 'Dino Perovic',
    'author_email': 'dino.perovic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/django-salesman-paypal/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
