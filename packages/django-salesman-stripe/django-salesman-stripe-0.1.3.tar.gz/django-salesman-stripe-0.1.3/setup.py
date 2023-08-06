# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['salesman_stripe']

package_data = \
{'': ['*'], 'salesman_stripe': ['templates/salesman_stripe/*']}

install_requires = \
['django-salesman>=1.1.3', 'django>=3.1,<4.1', 'stripe>=2.67.0,<3.0.0']

setup_kwargs = {
    'name': 'django-salesman-stripe',
    'version': '0.1.3',
    'description': 'Stripe payment integration for Salesman.',
    'long_description': "# Salesman Stripe\n\n[![PyPI](https://img.shields.io/pypi/v/django-salesman-stripe)](https://pypi.org/project/django-salesman-stripe/)\n[![Test](https://img.shields.io/github/workflow/status/dinoperovic/django-salesman-stripe/Test/master)](https://github.com/dinoperovic/django-salesman-stripe/actions?query=workflow:Test)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-salesman-stripe)](https://pypi.org/project/django-salesman-stripe/)\n[![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-salesman-stripe)](https://pypi.org/project/django-salesman-stripe/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n[Stripe](https://stripe.com/) payment integration for [Salesman](https://github.com/dinoperovic/django-salesman).\n\n## Installation\n\nInstall the package using pip:\n\n```bash\npip install django-salesman-stripe\n```\n\nAdd to your setting file:\n\n```python\nINSTALLED_APPS += ['salesman_stripe']\nSALESMAN_PAYMENT_METHODS = ['salesman_stripe.payment.StripePayment']\nSALESMAN_STRIPE_SECRET_KEY = '<stripe-secret-key>'\nSALESMAN_STRIPE_WEBHOOK_SECRET = '<stripe-webhook-secret>'\n```\n\n### Local setup\n\nTo simulate webhooks while in development you can use the [Stripe CLI](https://stripe.com/docs/stripe-cli).\nAfter you've installed the CLI, you can run:\n\n```bash\nstripe listen --forward-to localhost:8000/api/payment/stripe/webhook/\n```\n\nThis will connect the webhook and output the signing secret for `SALESMAN_STRIPE_WEBHOOK_SECRET` setting.\n\n### Additional settings\n\nOptional additional settings that you can override:\n\n```python\n# Payment method label used when displayed in the basket.\nSALESMAN_STRIPE_PAYMENT_LABEL = 'Pay with Stripe'\n\n# Default ISO currency used for payments (https://stripe.com/docs/currencies)\nSALESMAN_STRIPE_DEFAULT_CURRENCY = 'usd'\n\n# URL to redirect to when Stripe payment is cancelled.\nSALESMAN_STRIPE_CANCEL_URL = '/stripe/cancel/'\n\n# URL to redirect to when Stripe payment is successfull.\nSALESMAN_STRIPE_SUCCESS_URL = '/stripe/success/'\n\n# Default paid status for fullfiled orders.\nSALESMAN_STRIPE_PAID_STATUS = 'PROCESSING'\n```\n\n### Customer syncing\n\nIt is recommended to enable Stripe customer syncronization with your User model.\nThis will require an extra field on your User model which will hold the Stripe customer ID.\nEasiest way to do this is to define a custom user model:\n\n```python\n# shop/models.py\nfrom salesman_stripe.models import StripeCustomerMixin\n\nclass User(StripeCustomerMixin, AbstractUser):\n    pass\n```\n\nYou should then register your custom user model in `settings.py`:\n\n```python\nAUTH_USER_MODEL = 'shop.User'\n```\n\nAn alternative approach would be to override the `get_stripe_customer_id` and `save_stripe_customer_id`\nmethods in a custom `StripePayment` class, see more in advanced usage section below.\n\n## Advanced usage\n\nTo gain more control feel free to extend the `StripePayment` class with your custom functionality:\n\n```python\n# shop/payment.py\nfrom salesman_stripe.payment import StripePayment\nfrom salesman_stripe.conf import app_settings\n\nclass MyStripePayment(StripePayment):\n    def get_stripe_customer_data(self, obj, request):\n        # https://stripe.com/docs/api/customers/create\n        data = super().get_stripe_customer_data(obj, request)\n        if obj.user and obj.user.phone_number:\n            data['phone'] = obj.user.phone_number\n        return data\n\n    def get_currency(self, request):\n        currency = request.GET.get('currency', None)\n        # Check currency is valid for Stripe...\n        return currency or app_settings.SALESMAN_STRIPE_DEFAULT_CURRENCY\n```\n\nMake sure to use your payment method in `settings.py`:\n\n```python\nSALESMAN_PAYMENT_METHODS = ['shop.payment.MyStripePayment']\n```\n\nThe `StripePayment` class is setup with extending in mind, feel free to explore other methods.\n",
    'author': 'Dino Perovic',
    'author_email': 'dino.perovic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/django-salesman-stripe/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
