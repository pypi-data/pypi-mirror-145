# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcloud', 'gcloud.aio', 'gcloud.aio.kms']

package_data = \
{'': ['*']}

install_requires = \
['gcloud-aio-auth>=3.1.0,<5.0.0']

setup_kwargs = {
    'name': 'gcloud-aio-kms',
    'version': '4.0.0',
    'description': 'Python Client for Google Cloud KMS',
    'long_description': "(Asyncio OR Threadsafe) Python Client for Google Cloud KMS\n==========================================================\n\n    This is a shared codebase for ``gcloud-aio-kms`` and ``gcloud-rest-kms``\n\n|pypi| |pythons-aio| |pythons-rest|\n\nInstallation\n------------\n\n.. code-block:: console\n\n    $ pip install --upgrade gcloud-{aio,rest}-kms\n\nUsage\n-----\n\nWe're still working on more complete documentation, but roughly you can do:\n\n.. code-block:: python\n\n    from gcloud.aio.kms import KMS\n    from gcloud.aio.kms import decode\n    from gcloud.aio.kms import encode\n\n    kms = KMS('my-kms-project', 'my-keyring', 'my-key-name')\n\n    # encrypt\n    plaintext = b'the-best-animal-is-the-aardvark'\n    ciphertext = await kms.encrypt(encode(plaintext))\n\n    # decrypt\n    assert decode(await kms.decrypt(ciphertext)) == plaintext\n\n    # close the HTTP session\n    # Note that other options include:\n    # * providing your own session: ``KMS(.., session=session)``\n    # * using a context manager: ``async with KMS(..) as kms:``\n    await kms.close()\n\nEmulators\n~~~~~~~~~\n\nFor testing purposes, you may want to use ``gcloud-aio-kms`` along with a\nlocal emulator. Setting the ``$KMS_EMULATOR_HOST`` environment variable\nto the address of your emulator should be enough to do the trick.\n\nContributing\n------------\n\nPlease see our `contributing guide`_.\n\n.. _contributing guide: https://github.com/talkiq/gcloud-aio/blob/master/.github/CONTRIBUTING.rst\n\n.. |pypi| image:: https://img.shields.io/pypi/v/gcloud-aio-kms.svg?style=flat-square\n    :alt: Latest PyPI Version (gcloud-aio-kms)\n    :target: https://pypi.org/project/gcloud-aio-kms/\n\n.. |pythons-aio| image:: https://img.shields.io/pypi/pyversions/gcloud-aio-kms.svg?style=flat-square&label=python (aio)\n    :alt: Python Version Support (gcloud-aio-kms)\n    :target: https://pypi.org/project/gcloud-aio-kms/\n\n.. |pythons-rest| image:: https://img.shields.io/pypi/pyversions/gcloud-rest-kms.svg?style=flat-square&label=python (rest)\n    :alt: Python Version Support (gcloud-rest-kms)\n    :target: https://pypi.org/project/gcloud-rest-kms/\n",
    'author': 'Vi Engineering',
    'author_email': 'voiceai-eng@dialpad.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/talkiq/gcloud-aio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
