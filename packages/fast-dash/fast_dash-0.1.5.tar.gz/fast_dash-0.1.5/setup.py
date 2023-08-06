# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_dash', 'tests']

package_data = \
{'': ['*'], 'fast_dash': ['assets/*']}

install_requires = \
['Flask>=2.0.2,<3.0.0',
 'dash-bootstrap-components>=1.0.2,<2.0.0',
 'dash[testing]>=2.2.0,<3.0.0',
 'plotly>=5.5.0,<6.0.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.13.6,<0.14.0',
         'livereload>=2.6.3,<3.0.0',
         'mkdocs-autorefs==0.1.1'],
 'test': ['black==20.8b1',
          'isort==5.6.4',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest==6.1.2',
          'pytest-cov==2.10.1',
          'selenium>=4.1.3,<5.0.0']}

setup_kwargs = {
    'name': 'fast-dash',
    'version': '0.1.5',
    'description': 'Build Machine Learning prototypes web applications lightning fast.',
    'long_description': '# Overview\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/fast_dash">\n    <img src="https://img.shields.io/pypi/v/fast_dash?color=%2334D058"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/dkedar7/fast_dash/actions">\n    <img src="https://github.com/dkedar7/fast_dash/actions/workflows/release.yml/badge.svg" alt="CI Status">\n</a>\n\n\n<a href="https://github.com/dkedar7/fast_dash/blob/main/LICENSE">\n    <img src="https://img.shields.io/github/license/dkedar7/fast_dash" alt="MIT License">\n</a>\n\n<a href="https://docs.fastdash.app/">\n    <img src="https://img.shields.io/badge/Docs-MkDocs-<COLOR>.svg" alt="Documentation">\n</a>\n\n</p>\n\n\n<p align="center">\n  <a href="https://fastdash.app/"><img src="https://raw.githubusercontent.com/dkedar7/fast_dash/main/docs/assets/logo.png" alt="Fast Dash logo"></a>\n</p>\n<p align="center">\n    <em>Open source, Python-based tool to build ML prototypes lightning fast.</em>\n</p>\n\n\n---\n\n* Website: <https://fastdash.app/>\n* Documentation: <https://docs.fastdash.app/>\n* Source code: <https://github.com/dkedar7/fast_dash/>\n\n---\n\nFast Dash is a Python module that makes the development of web applications fast and easy. It is built on top of Plotly Dash and can be used to build web interfaces for Machine Learning models or to showcase any proof of concept without the hassle of developing UI from scratch.\n\n<p align="center">\n  <a href="https://fastdash.app/"><img src="https://raw.githubusercontent.com/dkedar7/fast_dash/examples/docs/assets/gallery_4_apps.gif" alt="Fast Dash logo"></a>\n</p>\n\n## Simple example\n\nRun your app with three simple steps:\n\n```python\nfrom fast_dash import FastDash\nfrom fast_dash.Components import Text\n\n# Step 1: Define your model inference\ndef text_to_text_function(input_text):\n    return input_text\n\n# Step 2: Specify the input and output components\napp = FastDash(callback_fn=text_to_text_function, \n                inputs=Text, \n                outputs=Text, \n                title=\'App title\')\n\n# Step 3: Run your app!\napp.run()\n\n# * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n```\n\nAnd just like that, we have a completely functional interactive app!\n\nOutput:\n\n![Simple example](https://raw.githubusercontent.com/dkedar7/fast_dash/main/docs/assets/simple_example.gif)\n\n---\n\nIn a similar way, we can add multiple input as well as output components at the same time.\n\n```python\nfrom fast_dash import FastDash\nfrom fast_dash.Components import Text, Slider\n\n# Step 1: Define your model inference\ndef text_to_text_function(input_text, slider_value):\n    processed_text = f\'{input_text}. Slider value is {slider_value}.\'\n    return processed_text\n\n# Step 2: Specify the input and output components\napp = FastDash(callback_fn=text_to_text_function, \n                inputs=[Text, Slider], \n                outputs=Text,\n                title=\'App title\')\n\n# Step 3: Run your app!\napp.run()\n\n# * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n```\n\n---\n\n![Simple example with multiple inputs](https://raw.githubusercontent.com/dkedar7/fast_dash/main/docs/assets/simple_example_multiple_inputs.gif)\n\nAnd with just a few more lines, we can add a title icon, subheader and social details.\n\n```python\n...\n\napp = FastDash(callback_fn=text_to_text_function, \n                inputs=[Text, Slider], \n                outputs=Text,\n                title=\'App title\',\n                title_image_path=\'https://raw.githubusercontent.com/dkedar7/fast_dash/main/docs/assets/favicon.jpg\',\n                subheader=\'Build a proof-of-concept UI for your Python functions lightning fast.\',\n                github_url=\'https://github.com/dkedar7/fast_dash\',\n                linkedin_url=\'https://linkedin.com/in/dkedar7\',\n                twitter_url=\'https://twitter.com/dkedar\')\n\n...\n\n```\n\nOutput:\n\n![Simple example with multiple inputs and details](https://raw.githubusercontent.com/dkedar7/fast_dash/main/docs/assets/simple_example_multiple_inputs_details.gif.png)\n\n---\n\n## Key features\n\n- Launch an app only by specifying the types of inputs and outputs.\n- Multiple input and output components simultaneously.\n- Flask-based backend allows easy scalability and customizability.\n- Build fast and iterate.\n\nSome features are coming up in future releases:\n\n- More input and output components.\n- Deploy to Heroku and Google Cloud.\n- and many more.\n\n## Community\n\nFast Dash is built on open-source. You are encouraged to share your own projects, which will be highlighted on a common community gallery that\'s upcoming. Join us on [Discord](https://discord.gg/B8nPVfPZ6a).\n\n## Credits\n\nFast Dash is inspired from [gradio](https://github.com/gradio-app/gradio) and built using [Plotly Dash](https://github.com/plotly/dash). Dash\'s Flask-based backend enables Fast Dash apps to scale easily and makes them highly compatibility with other integration services.  Many documentation ideas and concepts are borrowed from [FastAPI\'s docs](https://fastapi.tiangolo.com/) project template.\n\nThe project template was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage).\n',
    'author': 'Kedar Dabhadkar',
    'author_email': 'kedar@fastdash.app',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dkedar7/fast_dash',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
