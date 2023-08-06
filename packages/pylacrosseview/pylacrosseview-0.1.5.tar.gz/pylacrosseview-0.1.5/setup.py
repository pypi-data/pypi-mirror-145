# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylacrosseview']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT[crypto]>=2.3.0,<3.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pylacrosseview',
    'version': '0.1.5',
    'description': 'Python library that allows you to use La Crosse devices that connect with La Crosse View',
    'long_description': '# pylacrosseview\n\n`pylacrosseview` is a python library that allows you to use La Crosse devices that connect with La Crosse View in your python scripts.\n\nDesigned for Home Assistant.\n\nSee an example below:\n\n```py\nfrom logging import INFO, basicConfig\nfrom os import environ\n\nfrom pylacrosseview import *\n\nif __name__ == "__main__":\n    basicConfig(level=INFO)\n    ws: WeatherStation = WeatherStation()\n    ws.start(environ["LACROSSE_EMAIL"], environ["LACROSSE_PASSWORD"])\n    for device in ws.devices:\n        for field, values in device.states().items():\n            print(f"Value of {field} on {device} is {values[-1].value} {field.unit}")\n```\n',
    'author': 'regulad',
    'author_email': 'regulad@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
