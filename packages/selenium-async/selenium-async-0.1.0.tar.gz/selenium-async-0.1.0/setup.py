# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['selenium_async', 'selenium_async.vendor']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=4.1.3,<5.0.0']

entry_points = \
{'console_scripts': ['doc = selenium_async._scripts:doc',
                     'format = selenium_async._scripts:format',
                     'test = selenium_async._scripts:test',
                     'test-integration = '
                     'selenium_async._scripts:test_integration']}

setup_kwargs = {
    'name': 'selenium-async',
    'version': '0.1.0',
    'description': 'Wrapper for Selenium to make it easy, with asyncio support!',
    'long_description': '# selenium-async\n\nMake Selenium easy to by managing a browser pool, and `asyncio` compatibility!\n\n-   Source: [https://github.com/munro/python-selenium-async](https://github.com/munro/python-selenium-async)\n-   Documentation: [https://selenium-async.readthedocs.io/en/latest/](https://selenium-async.readthedocs.io/en/latest/)\n\n## install\n\n```bash\npoetry add selenium-async\n```\n\n## usage\n\n```python\nimport selenium_async\n\n\ndef get_title(driver: selenium_async.WebDriver):\n    driver.get("https://www.python.org/")\n    return driver.title\n\nprint(await selenium_async.run_sync(get_title))\n\n# prints: Welcome to Python.org\n```\n\n## license\n\nMIT\n',
    'author': 'Ryan Munro',
    'author_email': '500774+munro@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/munro/python-selenium-async',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
